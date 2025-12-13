"""
Agent Coordinator - 统一的 Agent 协调器

职责:
- 拦截命令执行，自动选择合适的 agent
- 提供 agent 上下文给命令执行
- 记录 agent 使用情况
- 建议下一步协作

使用方式:
    from commands.lib.agent_coordinator import get_agent_coordinator

    coordinator = get_agent_coordinator()
    agent_context = coordinator.intercept(
        task_description="实现用户登录功能",
        command_name="wf_05_code",
        auto_activate=True
    )

    print(coordinator.format_agent_info(agent_context))
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime

from .agent_registry import AgentRegistry, Agent, AgentMatch


class AgentCoordinator:
    """
    统一的 Agent 协调器

    采用单例模式，确保全局只有一个协调器实例。
    负责 agent 选择、上下文管理、使用统计和协作建议。
    """

    _instance: Optional['AgentCoordinator'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.registry = AgentRegistry()
        self.current_agent: Optional[Agent] = None
        self.task_description: str = ""
        self.usage_stats: List[Dict] = []
        self._initialized = True

    def intercept(
        self,
        task_description: str,
        command_name: str,
        auto_activate: bool = True,
        min_confidence: float = 0.85
    ) -> Dict[str, Any]:
        """
        拦截命令执行，选择合适的 agent

        Args:
            task_description: 用户任务描述
            command_name: 当前执行的命令名（如 wf_05_code）
            auto_activate: 是否自动激活
            min_confidence: 最低置信度阈值 (默认 0.85)

        Returns:
            agent_context: {
                'agent': Agent 对象,
                'match_score': 匹配分数,
                'auto_activated': 是否自动激活,
                'alternatives': 备选 agents,
                'mcp_hints': MCP 使用建议,
                'collaborators': 协作建议,
                'command_alignment': 命令对齐检查
            }
        """
        self.task_description = task_description

        # Step 1: 选择 agent
        matches = self.registry.select_agent(task_description, top_k=3)

        if not matches:
            return self._create_fallback_context(command_name)

        best_match: AgentMatch = matches[0]

        # Step 2: 判断是否自动激活
        should_activate = (
            auto_activate and
            best_match.score >= min_confidence
        )

        if should_activate:
            self.current_agent = best_match.agent

        # Step 3: 构建 agent 上下文
        context = {
            'agent': best_match.agent,
            'match_score': best_match.score,
            'auto_activated': should_activate,
            'alternatives': [m.agent for m in matches[1:3]],
            'mcp_hints': self._extract_mcp_hints(best_match.agent),
            'collaborators': self._get_collaborators(best_match.agent),
            'command_alignment': self._check_command_alignment(
                best_match.agent, command_name
            )
        }

        # Step 4: 记录使用
        self._record_usage(context)

        return context

    def _extract_mcp_hints(self, agent: Agent) -> List[Dict[str, Any]]:
        """
        智能提取 MCP 工具推荐（使用 MCPSelector V2 API）

        Args:
            agent: Agent 对象

        Returns:
            List of Dict containing:
                - tool: MCP tool name
                - usage: Tool usage description
                - confidence: Confidence score (0.0-1.0)
                - priority: "high" | "medium" | "low"
                - reason: Recommendation reason
        """
        try:
            # Import MCPSelector and Gateway
            from .mcp_selector import get_mcp_selector
            try:
                from src.mcp.gateway import get_mcp_gateway
                gateway = get_mcp_gateway()
            except ImportError:
                # Gateway not available, create selector without it
                gateway = None

            # Create MCPSelector with gateway
            selector = get_mcp_selector(gateway)

            # Use V2 API for intelligent tool selection
            recommendations = selector.select_tools_v2(
                agent=agent,
                task_description=self.task_description,
                auto_filter=True  # Filter out low-confidence tools
            )

            # Convert MCPToolRecommendation objects to dicts
            return [
                {
                    'tool': rec.tool_name,
                    'usage': rec.usage_description,
                    'confidence': rec.confidence,
                    'priority': rec.priority,
                    'reason': rec.reason
                }
                for rec in recommendations
            ]

        except (ImportError, AttributeError) as e:
            # Fallback to legacy behavior if MCPSelector not available
            return [
                {
                    'tool': mcp['name'],
                    'usage': mcp['usage'],
                    'confidence': 0.5,  # Default confidence
                    'priority': 'medium',
                    'reason': 'Legacy mode - no confidence scoring'
                }
                for mcp in agent.mcp_integrations
            ]

    def _get_collaborators(self, agent: Agent) -> List[Dict[str, str]]:
        """获取协作建议"""
        return self.registry.get_collaborators(agent.name)

    def _check_command_alignment(self, agent: Agent, command_name: str) -> Dict:
        """
        检查 agent 与命令的匹配度

        Returns:
            {
                'aligned': bool - agent 是否推荐当前命令,
                'recommended_tools': List[str] - agent 推荐的工具,
                'note': str - 如果不对齐，提示信息
            }
        """
        # 规范化命令名（支持 wf_05_code 和 /wf_05_code）
        normalized_cmd = command_name.strip('/')
        if not normalized_cmd.startswith('wf_'):
            normalized_cmd = f"wf_{normalized_cmd}"

        # 检查 agent 的 available_tools 是否包含当前命令
        aligned = any(
            f"/{normalized_cmd}" in tool or normalized_cmd in tool
            for tool in agent.available_tools
        )

        return {
            'aligned': aligned,
            'recommended_tools': agent.available_tools,
            'note': '' if aligned else
                    f"Agent 推荐使用 {agent.available_tools[0]} 而非 /{normalized_cmd}"
        }

    def _create_fallback_context(self, command_name: str) -> Dict:
        """无匹配 agent 时的后备上下文"""
        return {
            'agent': None,
            'match_score': 0.0,
            'auto_activated': False,
            'alternatives': [],
            'mcp_hints': [],
            'collaborators': [],
            'command_alignment': {'aligned': True, 'recommended_tools': [], 'note': ''}
        }

    def _record_usage(self, context: Dict) -> None:
        """记录 agent 使用统计"""
        self.usage_stats.append({
            'timestamp': datetime.now().isoformat(),
            'agent': context['agent'].name if context['agent'] else None,
            'score': context['match_score'],
            'auto_activated': context['auto_activated'],
            'task': self.task_description[:100]  # 限制长度
        })

    def format_agent_info(self, context: Dict, verbose: bool = True) -> str:
        """
        格式化 agent 信息输出

        Args:
            context: intercept() 返回的上下文
            verbose: 是否显示详细信息（MCP 提示、协作建议等）

        Returns:
            格式化的 Markdown 字符串
        """
        if not context['agent']:
            return "ℹ️ 未匹配到合适的 agent，使用标准流程\n"

        agent = context['agent']
        score = context['match_score']
        activated = context['auto_activated']

        # 基础信息
        output = [
            "## 🤖 Agent 协助",
            "",
            f"**使用 Agent**: {agent.role} (`{agent.name}`)",
            f"**匹配度**: {score:.0%} {'🟢 自动激活' if activated else '⚪ 建议使用'}",
            f"**专长**: {', '.join(agent.expertise[:3])}",
        ]

        # MCP 集成提示（V2 格式 - 包含置信度和优先级）
        if context['mcp_hints'] and verbose:
            output.extend([
                "",
                "**MCP 工具推荐**:"
            ])

            # Priority emoji mapping
            priority_emoji = {
                "high": "🔴",
                "medium": "🟠",
                "low": "🟡"
            }

            for hint in context['mcp_hints'][:3]:
                # Handle both dict format (V2) and string format (legacy)
                if isinstance(hint, dict):
                    emoji = priority_emoji.get(hint.get('priority', 'medium'), '⚪')
                    confidence = hint.get('confidence', 0.5)
                    tool = hint.get('tool', 'Unknown')
                    usage = hint.get('usage', '')

                    # Format: 🔴 Tool (90%) - Usage
                    output.append(
                        f"  - {emoji} **{tool}** ({confidence:.0%}): {usage}"
                    )
                else:
                    # Legacy string format
                    output.append(f"  - {hint}")

        # 协作建议
        if context['collaborators'] and verbose:
            output.extend([
                "",
                "**建议协作**:",
                *[
                    f"  - {c['mode']}: {c['agent']} ({c['scenario']})"
                    for c in context['collaborators'][:2]
                ]
            ])

        # 命令对齐检查
        if not context['command_alignment']['aligned'] and verbose:
            output.extend([
                "",
                f"⚠️ **注意**: {context['command_alignment']['note']}"
            ])

        # 备选 agents（如果有）
        if context['alternatives'] and verbose:
            output.extend([
                "",
                "**备选 Agents**:",
                *[
                    f"  - {alt.role} (`{alt.name}`)"
                    for alt in context['alternatives'][:2]
                ]
            ])

        output.append("")
        return "\n".join(output)

    def suggest_next_agent(self) -> Optional[str]:
        """
        根据当前 agent 建议下一步协作

        Returns:
            下一步建议的 agent 名称，如果没有建议则返回 None
        """
        if not self.current_agent:
            return None

        collaborators = self.registry.get_collaborators(self.current_agent.name)

        # 优先返回 sequential 模式的协作者
        for collab in collaborators:
            if collab['mode'] == 'sequential':
                return collab['agent']

        return None

    def get_usage_stats(self, limit: int = 10) -> List[Dict]:
        """
        获取 agent 使用统计

        Args:
            limit: 返回最近的 N 条记录

        Returns:
            使用统计列表
        """
        return self.usage_stats[-limit:]

    def format_usage_stats(self, limit: int = 10) -> str:
        """
        格式化使用统计输出

        Args:
            limit: 显示最近的 N 条记录

        Returns:
            格式化的统计信息
        """
        stats = self.get_usage_stats(limit)

        if not stats:
            return "📊 暂无 agent 使用记录\n"

        output = [
            "## 📊 Agent 使用统计",
            "",
            f"**总记录数**: {len(self.usage_stats)}",
            f"**显示最近**: {len(stats)} 条",
            "",
            "| 时间 | Agent | 匹配度 | 激活 | 任务 |",
            "|------|-------|--------|------|------|"
        ]

        for stat in stats:
            timestamp = stat['timestamp'][:19]  # 截取到秒
            agent_name = stat['agent'] or 'N/A'
            score = f"{stat['score']:.0%}" if stat['score'] > 0 else 'N/A'
            activated = '✅' if stat['auto_activated'] else '⚪'
            task = stat['task'][:30] + '...' if len(stat['task']) > 30 else stat['task']

            output.append(f"| {timestamp} | {agent_name} | {score} | {activated} | {task} |")

        output.append("")
        return "\n".join(output)

    def reset(self) -> None:
        """重置协调器状态（用于测试）"""
        self.current_agent = None
        self.task_description = ""
        # 保留 usage_stats 用于统计分析


# 全局单例获取函数
_coordinator: Optional[AgentCoordinator] = None


def get_agent_coordinator() -> AgentCoordinator:
    """
    获取全局 AgentCoordinator 实例

    使用单例模式，确保整个应用只有一个协调器实例。

    Returns:
        AgentCoordinator 实例
    """
    global _coordinator
    if _coordinator is None:
        _coordinator = AgentCoordinator()
    return _coordinator
