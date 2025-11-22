#!/usr/bin/env python3
# coding: utf-8
"""
Frontmatter 元数据处理工具集

自动生成，由 Claude Code 管理
生成源: docs/reference/FRONTMATTER.md
版本: 1.0
最后更新: 2025-11-11
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional

try:
    import yaml
except ImportError:
    print("警告: PyYAML 未安装，部分功能不可用", file=sys.stderr)
    print("安装命令: pip install pyyaml", file=sys.stderr)
    yaml = None


class FrontmatterValidator:
    """Frontmatter 验证器"""

    VALID_TYPES = ['技术设计', '系统集成', 'API参考', '教程', '故障排查', '架构决策']
    VALID_STATUSES = ['草稿', '完成', '待审查']
    VALID_PRIORITIES = ['高', '中', '低']
    REQUIRED_FIELDS = [
        'title', 'description', 'type', 'status',
        'priority', 'created_date', 'last_updated'
    ]

    def __init__(self, project_root: Optional[str] = None):
        """
        初始化验证器

        Args:
            project_root: 项目根目录路径，用于验证相对路径
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self._ensure_project_root()

    def _ensure_project_root(self):
        """确保当前在项目根目录（可选检查）"""
        # 宽松检查：只要有 docs/ 目录就认为是有效的项目根目录
        if not (self.project_root / 'docs').exists():
            # 如果没有 docs/ 目录，检查其他常见标识
            common_markers = ['.git', 'PLANNING.md', 'TASK.md', 'package.json', 'setup.py']
            has_marker = any((self.project_root / marker).exists() for marker in common_markers)
            if not has_marker:
                raise RuntimeError(
                    f"警告: 当前目录 ({self.project_root}) 可能不是项目根目录。\n"
                    f"建议从包含 docs/ 目录或其他项目标识文件的目录运行。"
                )

    def validate(self, doc_path: str, frontmatter: Dict) -> Dict[str, any]:
        """
        验证 frontmatter 元数据

        Args:
            doc_path: 文档路径（相对于项目根目录）
            frontmatter: 解析后的 frontmatter 字典

        Returns:
            {
                'valid': bool,
                'errors': List[str],      # 阻塞性错误
                'warnings': List[str]     # 非阻塞性警告
            }
        """
        errors = []
        warnings = []

        # 1. 必需字段检查
        for field in self.REQUIRED_FIELDS:
            if field not in frontmatter:
                errors.append(f"缺少必需字段: {field}")

        # 2. 枚举值验证
        if frontmatter.get('type') not in self.VALID_TYPES:
            errors.append(f"无效的 type 值: {frontmatter.get('type')}")

        if frontmatter.get('status') not in self.VALID_STATUSES:
            errors.append(f"无效的 status 值: {frontmatter.get('status')}")

        if frontmatter.get('priority') not in self.VALID_PRIORITIES:
            errors.append(f"无效的 priority 值: {frontmatter.get('priority')}")

        # 3. 日期格式验证
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        for date_field in ['created_date', 'last_updated', 'next_review_date']:
            if date_field in frontmatter:
                if not date_pattern.match(str(frontmatter[date_field])):
                    errors.append(f"{date_field} 格式错误，应为 YYYY-MM-DD")

        # 4. 日期逻辑验证
        if 'created_date' in frontmatter and 'last_updated' in frontmatter:
            if frontmatter['created_date'] > frontmatter['last_updated']:
                errors.append("created_date 不能晚于 last_updated")

        # 5. 关系引用验证
        if 'related_documents' in frontmatter:
            for doc in frontmatter['related_documents']:
                doc_path_ref = doc.get('path', '')
                if doc_path_ref and not (self.project_root / doc_path_ref).exists():
                    warnings.append(f"related_documents 引用的文档不存在: {doc_path_ref}")

        if 'related_code' in frontmatter:
            for code in frontmatter['related_code']:
                code_path_ref = code.get('path', '')
                if code_path_ref and not (self.project_root / code_path_ref).exists():
                    warnings.append(f"related_code 引用的代码文件不存在: {code_path_ref}")

        # 6. 任务引用验证
        if 'related_tasks' in frontmatter:
            task_file = self.project_root / 'TASK.md'
            if task_file.exists():
                task_content = task_file.read_text(encoding='utf-8')
                for task_ref in frontmatter['related_tasks']:
                    if task_ref not in task_content:
                        warnings.append(f"related_tasks 引用的任务不在 TASK.md 中: {task_ref}")
            else:
                warnings.append("无法验证 related_tasks: TASK.md 不存在")

        # 7. 推荐字段提醒
        recommended = ['related_documents', 'related_code', 'tags']
        missing_recommended = [f for f in recommended if f not in frontmatter]
        if missing_recommended:
            warnings.append(f"建议添加推荐字段: {', '.join(missing_recommended)}")

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def validate_batch(self, directory: str) -> List[Dict]:
        """批量验证目录下所有文档"""
        results = []
        docs_dir = self.project_root / directory

        for md_file in docs_dir.rglob('*.md'):
            try:
                frontmatter = self._extract_frontmatter(md_file)
                if frontmatter:
                    rel_path = md_file.relative_to(self.project_root)
                    validation = self.validate(str(rel_path), frontmatter)
                    results.append({
                        'file': str(rel_path),
                        'validation': validation
                    })
            except Exception as e:
                results.append({
                    'file': str(md_file.relative_to(self.project_root)),
                    'error': str(e)
                })

        return results

    def _extract_frontmatter(self, file_path: Path) -> Optional[Dict]:
        """从 Markdown 文件中提取 frontmatter"""
        if not yaml:
            raise ImportError("需要安装 PyYAML: pip install pyyaml")

        content = file_path.read_text(encoding='utf-8')
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except yaml.YAMLError as e:
                raise ValueError(f"YAML 解析错误: {e}")
        return None


class FrontmatterGenerator:
    """Frontmatter 模板生成器"""

    TYPE_MAPPING = {
        'api/': 'API参考',
        'architecture/': '技术设计',
        'deployment/': '系统集成',
        'development/': '教程',
        'troubleshooting/': '故障排查',
        'adr/': '架构决策'
    }

    def determine_priority(self, doc_type: str, reference_count: int = 0) -> str:
        """
        基于文档类型和引用次数确定优先级

        Args:
            doc_type: 文档类型
            reference_count: 被引用次数

        Returns:
            优先级字符串
        """
        high_priority_types = ['API参考', '系统集成', '架构决策']

        if doc_type in high_priority_types:
            return '高'
        elif reference_count > 5:
            return '高'
        elif reference_count > 2:
            return '中'
        else:
            return '低'

    def generate_template(self, doc_path: str) -> str:
        """
        为文档生成默认 frontmatter

        Args:
            doc_path: 文档路径

        Returns:
            frontmatter YAML 字符串
        """
        # 从路径推断 type
        doc_type = '技术设计'  # 默认
        for path_prefix, dtype in self.TYPE_MAPPING.items():
            if path_prefix in doc_path:
                doc_type = dtype
                break

        # 从文件名提取 title
        filename = os.path.basename(doc_path)
        title = filename.replace('.md', '').replace('-', ' ').replace('_', ' ').title()

        # 设置日期
        today = datetime.now().strftime('%Y-%m-%d')
        review_date = (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')

        # 根据类型确定优先级
        priority = self.determine_priority(doc_type)

        return f"""---
title: "{title}"
description: "TODO: 添加文档描述"
type: "{doc_type}"
status: "草稿"
priority: "{priority}"
created_date: "{today}"
last_updated: "{today}"
related_documents: []
related_code: []
tags: []
authors: ["Claude"]
version: "1.0"
next_review_date: "{review_date}"
---
"""


class DocumentGraphBuilder:
    """文档关系图构建器"""

    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.validator = FrontmatterValidator(str(self.project_root))

    def build_graph(self, directory: str) -> Dict:
        """
        构建文档关系图

        Args:
            directory: 要扫描的目录

        Returns:
            {
                'nodes': List[Dict],  # 文档节点
                'edges': List[Dict]   # 关系边
            }
        """
        nodes = []
        edges = []
        docs_dir = self.project_root / directory

        # 扫描所有文档
        for md_file in docs_dir.rglob('*.md'):
            try:
                frontmatter = self.validator._extract_frontmatter(md_file)
                if not frontmatter:
                    continue

                rel_path = str(md_file.relative_to(self.project_root))

                # 添加节点
                nodes.append({
                    'id': rel_path,
                    'title': frontmatter.get('title', 'Untitled'),
                    'type': frontmatter.get('type', 'Unknown'),
                    'status': frontmatter.get('status', 'Unknown'),
                    'priority': frontmatter.get('priority', 'Unknown')
                })

                # 添加文档关系边
                for related_doc in frontmatter.get('related_documents', []):
                    edges.append({
                        'source': rel_path,
                        'target': related_doc.get('path', ''),
                        'type': 'document_relation',
                        'relation_type': related_doc.get('type', 'unknown'),
                        'description': related_doc.get('description', '')
                    })

                # 添加代码关系边
                for related_code in frontmatter.get('related_code', []):
                    edges.append({
                        'source': rel_path,
                        'target': related_code.get('path', ''),
                        'type': 'code_relation',
                        'relation_type': related_code.get('type', 'unknown'),
                        'description': related_code.get('description', '')
                    })

            except Exception as e:
                print(f"警告: 处理 {md_file} 时出错: {e}", file=sys.stderr)

        return {
            'nodes': nodes,
            'edges': edges,
            'stats': {
                'total_documents': len(nodes),
                'total_relations': len(edges),
                'document_relations': len([e for e in edges if e['type'] == 'document_relation']),
                'code_relations': len([e for e in edges if e['type'] == 'code_relation'])
            }
        }

    def export_mermaid(self, graph: Dict) -> str:
        """导出为 Mermaid 格式"""
        lines = ["graph TD"]

        # 添加节点
        for node in graph['nodes']:
            node_id = node['id'].replace('/', '_').replace('.', '_')
            label = f"{node['title']}<br/>[{node['type']}]"
            lines.append(f'    {node_id}["{label}"]')

        # 添加边
        for edge in graph['edges']:
            if edge['type'] == 'document_relation':
                source_id = edge['source'].replace('/', '_').replace('.', '_')
                target_id = edge['target'].replace('/', '_').replace('.', '_')
                relation = edge['relation_type']
                lines.append(f'    {source_id} -->|{relation}| {target_id}')

        return '\n'.join(lines)


def format_output(data: any, format_type: str) -> str:
    """格式化输出"""
    if format_type == 'json':
        return json.dumps(data, ensure_ascii=False, indent=2)
    elif format_type == 'yaml':
        if not yaml:
            return "错误: PyYAML 未安装"
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)
    elif format_type == 'table':
        # 简单的表格格式
        if isinstance(data, list):
            return '\n'.join([str(item) for item in data])
        return str(data)
    else:
        return str(data)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='Frontmatter 元数据处理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 验证单个文件
  %(prog)s validate docs/api/auth.md

  # 批量验证目录
  %(prog)s validate-batch docs/

  # 生成模板
  %(prog)s generate docs/api/new-api.md

  # 构建关系图
  %(prog)s graph docs/ --format mermaid > docs/graph.mmd
        """
    )

    parser.add_argument('command',
                        choices=['validate', 'validate-batch', 'generate', 'graph'],
                        help='要执行的命令')
    parser.add_argument('target',
                        help='目标文件或目录路径')
    parser.add_argument('--format',
                        choices=['json', 'yaml', 'table', 'mermaid'],
                        default='json',
                        help='输出格式 (默认: json)')
    parser.add_argument('--project-root',
                        default='.',
                        help='项目根目录路径 (默认: 当前目录)')

    args = parser.parse_args()

    try:
        if args.command == 'validate':
            validator = FrontmatterValidator(args.project_root)
            frontmatter = validator._extract_frontmatter(Path(args.target))
            if frontmatter:
                result = validator.validate(args.target, frontmatter)
                print(format_output(result, args.format))
            else:
                print("错误: 未找到 frontmatter", file=sys.stderr)
                sys.exit(1)

        elif args.command == 'validate-batch':
            validator = FrontmatterValidator(args.project_root)
            results = validator.validate_batch(args.target)
            print(format_output(results, args.format))

        elif args.command == 'generate':
            generator = FrontmatterGenerator()
            template = generator.generate_template(args.target)
            print(template)

        elif args.command == 'graph':
            builder = DocumentGraphBuilder(args.project_root)
            graph = builder.build_graph(args.target)
            if args.format == 'mermaid':
                print(builder.export_mermaid(graph))
            else:
                print(format_output(graph, args.format))

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
