#!/usr/bin/env python3
"""
AI Workflow Command Compatibility Validator

检测当前环境版本和MCP可用性，验证14个命令的兼容性状态。
支持Markdown和JSON双格式输出，CI/CD友好的退出码。

Usage:
    python validate_command_compatibility.py [--format markdown|json] [--verbose]
"""

import sys
import json
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class CompatibilityStatus(Enum):
    """命令兼容性状态"""
    FULL = "FULL"          # 完全可用 (100%)
    LIMITED = "LIMITED"    # 功能降级 (50-80%)
    UNAVAILABLE = "UNAVAILABLE"  # 不可用 (0-30%)


class Tier(Enum):
    """命令分层"""
    TIER_1 = 1  # 完全兼容 (无MCP依赖)
    TIER_2 = 2  # 功能降级 (可选MCP)
    TIER_3 = 3  # 受限/不可用 (强依赖MCP)


@dataclass
class CommandDefinition:
    """命令定义"""
    name: str
    description: str
    tier: Tier
    required_mcps: List[str]  # 必需的MCP (缺失则UNAVAILABLE)
    optional_mcps: List[str]  # 可选的MCP (缺失则LIMITED)


@dataclass
class CommandCompatibility:
    """命令兼容性结果"""
    name: str
    status: CompatibilityStatus
    tier: int
    available_mcps: List[str]
    missing_mcps: List[str]
    functionality_percentage: int  # 功能可用百分比


def detect_environment_version() -> Tuple[str, str]:
    """
    检测环境版本

    Returns:
        Tuple[str, str]: (版本号, 兼容性描述)

    版本判断逻辑:
        v1.7: COMMAND_INDEX.md + src/mcp/gateway.py + commands/lib/agent_registry.py
        v1.6: src/mcp/gateway.py 存在
        v1.3-v1.5: docs_index.json 存在
        v1.0-v1.2: 以上都不存在
    """
    markers = {
        "command_index": Path("COMMAND_INDEX.md"),
        "mcp_gateway": Path("src/mcp/gateway.py"),
        "agent_registry": Path("commands/lib/agent_registry.py"),
        "docs_index": Path("docs_index.json")
    }

    if (markers["command_index"].exists() and
        markers["mcp_gateway"].exists() and
        markers["agent_registry"].exists()):
        return "v1.7", "完全兼容"
    elif markers["mcp_gateway"].exists():
        return "v1.6", "大部分兼容"
    elif markers["docs_index"].exists():
        return "v1.3-v1.5", "基础兼容"
    else:
        return "v1.0-v1.2", "受限兼容"


def detect_mcp_servers() -> Dict[str, bool]:
    """
    检测6个MCP服务器可用性

    Returns:
        Dict[str, bool]: MCP名称 -> 是否可用

    使用 importlib.util.find_spec() 进行Python模块检测
    """
    mcp_servers = [
        "mcp_sequential_thinking",  # v1.5+
        "mcp_context7",              # v1.4+
        "mcp_serena",                # v1.6+
        "mcp_tavily",                # v1.4+
        "mcp_magic",                 # v1.7+
        "mcp_playwright"             # v1.7+
    ]

    return {
        mcp: importlib.util.find_spec(mcp) is not None
        for mcp in mcp_servers
    }


def load_command_definitions() -> List[CommandDefinition]:
    """
    加载14个命令定义

    Returns:
        List[CommandDefinition]: 14个命令的完整定义

    分层说明:
        Tier 1 (3个): 无MCP依赖, 100%兼容
        Tier 2 (9个): 可选MCP, 降级50-80%
        Tier 3 (2个): 强依赖MCP, 0-30%可用
    """
    return [
        # Tier 1: 完全兼容 (3个) - 无MCP依赖
        CommandDefinition(
            name="wf_01_planning",
            description="项目规划",
            tier=Tier.TIER_1,
            required_mcps=[],
            optional_mcps=[]  # Tier 1 无MCP依赖
        ),
        CommandDefinition(
            name="wf_02_task",
            description="任务追踪",
            tier=Tier.TIER_1,
            required_mcps=[],
            optional_mcps=[]  # Tier 1 无MCP依赖
        ),
        CommandDefinition(
            name="wf_11_commit",
            description="Git提交",
            tier=Tier.TIER_1,
            required_mcps=[],
            optional_mcps=[]  # Tier 1 无MCP依赖
        ),

        # Tier 2: 功能降级 (9个)
        CommandDefinition(
            name="wf_03_prime",
            description="上下文加载",
            tier=Tier.TIER_2,
            required_mcps=[],
            optional_mcps=["mcp_serena"]
        ),
        CommandDefinition(
            name="wf_04_ask",
            description="架构咨询",
            tier=Tier.TIER_2,
            required_mcps=[],
            optional_mcps=["mcp_sequential_thinking", "mcp_context7", "mcp_tavily"]
        ),
        CommandDefinition(
            name="wf_04_research",
            description="技术研究",
            tier=Tier.TIER_2,
            required_mcps=[],
            optional_mcps=["mcp_context7", "mcp_tavily"]
        ),
        CommandDefinition(
            name="wf_05_code",
            description="功能实现",
            tier=Tier.TIER_2,
            required_mcps=[],
            optional_mcps=["mcp_serena", "mcp_magic"]
        ),
        CommandDefinition(
            name="wf_06_debug",
            description="调试修复",
            tier=Tier.TIER_2,
            required_mcps=[],
            optional_mcps=["mcp_sequential_thinking", "mcp_serena"]
        ),
        CommandDefinition(
            name="wf_07_test",
            description="测试开发",
            tier=Tier.TIER_2,
            required_mcps=[],
            optional_mcps=["mcp_serena", "mcp_sequential_thinking"]
        ),
        CommandDefinition(
            name="wf_08_review",
            description="代码审查",
            tier=Tier.TIER_2,
            required_mcps=[],
            optional_mcps=["mcp_serena", "mcp_sequential_thinking"]
        ),
        CommandDefinition(
            name="wf_09_refactor",
            description="代码重构",
            tier=Tier.TIER_2,
            required_mcps=[],
            optional_mcps=["mcp_serena"]
        ),
        CommandDefinition(
            name="wf_10_optimize",
            description="性能优化",
            tier=Tier.TIER_2,
            required_mcps=[],
            optional_mcps=["mcp_serena"]
        ),

        # Tier 3: 受限/不可用 (2个)
        CommandDefinition(
            name="wf_12_deploy_check",
            description="部署检查",
            tier=Tier.TIER_3,
            required_mcps=["mcp_playwright"],
            optional_mcps=[]
        ),
        CommandDefinition(
            name="wf_14_doc",
            description="文档生成",
            tier=Tier.TIER_3,
            required_mcps=["mcp_magic"],
            optional_mcps=[]
        ),
    ]


def validate_command(cmd_def: CommandDefinition, available_mcps: Dict[str, bool]) -> CommandCompatibility:
    """
    验证单个命令的兼容性

    Args:
        cmd_def: 命令定义
        available_mcps: MCP可用性字典

    Returns:
        CommandCompatibility: 兼容性结果

    判断逻辑:
        - 缺失required_mcps中任一MCP → UNAVAILABLE (0-30%)
        - 所有optional_mcps都缺失 → LIMITED (50-80%)
        - 至少有1个optional_mcp → LIMITED (70-90%)
        - 无MCP依赖或全部可用 → FULL (100%)
    """
    # 检查required MCPs
    missing_required = [
        mcp for mcp in cmd_def.required_mcps
        if not available_mcps.get(mcp, False)
    ]

    # 检查optional MCPs
    missing_optional = [
        mcp for mcp in cmd_def.optional_mcps
        if not available_mcps.get(mcp, False)
    ]

    available_mcps_list = [
        mcp for mcp in (cmd_def.required_mcps + cmd_def.optional_mcps)
        if available_mcps.get(mcp, False)
    ]

    # 状态判断
    if missing_required:
        # 缺少必需MCP
        status = CompatibilityStatus.UNAVAILABLE
        functionality = 20  # 0-30%范围
    elif not cmd_def.optional_mcps:
        # 无MCP依赖
        status = CompatibilityStatus.FULL
        functionality = 100
    elif not missing_optional:
        # 所有可选MCP都可用
        status = CompatibilityStatus.FULL
        functionality = 100
    elif available_mcps_list:
        # 部分可选MCP可用
        status = CompatibilityStatus.LIMITED
        available_ratio = len(available_mcps_list) / len(cmd_def.optional_mcps)
        functionality = int(50 + available_ratio * 40)  # 50-90%范围
    else:
        # 所有可选MCP都缺失
        status = CompatibilityStatus.LIMITED
        functionality = 60  # 50-80%范围

    return CommandCompatibility(
        name=cmd_def.name,
        status=status,
        tier=cmd_def.tier.value,
        available_mcps=available_mcps_list,
        missing_mcps=missing_required + missing_optional,
        functionality_percentage=functionality
    )


def generate_report(results: List[CommandCompatibility], format: str = "markdown") -> str:
    """
    生成兼容性报告

    Args:
        results: 兼容性结果列表
        format: 输出格式 ("markdown" 或 "json")

    Returns:
        str: 格式化的报告文本
    """
    if format == "json":
        # Convert CompatibilityStatus enum to string for JSON serialization
        json_results = []
        for r in results:
            r_dict = asdict(r)
            r_dict['status'] = r.status.value  # Convert enum to string
            json_results.append(r_dict)

        return json.dumps(
            json_results,
            indent=2,
            ensure_ascii=False
        )

    # Markdown 格式
    lines = ["# AI Workflow 命令兼容性报告", ""]

    # 环境信息
    version, compat = detect_environment_version()
    mcp_status = detect_mcp_servers()
    available_count = sum(1 for v in mcp_status.values() if v)

    lines.extend([
        f"**环境版本**: {version} ({compat})",
        f"**MCP 可用性**: {available_count}/6",
        ""
    ])

    # 统计信息
    status_counts = {
        CompatibilityStatus.FULL: 0,
        CompatibilityStatus.LIMITED: 0,
        CompatibilityStatus.UNAVAILABLE: 0
    }
    for r in results:
        status_counts[r.status] += 1

    lines.extend([
        "## 总体统计",
        "",
        f"- ✅ 完全可用 (FULL): {status_counts[CompatibilityStatus.FULL]}/14",
        f"- 🟡 功能降级 (LIMITED): {status_counts[CompatibilityStatus.LIMITED]}/14",
        f"- 🔴 不可用 (UNAVAILABLE): {status_counts[CompatibilityStatus.UNAVAILABLE]}/14",
        ""
    ])

    # 按Tier分组
    tier_groups = {1: [], 2: [], 3: []}
    for r in results:
        tier_groups[r.tier].append(r)

    lines.extend(["## 命令兼容性详情", ""])

    for tier in [1, 2, 3]:
        tier_name = {1: "Tier 1: 完全兼容", 2: "Tier 2: 功能降级", 3: "Tier 3: 受限/不可用"}[tier]
        lines.extend([f"### {tier_name}", ""])

        if not tier_groups[tier]:
            lines.extend(["无命令", ""])
            continue

        lines.append("| 命令 | 状态 | 功能可用性 | 可用MCP | 缺失MCP |")
        lines.append("|------|------|-----------|---------|---------|")

        for r in sorted(tier_groups[tier], key=lambda x: x.name):
            status_icon = {
                CompatibilityStatus.FULL: "✅",
                CompatibilityStatus.LIMITED: "🟡",
                CompatibilityStatus.UNAVAILABLE: "🔴"
            }[r.status]

            available_str = ", ".join(r.available_mcps) if r.available_mcps else "-"
            missing_str = ", ".join(r.missing_mcps) if r.missing_mcps else "-"

            lines.append(
                f"| {r.name} | {status_icon} {r.status.value} | "
                f"{r.functionality_percentage}% | {available_str} | {missing_str} |"
            )

        lines.append("")

    return "\n".join(lines)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="AI Workflow 命令兼容性验证")
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="输出格式 (默认: markdown)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="详细输出 (包含MCP检测详情)"
    )

    args = parser.parse_args()

    # 检测环境
    version, compat = detect_environment_version()
    mcp_status = detect_mcp_servers()

    if args.verbose:
        print(f"环境版本: {version} ({compat})", file=sys.stderr)
        print(f"MCP 检测结果:", file=sys.stderr)
        for mcp, available in mcp_status.items():
            status = "✅" if available else "❌"
            print(f"  {status} {mcp}", file=sys.stderr)
        print("", file=sys.stderr)

    # 加载命令定义
    commands = load_command_definitions()

    # 验证每个命令
    results = [validate_command(cmd, mcp_status) for cmd in commands]

    # 生成报告
    report = generate_report(results, format=args.format)
    print(report)

    # CI/CD 友好退出码
    # 0: 所有命令完全可用
    # 1: 有命令功能降级或不可用
    status_counts = {r.status for r in results}
    if status_counts == {CompatibilityStatus.FULL}:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
