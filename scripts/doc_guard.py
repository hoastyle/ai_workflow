#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档守卫工具 (Doc Guard)

功能：
- 自动检测文档大小
- 智能选择加载策略
- 拦截大文档直接读取
- Token 预算管理

使用示例：
    # 基础用法
    python scripts/doc_guard.py --docs "PLANNING.md,TASK.md"

    # 指定章节
    python scripts/doc_guard.py \
      --docs "docs/guides/large_guide.md" \
      --sections '{"docs/guides/large_guide.md": ["Step 3", "MCP Integration"]}'

    # 自定义 token 预算
    python scripts/doc_guard.py --docs "PLANNING.md" --budget 5000
"""

import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from commands.lib.doc_loader import DocLoader
except ImportError:
    print("⚠️ 警告: 无法导入 DocLoader，使用简化模式", file=sys.stderr)
    DocLoader = None


class DocGuardError(Exception):
    """文档守卫错误"""
    pass


class DocGuard:
    """文档守卫核心类"""

    # 文档大小阈值（行数）
    SIZE_SMALL = 100      # < 100: 完整读取
    SIZE_MEDIUM = 300     # 100-300: 摘要模式
    SIZE_LARGE = 800      # 300-800: 章节模式
    # > 800: 拒绝完整读取

    def __init__(self, token_budget: int = 20000):
        """
        初始化文档守卫

        Args:
            token_budget: Token 预算上限
        """
        self.loader = DocLoader() if DocLoader else None
        self.token_budget = token_budget
        self.token_used = 0
        self.violations = []
        self.load_stats = []

    def load_docs(
        self,
        doc_paths: List[str],
        sections_map: Optional[Dict[str, List[str]]] = None
    ) -> Dict[str, str]:
        """
        批量加载文档

        Args:
            doc_paths: 文档路径列表
            sections_map: {doc_path: [sections]} 章节映射（可选）

        Returns:
            {doc_path: content} 文档内容字典
        """
        results = {}
        sections_map = sections_map or {}

        print(f"\n📚 Doc Guard 开始加载 {len(doc_paths)} 个文档...\n", file=sys.stderr)

        for doc_path in doc_paths:
            sections = sections_map.get(doc_path)
            try:
                content = self._load_single(doc_path, sections)
                results[doc_path] = content
            except DocGuardError as e:
                self.violations.append(str(e))
                print(f"❌ {e}\n", file=sys.stderr)

        # 输出统计
        self._print_summary()

        return results

    def _load_single(self, doc_path: str, sections: Optional[List[str]] = None) -> str:
        """
        单个文档智能加载

        Args:
            doc_path: 文档路径
            sections: 需要加载的章节列表

        Returns:
            文档内容

        Raises:
            DocGuardError: 文档不存在或超过大小限制
        """
        # 检查文件是否存在
        path = Path(doc_path)
        if not path.exists():
            raise DocGuardError(f"文档不存在: {doc_path}")

        # 统计行数
        lines = self._count_lines(doc_path)

        print(f"📄 {doc_path}: {lines} 行", file=sys.stderr)

        # 策略选择
        if lines < self.SIZE_SMALL:
            strategy = "完整读取"
            content = self._read_full(doc_path)
            tokens = self._estimate_tokens(content)

        elif lines < self.SIZE_MEDIUM:
            strategy = "摘要模式（50行）"
            if self.loader:
                content = self.loader.load_summary(doc_path, max_lines=50)
            else:
                # 降级：读取前50行
                content = self._read_head(doc_path, 50)
            tokens = self._estimate_tokens(content)

        elif lines < self.SIZE_LARGE:
            if not sections:
                raise DocGuardError(
                    f"文档 {doc_path} 有 {lines} 行，必须指定 --sections 参数\n"
                    f"  建议: 使用 --sections '{{\"{doc_path}\": [\"章节1\", \"章节2\"]}}'"
                )
            strategy = f"章节模式 {sections}"
            if self.loader:
                section_dict = self.loader.load_sections(doc_path, sections)
                # 合并所有章节内容
                content = "\n\n".join(section_dict.values())
            else:
                # 降级：读取前100行并提示
                content = self._read_head(doc_path, 100)
                content = f"[降级模式: 仅加载前100行]\n\n{content}"
            tokens = self._estimate_tokens(content)

        else:
            raise DocGuardError(
                f"文档 {doc_path} 有 {lines} 行，超过限制（{self.SIZE_LARGE}行）\n"
                f"  建议: 必须指定 --sections 加载部分章节"
            )

        # 更新统计
        self.token_used += tokens
        self.load_stats.append({
            'path': doc_path,
            'lines': lines,
            'strategy': strategy,
            'tokens': tokens
        })

        print(f"  ✅ 策略: {strategy}", file=sys.stderr)
        print(f"  📊 Token: ~{tokens}", file=sys.stderr)

        # 检查预算
        if self.token_used > self.token_budget:
            print(
                f"  ⚠️  警告: Token 消耗 {self.token_used} 超出预算 {self.token_budget}",
                file=sys.stderr
            )

        return content

    def _count_lines(self, doc_path: str) -> int:
        """统计文档行数"""
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                return len(f.readlines())
        except Exception as e:
            raise DocGuardError(f"无法读取文档 {doc_path}: {e}")

    def _read_full(self, doc_path: str) -> str:
        """完整读取小文档"""
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise DocGuardError(f"无法读取文档 {doc_path}: {e}")

    def _read_head(self, doc_path: str, n_lines: int) -> str:
        """读取文档前 N 行"""
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                lines = [next(f) for _ in range(n_lines)]
                return ''.join(lines)
        except StopIteration:
            # 文件不足 N 行，返回全部
            with open(doc_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise DocGuardError(f"无法读取文档 {doc_path}: {e}")

    def _estimate_tokens(self, text: str) -> int:
        """估算文本的 token 数量（粗略估计：1 token ≈ 4 字符）"""
        return len(text) // 4

    def _print_summary(self):
        """输出加载统计摘要"""
        print(f"\n{'='*80}", file=sys.stderr)
        print(f"📊 Doc Guard 加载统计", file=sys.stderr)
        print(f"{'='*80}", file=sys.stderr)

        print(f"\n文档加载详情:", file=sys.stderr)
        for stat in self.load_stats:
            print(f"  • {stat['path']}", file=sys.stderr)
            print(f"    - 行数: {stat['lines']}", file=sys.stderr)
            print(f"    - 策略: {stat['strategy']}", file=sys.stderr)
            print(f"    - Token: ~{stat['tokens']}", file=sys.stderr)

        print(f"\n总计:", file=sys.stderr)
        print(f"  • 加载文档数: {len(self.load_stats)}", file=sys.stderr)
        print(f"  • Token 消耗: ~{self.token_used}", file=sys.stderr)
        print(f"  • Token 预算: {self.token_budget}", file=sys.stderr)
        print(f"  • 预算使用率: {self.token_used / self.token_budget * 100:.1f}%", file=sys.stderr)

        if self.violations:
            print(f"\n⚠️  违规记录:", file=sys.stderr)
            for v in self.violations:
                print(f"  • {v}", file=sys.stderr)
        else:
            print(f"\n✅ 无违规记录", file=sys.stderr)

        print(f"\n{'='*80}\n", file=sys.stderr)


def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(
        description="文档守卫工具 - 防止大文档读取导致上下文爆炸",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 基础用法
  python scripts/doc_guard.py --docs "PLANNING.md,TASK.md"

  # 指定章节
  python scripts/doc_guard.py \\
    --docs "docs/guides/large_guide.md" \\
    --sections '{"docs/guides/large_guide.md": ["Step 3", "MCP Integration"]}'

  # 自定义 token 预算
  python scripts/doc_guard.py --docs "PLANNING.md" --budget 5000
        """
    )

    parser.add_argument(
        '--docs',
        required=True,
        help='文档路径，逗号分隔（如: PLANNING.md,TASK.md）'
    )
    parser.add_argument(
        '--sections',
        help='章节映射（JSON 格式），如: \'{"path/to/doc.md": ["章节1", "章节2"]}\''
    )
    parser.add_argument(
        '--budget',
        type=int,
        default=20000,
        help='Token 预算上限（默认: 20000）'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='安静模式，仅输出文档内容'
    )

    args = parser.parse_args()

    # 解析文档列表
    doc_paths = [d.strip() for d in args.docs.split(',')]

    # 解析章节映射
    sections_map = None
    if args.sections:
        try:
            sections_map = json.loads(args.sections)
        except json.JSONDecodeError as e:
            print(f"❌ 错误: 无法解析 --sections 参数: {e}", file=sys.stderr)
            sys.exit(1)

    # 创建守卫并加载文档
    guard = DocGuard(token_budget=args.budget)

    try:
        results = guard.load_docs(doc_paths, sections_map)
    except Exception as e:
        print(f"❌ 加载失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 输出文档内容
    if not args.quiet:
        print("\n" + "="*80)
        print("📄 文档内容")
        print("="*80 + "\n")

    for doc_path, content in results.items():
        if not args.quiet:
            print(f"# {doc_path}\n")
        print(content)
        if not args.quiet:
            print("\n" + "-"*80 + "\n")

    # 检查违规
    if guard.violations:
        print(f"\n⚠️  发现 {len(guard.violations)} 个违规", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
