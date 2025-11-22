#!/usr/bin/env python3
# coding: utf-8
"""
文档关系图生成器（便捷包装）

快速生成文档关系图的命令行工具
由 Claude Code 管理
版本: 1.0
最后更新: 2025-11-11
"""

import argparse
import sys
from pathlib import Path

# 导入核心工具
try:
    from frontmatter_utils import DocumentGraphBuilder, format_output
except ImportError:
    # 如果在 scripts/ 目录外运行，尝试添加路径
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))
    from frontmatter_utils import DocumentGraphBuilder, format_output


def generate_graph_visualization(graph: dict, format_type: str = 'mermaid') -> str:
    """
    生成可视化的文档关系图

    Args:
        graph: 文档关系图数据
        format_type: 输出格式 (mermaid, dot, json)

    Returns:
        可视化图表字符串
    """
    if format_type == 'mermaid':
        builder = DocumentGraphBuilder()
        return builder.export_mermaid(graph)

    elif format_type == 'dot':
        # Graphviz DOT 格式
        lines = ['digraph DocumentGraph {']
        lines.append('  rankdir=LR;')
        lines.append('  node [shape=box];')
        lines.append('')

        # 按类型分组节点
        type_colors = {
            'API参考': 'lightblue',
            '技术设计': 'lightgreen',
            '系统集成': 'lightyellow',
            '教程': 'lightpink',
            '故障排查': 'lightgray',
            '架构决策': 'lightcoral'
        }

        for node in graph['nodes']:
            node_id = node['id'].replace('/', '_').replace('.', '_').replace('-', '_')
            label = f"{node['title']}\\n[{node['type']}]"
            color = type_colors.get(node['type'], 'white')
            lines.append(f'  {node_id} [label="{label}", fillcolor="{color}", style=filled];')

        lines.append('')

        # 添加边
        for edge in graph['edges']:
            if edge['type'] == 'document_relation':
                source_id = edge['source'].replace('/', '_').replace('.', '_').replace('-', '_')
                target_id = edge['target'].replace('/', '_').replace('.', '_').replace('-', '_')
                relation = edge['relation_type']
                lines.append(f'  {source_id} -> {target_id} [label="{relation}"];')

        lines.append('}')
        return '\n'.join(lines)

    elif format_type == 'json':
        import json
        return json.dumps(graph, ensure_ascii=False, indent=2)

    else:
        return str(graph)


def analyze_graph_metrics(graph: dict) -> dict:
    """
    分析文档关系图的指标

    Args:
        graph: 文档关系图数据

    Returns:
        分析指标字典
    """
    nodes = graph['nodes']
    edges = graph['edges']

    # 计算入度和出度
    in_degree = {}
    out_degree = {}

    for edge in edges:
        source = edge['source']
        target = edge['target']

        out_degree[source] = out_degree.get(source, 0) + 1
        in_degree[target] = in_degree.get(target, 0) + 1

    # 找出最重要的文档（被引用最多）
    most_referenced = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[:10]

    # 找出最活跃的文档（引用最多）
    most_active = sorted(out_degree.items(), key=lambda x: x[1], reverse=True)[:10]

    # 按类型统计
    type_stats = {}
    for node in nodes:
        node_type = node['type']
        type_stats[node_type] = type_stats.get(node_type, 0) + 1

    return {
        'total_documents': len(nodes),
        'total_relations': len(edges),
        'document_relations': len([e for e in edges if e['type'] == 'document_relation']),
        'code_relations': len([e for e in edges if e['type'] == 'code_relation']),
        'most_referenced_docs': most_referenced,
        'most_active_docs': most_active,
        'documents_by_type': type_stats,
        'average_connections': len(edges) / len(nodes) if nodes else 0
    }


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='文档关系图生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成 Mermaid 图表
  %(prog)s docs/ --format mermaid > docs/graph.mmd

  # 生成 Graphviz DOT 格式
  %(prog)s docs/ --format dot > docs/graph.dot
  dot -Tpng docs/graph.dot -o docs/graph.png

  # 分析文档关系指标
  %(prog)s docs/ --analyze

  # 导出 JSON 数据
  %(prog)s docs/ --format json > docs/graph.json
        """
    )

    parser.add_argument('directory',
                        help='要扫描的文档目录')
    parser.add_argument('--format',
                        choices=['mermaid', 'dot', 'json'],
                        default='mermaid',
                        help='输出格式 (默认: mermaid)')
    parser.add_argument('--analyze',
                        action='store_true',
                        help='分析文档关系指标')
    parser.add_argument('--project-root',
                        default='.',
                        help='项目根目录路径 (默认: 当前目录)')

    args = parser.parse_args()

    try:
        builder = DocumentGraphBuilder(args.project_root)
        graph = builder.build_graph(args.directory)

        if args.analyze:
            metrics = analyze_graph_metrics(graph)
            import json
            print(json.dumps(metrics, ensure_ascii=False, indent=2))
        else:
            output = generate_graph_visualization(graph, args.format)
            print(output)

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
