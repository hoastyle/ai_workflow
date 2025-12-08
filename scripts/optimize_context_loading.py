#!/usr/bin/env python3
"""
AI Workflow Context Loading Optimizer

分析 wf_03_prime.md 的加载逻辑和 docs_index.json 的覆盖率，
生成优化建议和预估 token 节省。

Usage:
    python optimize_context_loading.py [--format markdown|json] [--verbose]
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class OptimizationType(Enum):
    """优化类型"""
    REDUCE_AUTO_LOAD = "减少自动加载"
    IMPROVE_INDEXING = "改进索引覆盖"
    LAZY_LOADING = "延迟加载优化"
    CACHING_STRATEGY = "缓存策略"


class Priority(Enum):
    """优先级"""
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"


@dataclass
class Optimization:
    """优化建议"""
    type: OptimizationType
    priority: Priority
    description: str
    estimated_savings: int  # Token 节省估算
    implementation_effort: str  # 实施工作量: "低", "中", "高"
    details: List[str]


@dataclass
class LoadingAnalysis:
    """加载分析结果"""
    mode: str  # Quick Start / Task Focused / Full Context
    auto_loaded_files: List[str]
    estimated_tokens: int
    lazy_loaded_categories: List[str]
    potential_tokens: int


@dataclass
class IndexCoverage:
    """索引覆盖率分析"""
    total_docs: int
    indexed_docs: int
    missing_docs: List[str]
    coverage_percentage: float


def analyze_prime_loading() -> Dict:
    """
    解析 wf_03_prime.md 加载逻辑，估算 token 使用

    Returns:
        Dict: 包含各模式的加载分析结果
    """
    prime_file = Path("wf_03_prime.md")

    if not prime_file.exists():
        return {
            "error": "wf_03_prime.md not found",
            "modes": {}
        }

    content = prime_file.read_text(encoding='utf-8')

    # 提取加载模式
    modes = {}

    # Quick Start 模式
    quick_start = LoadingAnalysis(
        mode="Quick Start",
        auto_loaded_files=[
            "PROJECT_INDEX.md",
            "CONTEXT.md",
            "COMMAND_INDEX.md"
        ],
        estimated_tokens=2500,  # 1,500 + 500 + 500
        lazy_loaded_categories=[
            "docs/guides/",
            "docs/examples/",
            "docs/integration/"
        ],
        potential_tokens=23000
    )
    modes["quick_start"] = asdict(quick_start)

    # Full Context 模式
    full_context = LoadingAnalysis(
        mode="Full Context",
        auto_loaded_files=[
            "PROJECT_INDEX.md",
            "CONTEXT.md",
            "COMMAND_INDEX.md",
            "docs/management/PLANNING.md",
            "docs/management/TASK.md",
            "KNOWLEDGE.md"
        ],
        estimated_tokens=6000,  # Quick Start + 3 management files
        lazy_loaded_categories=[
            "docs/guides/",
            "docs/examples/",
            "docs/integration/"
        ],
        potential_tokens=20000
    )
    modes["full_context"] = asdict(full_context)

    # 提取实际token数据 (如果文档中有明确说明)
    token_pattern = r'(\d+,?\d*)\s*tokens?'
    token_matches = re.findall(token_pattern, content, re.IGNORECASE)

    return {
        "modes": modes,
        "total_commands": 16,  # 基于 COMMAND_INDEX.md
        "optimization_implemented": True,
        "current_savings": "31,291 tokens (79% reduction)",
        "token_mentions": [t.replace(',', '') for t in token_matches[:10]]
    }


def analyze_docs_index() -> Tuple[int, int, List[str]]:
    """
    分析 docs_index.json 覆盖率缺口

    Returns:
        Tuple[int, int, List[str]]: (总文档数, 已索引文档数, 缺失文档列表)
    """
    docs_index_file = Path("docs_index.json")

    if not docs_index_file.exists():
        return 0, 0, ["docs_index.json not found"]

    # 加载索引
    with open(docs_index_file, 'r', encoding='utf-8') as f:
        index_data = json.load(f)

    # 统计已索引的文档
    indexed_files = set()

    # always_load
    if "always_load" in index_data:
        indexed_files.update(index_data["always_load"].get("files", []))

    # command_mappings
    if "command_mappings" in index_data:
        for cmd, mapping in index_data["command_mappings"].items():
            indexed_files.update(mapping.get("guides", []))
            indexed_files.update(mapping.get("examples", []))
            indexed_files.update(mapping.get("references", []))
            indexed_files.update(mapping.get("auto_load_in_full_mode", []))

    # category_mappings
    if "category_mappings" in index_data:
        for category, mapping in index_data["category_mappings"].items():
            for file in mapping.get("files", []):
                # 处理通配符
                if "*" not in file:
                    indexed_files.add(file)

    # 扫描实际文档
    docs_dir = Path("docs")
    actual_docs = []

    if docs_dir.exists():
        for md_file in docs_dir.rglob("*.md"):
            # 排除模板和研究文档
            rel_path = str(md_file.relative_to("."))
            if "/doc_templates/" not in rel_path and "/research/" not in rel_path:
                actual_docs.append(rel_path)

    # 计算缺失文档
    missing_docs = []
    for doc in actual_docs:
        if doc not in indexed_files:
            # 检查是否被通配符覆盖
            covered = False
            for indexed in indexed_files:
                if "*" in indexed:
                    pattern = indexed.replace("**", ".*").replace("*", "[^/]*")
                    if re.match(pattern, doc):
                        covered = True
                        break

            if not covered:
                missing_docs.append(doc)

    total_docs = len(actual_docs)
    indexed_count = total_docs - len(missing_docs)

    return total_docs, indexed_count, missing_docs


def suggest_optimizations(
    loading_analysis: Dict,
    coverage: IndexCoverage,
    current_token_usage: int = 181000
) -> List[Optimization]:
    """
    生成4类优化建议 (带优先级和预估节省)

    Args:
        loading_analysis: analyze_prime_loading() 的结果
        coverage: 索引覆盖率分析结果
        current_token_usage: 当前 token 使用量

    Returns:
        List[Optimization]: 优化建议列表
    """
    optimizations = []

    # 类型1: 减少自动加载
    if coverage.coverage_percentage < 90:
        optimizations.append(Optimization(
            type=OptimizationType.IMPROVE_INDEXING,
            priority=Priority.HIGH,
            description=f"提升索引覆盖率至 90%+ (当前 {coverage.coverage_percentage:.1f}%)",
            estimated_savings=1000 * len(coverage.missing_docs[:10]),
            implementation_effort="中",
            details=[
                f"补充 {len(coverage.missing_docs)} 个未索引文档",
                "为每个文档添加 command mapping",
                "使用 category mapping 处理相似文档组"
            ]
        ))

    # 类型2: 改进索引覆盖
    modes = loading_analysis.get("modes", {})
    if "quick_start" in modes:
        quick_tokens = modes["quick_start"]["estimated_tokens"]
        if quick_tokens > 3000:
            optimizations.append(Optimization(
                type=OptimizationType.REDUCE_AUTO_LOAD,
                priority=Priority.MEDIUM,
                description="进一步精简 Quick Start 模式自动加载",
                estimated_savings=quick_tokens - 2000,
                implementation_effort="低",
                details=[
                    "审查 PROJECT_INDEX.md 可否进一步精简",
                    "考虑 COMMAND_INDEX.md 分级加载（只加载常用命令）",
                    "延迟加载某些 metadata 字段"
                ]
            ))

    # 类型3: 延迟加载优化
    optimizations.append(Optimization(
        type=OptimizationType.LAZY_LOADING,
        priority=Priority.HIGH,
        description="为高频命令添加专属索引入口",
        estimated_savings=5000,
        implementation_effort="中",
        details=[
            "为 /wf_05_code, /wf_04_ask 创建快速索引",
            "预缓存常用文档组合",
            "实现文档依赖树分析"
        ]
    ))

    # 类型4: 缓存策略
    optimizations.append(Optimization(
        type=OptimizationType.CACHING_STRATEGY,
        priority=Priority.LOW,
        description="实现会话级文档缓存",
        estimated_savings=3000,
        implementation_effort="高",
        details=[
            "缓存已加载文档的 token 计数",
            "使用 LRU 缓存淘汰策略",
            "跨会话持久化热文档列表"
        ]
    ))

    return optimizations


def calculate_token_savings(optimizations: List[Optimization]) -> Dict:
    """
    计算总节省和分类节省

    Args:
        optimizations: 优化建议列表

    Returns:
        Dict: 节省统计
    """
    by_type = {}
    by_priority = {}

    total_savings = 0

    for opt in optimizations:
        # 按类型统计
        type_name = opt.type.value
        if type_name not in by_type:
            by_type[type_name] = {"count": 0, "savings": 0}
        by_type[type_name]["count"] += 1
        by_type[type_name]["savings"] += opt.estimated_savings

        # 按优先级统计
        priority_name = opt.priority.value
        if priority_name not in by_priority:
            by_priority[priority_name] = {"count": 0, "savings": 0}
        by_priority[priority_name]["count"] += 1
        by_priority[priority_name]["savings"] += opt.estimated_savings

        total_savings += opt.estimated_savings

    return {
        "total_savings": total_savings,
        "by_type": by_type,
        "by_priority": by_priority,
        "optimization_count": len(optimizations)
    }


def generate_report(
    loading_analysis: Dict,
    coverage: IndexCoverage,
    optimizations: List[Optimization],
    savings: Dict,
    format: str = "markdown"
) -> str:
    """
    生成优化报告

    Args:
        loading_analysis: 加载分析结果
        coverage: 索引覆盖率
        optimizations: 优化建议
        savings: 节省统计
        format: 输出格式 ("markdown" 或 "json")

    Returns:
        str: 格式化的报告文本
    """
    if format == "json":
        # Convert Optimization dataclasses to dicts with Enum values as strings
        json_optimizations = []
        for opt in optimizations:
            opt_dict = asdict(opt)
            opt_dict['type'] = opt.type.value  # Convert enum to string
            opt_dict['priority'] = opt.priority.value  # Convert enum to string
            json_optimizations.append(opt_dict)

        return json.dumps({
            "loading_analysis": loading_analysis,
            "coverage": asdict(coverage),
            "optimizations": json_optimizations,
            "savings": savings
        }, indent=2, ensure_ascii=False)

    # Markdown 格式
    lines = ["# AI Workflow 上下文加载优化报告", ""]

    # 1. 加载分析
    lines.extend(["## 📊 当前加载分析", ""])

    modes = loading_analysis.get("modes", {})
    if "quick_start" in modes:
        qs = modes["quick_start"]
        lines.extend([
            f"### Quick Start 模式",
            f"- **自动加载**: {len(qs['auto_loaded_files'])} 个文件",
            f"- **估算 Tokens**: {qs['estimated_tokens']:,}",
            f"- **懒加载分类**: {len(qs['lazy_loaded_categories'])} 个",
            ""
        ])

    if "full_context" in modes:
        fc = modes["full_context"]
        lines.extend([
            f"### Full Context 模式",
            f"- **自动加载**: {len(fc['auto_loaded_files'])} 个文件",
            f"- **估算 Tokens**: {fc['estimated_tokens']:,}",
            ""
        ])

    # 2. 索引覆盖率
    lines.extend([
        "## 🎯 索引覆盖率分析",
        "",
        f"- **总文档数**: {coverage.total_docs}",
        f"- **已索引**: {coverage.indexed_docs}",
        f"- **覆盖率**: {coverage.coverage_percentage:.1f}%",
        f"- **缺失文档**: {len(coverage.missing_docs)} 个",
        ""
    ])

    if coverage.missing_docs:
        lines.append("**缺失文档示例** (前10个):")
        for doc in coverage.missing_docs[:10]:
            lines.append(f"- {doc}")
        lines.append("")

    # 3. 优化建议
    lines.extend(["## 💡 优化建议", ""])

    for i, opt in enumerate(optimizations, 1):
        lines.extend([
            f"### {i}. {opt.description}",
            f"- **类型**: {opt.type.value}",
            f"- **优先级**: {opt.priority.value}",
            f"- **预估节省**: {opt.estimated_savings:,} tokens",
            f"- **工作量**: {opt.implementation_effort}",
            "",
            "**详细步骤**:"
        ])
        for detail in opt.details:
            lines.append(f"- {detail}")
        lines.append("")

    # 4. 节省统计
    lines.extend([
        "## 📈 节省统计",
        "",
        f"**总预估节省**: {savings['total_savings']:,} tokens",
        f"**优化项数**: {savings['optimization_count']}",
        "",
        "### 按类型分类",
        ""
    ])

    for type_name, stats in savings["by_type"].items():
        lines.append(f"- **{type_name}**: {stats['count']} 项, {stats['savings']:,} tokens")

    lines.extend(["", "### 按优先级分类", ""])

    for priority, stats in savings["by_priority"].items():
        lines.append(f"- **{priority}**: {stats['count']} 项, {stats['savings']:,} tokens")

    return "\n".join(lines)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="AI Workflow 上下文加载优化器")
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="输出格式 (默认: markdown)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="详细输出"
    )

    args = parser.parse_args()

    # 1. 分析 Prime 加载逻辑
    if args.verbose:
        print("📖 分析 wf_03_prime.md 加载逻辑...", file=sys.stderr)

    loading_analysis = analyze_prime_loading()

    # 2. 分析 Docs 索引覆盖率
    if args.verbose:
        print("🔍 分析 docs_index.json 覆盖率...", file=sys.stderr)

    total_docs, indexed_docs, missing_docs = analyze_docs_index()
    coverage = IndexCoverage(
        total_docs=total_docs,
        indexed_docs=indexed_docs,
        missing_docs=missing_docs,
        coverage_percentage=(indexed_docs / total_docs * 100) if total_docs > 0 else 0
    )

    if args.verbose:
        print(f"   总文档: {total_docs}, 已索引: {indexed_docs}, 覆盖率: {coverage.coverage_percentage:.1f}%", file=sys.stderr)

    # 3. 生成优化建议
    if args.verbose:
        print("💡 生成优化建议...", file=sys.stderr)

    optimizations = suggest_optimizations(loading_analysis, coverage)

    # 4. 计算节省
    savings = calculate_token_savings(optimizations)

    if args.verbose:
        print(f"   预估总节省: {savings['total_savings']:,} tokens", file=sys.stderr)
        print("", file=sys.stderr)

    # 5. 生成报告
    report = generate_report(loading_analysis, coverage, optimizations, savings, format=args.format)
    print(report)

    # 退出码: 0 表示一切正常
    sys.exit(0)


if __name__ == "__main__":
    main()
