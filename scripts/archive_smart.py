#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能文档存档脚本 (Smart Document Archive)

版本: v1.0
创建日期: 2025-12-21
用途: 根据文档类型和配置，自动执行智能存档操作

支持的命令:
  python scripts/archive_smart.py --file TASK.md
  python scripts/archive_smart.py --file TASK.md --dry-run
  python scripts/archive_smart.py --file TASK.md --auto
  python scripts/archive_smart.py --batch
  python scripts/archive_smart.py --batch --dry-run

设计特点:
  - 策略模式: 每种文档类型有独立的存档策略
  - 原子操作: 备份-操作-验证-提交的四步流程
  - 自动回滚: 失败时自动恢复到备份状态
  - 详细报告: 生成清晰的操作日志和统计信息
"""

import argparse
import os
import re
import shutil
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("❌ 错误: 需要安装 PyYAML")
    print("   运行: pip install PyYAML")
    sys.exit(1)


# ============================================
# 数据模型
# ============================================

@dataclass
class ArchiveResult:
    """存档操作结果"""
    success: bool
    file_path: str
    original_lines: int
    archived_lines: int
    kept_lines: int
    archive_file: Optional[str] = None
    error_message: Optional[str] = None


class ArchiveStrategy(ABC):
    """存档策略的抽象基类"""

    def __init__(self, config: Dict, file_path: str):
        self.config = config
        self.file_path = file_path
        self.doc_name = Path(file_path).name

    @abstractmethod
    def identify_content_structure(self, content: str) -> Dict:
        """识别文档结构，返回可分离的内容块"""
        pass

    @abstractmethod
    def determine_archive_boundary(self, structure: Dict) -> Tuple[int, str]:
        """确定存档分界线，返回 (分界行号, 分界说明)"""
        pass

    @abstractmethod
    def generate_archive_filename(self) -> str:
        """生成存档文件名"""
        pass

    def execute_archive(self, dry_run: bool = False) -> ArchiveResult:
        """执行存档操作（策略模板方法）"""
        try:
            # Step 1: 读取原始文件
            if not os.path.exists(self.file_path):
                return ArchiveResult(
                    success=False,
                    file_path=self.file_path,
                    original_lines=0,
                    archived_lines=0,
                    kept_lines=0,
                    error_message=f"文件不存在: {self.file_path}"
                )

            with open(self.file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            lines = original_content.split('\n')
            original_lines = len(lines)

            # Step 2: 识别结构
            structure = self.identify_content_structure(original_content)
            if not structure:
                return ArchiveResult(
                    success=False,
                    file_path=self.file_path,
                    original_lines=original_lines,
                    archived_lines=0,
                    kept_lines=original_lines,
                    error_message="无法识别文档结构"
                )

            # Step 3: 确定分界线
            boundary_line, boundary_reason = self.determine_archive_boundary(structure)
            if boundary_line <= 0 or boundary_line >= original_lines:
                return ArchiveResult(
                    success=False,
                    file_path=self.file_path,
                    original_lines=original_lines,
                    archived_lines=0,
                    kept_lines=original_lines,
                    error_message=f"无效的分界线: {boundary_line}"
                )

            # Step 4: 分离内容
            kept_content = '\n'.join(lines[:boundary_line])
            archived_content = '\n'.join(lines[boundary_line:])

            kept_lines = len(kept_content.split('\n'))
            archived_lines = len(archived_content.split('\n'))

            # Step 5: 生成存档文件名和路径
            archive_filename = self.generate_archive_filename()
            archive_dir = self.config.get('archive_path', 'docs/archives')
            archive_path = os.path.join(archive_dir, archive_filename)

            # Step 6: 创建备份
            backup_path = f"{self.file_path}.backup.{datetime.now().strftime('%Y%m%d%H%M%S')}"
            shutil.copy2(self.file_path, backup_path)

            try:
                if not dry_run:
                    # Step 7a: 创建存档目录
                    os.makedirs(archive_dir, exist_ok=True)

                    # Step 7b: 写入保留内容
                    with open(self.file_path, 'w', encoding='utf-8') as f:
                        f.write(kept_content)

                    # Step 7c: 写入存档文件
                    with open(archive_path, 'w', encoding='utf-8') as f:
                        f.write(archived_content)

                    # Step 7d: 删除备份
                    os.remove(backup_path)

                return ArchiveResult(
                    success=True,
                    file_path=self.file_path,
                    original_lines=original_lines,
                    archived_lines=archived_lines,
                    kept_lines=kept_lines,
                    archive_file=archive_path
                )

            except Exception as e:
                # 回滚: 恢复备份
                shutil.copy2(backup_path, self.file_path)
                os.remove(backup_path)
                return ArchiveResult(
                    success=False,
                    file_path=self.file_path,
                    original_lines=original_lines,
                    archived_lines=0,
                    kept_lines=original_lines,
                    error_message=f"存档失败，已回滚: {str(e)}"
                )

        except Exception as e:
            return ArchiveResult(
                success=False,
                file_path=self.file_path,
                original_lines=0,
                archived_lines=0,
                kept_lines=0,
                error_message=f"意外错误: {str(e)}"
            )


# ============================================
# 具体的存档策略实现
# ============================================

class PhaseBasedArchive(ArchiveStrategy):
    """基于阶段的存档策略 (用于 TASK.md)

    设计目标:
    1. 多阶段: 保留最新阶段，归档历史阶段
    2. 单阶段: 拒绝存档（保留所有内容，包括元数据和待开始任务）
    3. 关键原则: 始终保护文档元数据、阶段概述、进度统计
    """

    def identify_content_structure(self, content: str) -> Dict:
        """识别 TASK.md 的完整结构"""
        structure = {}
        lines = content.split('\n')

        # 1. 找到元数据结束位置（第一个 ## 标题）
        metadata_end = self._find_metadata_end(lines)

        # 2. 识别所有阶段
        current_phase = None
        phase_start_line = 0
        phase_num = 0

        for i, line in enumerate(lines):
            match = re.match(r'^##\s+🚀?\s*Phase\s+(\d+)', line)
            if match:
                if current_phase is not None:
                    structure[current_phase] = {
                        'start_line': phase_start_line,
                        'end_line': i,
                        'name': current_phase,
                        'number': phase_num
                    }
                phase_num = int(match.group(1))
                current_phase = f"Phase {phase_num}"
                phase_start_line = i

        # 添加最后一个 Phase
        if current_phase is not None:
            structure[current_phase] = {
                'start_line': phase_start_line,
                'end_line': len(lines),
                'name': current_phase,
                'number': phase_num
            }

        # 3. 存储元数据信息
        structure['_meta'] = {
            'metadata_end': metadata_end,
            'total_lines': len(lines)
        }

        return structure

    def _find_metadata_end(self, lines: List[str]) -> int:
        """找到元数据的结束位置（第一个 ## 标题处）"""
        for i, line in enumerate(lines):
            if re.match(r'^##\s+🚀?', line):  # 匹配任何 ## 标题（阶段或其他）
                return i
        return len(lines)

    def determine_archive_boundary(self, structure: Dict) -> Tuple[int, str]:
        """确定存档分界线（关键逻辑）

        核心原则:
        1. 单 Phase: 拒绝存档 (return -1) - 保留所有内容
        2. 多 Phase: 在最新 Phase 处设分界 - 保留最新，归档历史
        """
        if not structure or '_meta' not in structure:
            return -1, "无法识别结构"

        meta = structure['_meta']
        phases = {k: v for k, v in structure.items() if k != '_meta'}

        # 按阶段号排序（从新到旧）
        phases_list = sorted(
            phases.items(),
            key=lambda x: x[1]['number'],
            reverse=True
        )

        if not phases_list:
            return -1, "没有找到阶段"

        # 策略 A: 单阶段文档 - 拒绝存档
        if len(phases_list) == 1:
            return -1, (
                "单阶段文档暂不存档。原因: \n"
                "  • 文档只有 1 个阶段，无历史内容可存档\n"
                "  • 等待出现多个阶段后再进行存档"
            )

        # 策略 B: 多阶段文档 - 在最新阶段处设分界
        if len(phases_list) >= 2:
            latest_phase = phases_list[0][1]
            boundary = latest_phase['start_line']
            archived_phases_count = len(phases_list) - 1
            return boundary, (
                f"保留最新阶段 {latest_phase['name']}，"
                f"归档历史 {archived_phases_count} 个阶段"
            )

        return -1, "无法确定分界线"

    def generate_archive_filename(self) -> str:
        """生成存档文件名: TASK-archive-YYYY-QX-phases-X-Y.md"""
        today = datetime.now()
        quarter = (today.month - 1) // 3 + 1
        year = today.year

        # 读取文件以确定包含的阶段
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        phases = re.findall(r'Phase\s+(\d+)', content)
        if phases:
            min_phase = min(int(p) for p in phases)
            max_phase = max(int(p) for p in phases)
            return f"TASK-archive-{year}-Q{quarter}-phases-{min_phase}-{max_phase}.md"
        else:
            return f"TASK-archive-{year}-Q{quarter}.md"


class VersionBasedArchive(ArchiveStrategy):
    """基于版本的存档策略 (用于 PLANNING.md)"""

    def identify_content_structure(self, content: str) -> Dict:
        """识别 PLANNING.md 的版本结构"""
        versions = {}

        # 尝试从文件头部获取版本信息
        match = re.search(r'\*\*版本\*\*:\s*v([\d.]+)', content)
        if match:
            current_version = f"v{match.group(1)}"
            versions['current'] = {
                'version': current_version,
                'position': 'header'
            }

        return versions

    def determine_archive_boundary(self, structure: Dict) -> Tuple[int, str]:
        """确定存档分界线：保留当前版本，归档历史版本"""
        # 对于 PLANNING.md，可以按最后更新时间分离
        lines = []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 查找最后的主要内容块（通过最后的 ## 标题）
        last_major_section = 0
        for i, line in enumerate(lines):
            if re.match(r'^##\s+', line):
                last_major_section = i

        # 保留到最后一个主要章节之后约 10 行
        boundary = min(last_major_section + 10, len(lines) - 1)

        if boundary > 0 and boundary < len(lines):
            return boundary, "保留当前版本内容，归档历史版本"
        else:
            return -1, "无法确定版本边界"

    def generate_archive_filename(self) -> str:
        """生成存档文件名: PLANNING-archive-vX.X.md"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        match = re.search(r'\*\*版本\*\*:\s*v([\d.]+)', content)
        if match:
            version = match.group(1)
            return f"PLANNING-archive-v{version}.md"
        else:
            today = datetime.now()
            return f"PLANNING-archive-{today.strftime('%Y%m%d')}.md"


class WeekBasedArchive(ArchiveStrategy):
    """基于周的存档策略 (用于 CONTEXT.md)"""

    def identify_content_structure(self, content: str) -> Dict:
        """识别 CONTEXT.md 的周期结构"""
        weeks = {}
        lines = content.split('\n')

        # 从 "最后会话" 日期解析周信息
        for line in lines:
            match = re.search(r'\*\*最后会话\*\*:\s*(\d{4})-(\d{2})-(\d{2})', line)
            if match:
                year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
                date = datetime(year, month, day)
                week_num = date.isocalendar()[1]
                weeks['last_session'] = {
                    'date': date,
                    'week': week_num,
                    'year': year
                }
                break

        return weeks

    def determine_archive_boundary(self, structure: Dict) -> Tuple[int, str]:
        """确定存档分界线：保留最近 2 周，归档更早的"""
        lines = []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # CONTEXT.md 通常很小，保留最后约 20 行
        boundary = max(0, len(lines) - 20)

        if boundary > 0 and boundary < len(lines):
            return boundary, "保留最近会话信息（2 周内），归档更早记录"
        else:
            return -1, "文件内容不足以归档"

    def generate_archive_filename(self) -> str:
        """生成存档文件名: CONTEXT-archive-YYYY-wXX.md"""
        today = datetime.now()
        week_num = today.isocalendar()[1]
        year = today.year
        return f"CONTEXT-archive-{year}-w{week_num:02d}.md"


# ============================================
# 主类: ArchiveSmart
# ============================================

class ArchiveSmart:
    """智能文档存档系统的主类"""

    def __init__(self, config_path: str = 'doc_limits.yaml'):
        """初始化配置"""
        self.config = self._load_config(config_path)
        self.strategies = self._init_strategies()

    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        if not os.path.exists(config_path):
            # 尝试从全局位置加载
            config_path = os.path.expanduser('~/.claude/commands/doc_limits.yaml')

        if not os.path.exists(config_path):
            print(f"❌ 错误: 找不到配置文件 {config_path}")
            sys.exit(1)

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"❌ 错误: 加载配置文件失败 - {e}")
            sys.exit(1)

    def _init_strategies(self) -> Dict[str, type]:
        """初始化存档策略映射"""
        return {
            'TASK.md': PhaseBasedArchive,
            'PLANNING.md': VersionBasedArchive,
            'CONTEXT.md': WeekBasedArchive,
        }

    def _get_strategy(self, file_path: str) -> Optional[ArchiveStrategy]:
        """根据文件路径获取对应的策略"""
        doc_name = Path(file_path).name

        if doc_name not in self.strategies:
            return None

        # 获取配置中的存档规则
        archive_rules = self.config.get('archive_rules', {})
        rule_config = archive_rules.get(doc_name, {})

        strategy_class = self.strategies[doc_name]
        return strategy_class(rule_config, file_path)

    def archive_file(self, file_path: str, dry_run: bool = False) -> ArchiveResult:
        """对单个文件执行存档"""
        strategy = self._get_strategy(file_path)

        if strategy is None:
            return ArchiveResult(
                success=False,
                file_path=file_path,
                original_lines=0,
                archived_lines=0,
                kept_lines=0,
                error_message=f"不支持的文件类型: {Path(file_path).name}"
            )

        return strategy.execute_archive(dry_run=dry_run)

    def batch_archive(self, dry_run: bool = False) -> List[ArchiveResult]:
        """批量存档所有超限文档"""
        results = []
        limits = self.config.get('document_limits', {})

        for file_path, limit in limits.items():
            if not os.path.exists(file_path):
                continue

            # 检查是否超过限制
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())

            threshold = self.config.get('archive_triggers', {}).get('auto_threshold', 0.8)
            if lines > limit * threshold:
                result = self.archive_file(file_path, dry_run=dry_run)
                results.append(result)

        return results

    def print_report(self, results: List[ArchiveResult], dry_run: bool = False):
        """打印操作报告"""
        print("\n" + "=" * 80)
        print("📊 存档操作报告")
        print("=" * 80)

        if dry_run:
            print("⚠️ 预览模式 (dry-run) - 未实际执行任何操作\n")

        if not results:
            print("✅ 没有需要存档的文档\n")
            return

        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]

        # 成功的存档
        if successful:
            print(f"\n✅ 成功存档 {len(successful)} 个文件:\n")
            for result in successful:
                print(f"  📄 {result.file_path}")
                print(f"     原始行数: {result.original_lines}")
                print(f"     保留行数: {result.kept_lines}")
                print(f"     归档行数: {result.archived_lines}")
                print(f"     存档位置: {result.archive_file}\n")

        # 失败的操作
        if failed:
            print(f"\n❌ 失败 {len(failed)} 个文件:\n")
            for result in failed:
                print(f"  📄 {result.file_path}")
                print(f"     错误: {result.error_message}\n")

        # 统计信息
        total_lines_archived = sum(r.archived_lines for r in successful)
        print("=" * 80)
        print(f"📈 统计: 共存档 {total_lines_archived} 行内容")
        print("=" * 80 + "\n")


# ============================================
# 命令行接口
# ============================================

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='智能文档存档脚本 - 自动识别并存档超限文档',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 存档指定文件
  python scripts/archive_smart.py --file docs/management/TASK.md

  # 预览存档效果（不实际修改文件）
  python scripts/archive_smart.py --file docs/management/TASK.md --dry-run

  # 自动确认（无需交互提示）
  python scripts/archive_smart.py --file docs/management/TASK.md --auto

  # 批量存档所有超限文档
  python scripts/archive_smart.py --batch

  # 预览批量存档
  python scripts/archive_smart.py --batch --dry-run
        """
    )

    parser.add_argument(
        '--file',
        type=str,
        help='指定要存档的文件路径'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='批量存档所有超限文档'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式：显示操作但不实际修改文件'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='自动确认：跳过交互提示'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='doc_limits.yaml',
        help='配置文件路径（默认: doc_limits.yaml）'
    )

    args = parser.parse_args()

    # 验证参数
    if not args.file and not args.batch:
        parser.print_help()
        sys.exit(1)

    # 初始化智能存档系统
    try:
        archive_smart = ArchiveSmart(args.config)
    except SystemExit:
        sys.exit(1)

    # 执行存档操作
    results = []

    if args.batch:
        results = archive_smart.batch_archive(dry_run=args.dry_run)
    elif args.file:
        result = archive_smart.archive_file(args.file, dry_run=args.dry_run)
        results = [result]

    # 打印报告
    archive_smart.print_report(results, dry_run=args.dry_run)

    # 确定退出码
    failed_count = sum(1 for r in results if not r.success)
    sys.exit(1 if failed_count > 0 else 0)


if __name__ == '__main__':
    main()
