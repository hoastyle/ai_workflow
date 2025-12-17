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
        min_confidence: float = 0.65
    ) -> Dict[str, Any]:
        """
        拦截命令执行，选择合适的 agent

        Args:
            task_description: 用户任务描述
            command_name: 当前执行的命令名（如 wf_05_code）
            auto_activate: 是否自动激活
            min_confidence: 最低置信度阈值 (默认 0.65，足以激活推荐的 agent)

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
        # 使用双阈值策略:
        # - min_confidence (默认 0.65): 推荐激活阈值 - Agent 匹配足够好，应该激活
        # - 强制激活阈值 0.85: 完全匹配，无条件激活
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

    def detect_command_conflict(
        self,
        agent: Agent,
        user_command: str
    ) -> Dict[str, Any]:
        """
        检测 Agent 推荐命令与用户执行命令的冲突

        改进 1️⃣: Agent 命令冲突处理
        目的：避免 "Agent 激活但无效" 的现象。Agent 的建议必须被尊重和执行

        Args:
            agent: 激活的 Agent 对象
            user_command: 用户执行的命令（如 wf_04_ask）

        Returns:
            {
                'has_conflict': bool - 是否存在冲突,
                'recommended_command': str - Agent 推荐的命令,
                'user_command': str - 用户执行的命令,
                'match_score': float - Agent 匹配度,
                'alternative_agents': List - 备选 agents,
                'conflict_resolution_options': List[str] - 解决冲突的三个选项
            }
        """
        # 规范化命令名
        normalized_user_cmd = user_command.strip('/').lstrip('wf_')

        # 获取 Agent 推荐的主要工具/命令
        recommended_tools = agent.available_tools
        recommended_cmd = recommended_tools[0] if recommended_tools else None

        # 规范化推荐命令
        if recommended_cmd:
            normalized_recommended = recommended_cmd.strip('/').lstrip('wf_')
        else:
            normalized_recommended = None

        # 检测是否存在冲突
        has_conflict = (
            normalized_recommended and
            normalized_recommended != normalized_user_cmd
        )

        return {
            'has_conflict': has_conflict,
            'recommended_command': recommended_cmd,
            'user_command': user_command,
            'agent_match_score': agent.match_score if hasattr(agent, 'match_score') else 0.0,
            'alternative_agents': [
                {
                    'name': alt['name'],
                    'score': alt['score'],
                    'tools': alt.get('available_tools', [])
                }
                for alt in agent.alternatives if hasattr(agent, 'alternatives')
            ] if hasattr(agent, 'alternatives') else [],
            'conflict_resolution_options': [
                f"1. [推荐] 改用 {recommended_cmd} 进行专业化操作",
                f"2. 继续 {user_command}，采用当前命令的分析视角",
                f"3. 同时执行两个，获得完整的 {recommended_cmd} + {user_command} 分析"
            ] if has_conflict else []
        }

    def extract_mcp_recommendations(
        self,
        agent: Agent,
        mcp_hints: List[Dict[str, Any]],
        enforce: bool = True
    ) -> Dict[str, Any]:
        """
        提取并强制使用 Agent 推荐的 MCP 工具

        改进 2️⃣: MCP 工具强制使用
        目的：使 Agent 的 MCP 推荐真正发挥作用，提升工作流的专业化程度

        Args:
            agent: 激活的 Agent 对象
            mcp_hints: 来自 _extract_mcp_hints 的推荐列表
            enforce: 是否强制使用（默认 True，遵循 Agent 建议）

        Returns:
            {
                'should_enable_mcp': bool - 是否应该启用 MCP,
                'enabled_tools': List[str] - 应该启用的 MCP 工具（按优先级排序），
                'high_priority_tools': List[Dict] - 高优先级工具（必须启用），
                'medium_priority_tools': List[Dict] - 中优先级工具（推荐启用），
                'mcp_justification': str - MCP 使用的理由说明,
                'tool_descriptions': List[str] - 每个工具的使用说明
            }
        """
        if not agent or not mcp_hints:
            return {
                'should_enable_mcp': False,
                'enabled_tools': [],
                'high_priority_tools': [],
                'medium_priority_tools': [],
                'mcp_justification': '无可用的 MCP 工具推荐',
                'tool_descriptions': []
            }

        # 按优先级分类工具
        high_priority = [h for h in mcp_hints if h.get('priority') == 'high']
        medium_priority = [h for h in mcp_hints if h.get('priority') == 'medium']
        low_priority = [h for h in mcp_hints if h.get('priority') == 'low']

        # 确定应该启用的工具（优先级排序）
        # 策略：启用所有高优先级 + 前 2 个中优先级
        enabled_tools = [h['tool'] for h in high_priority]
        enabled_tools.extend([h['tool'] for h in medium_priority[:2]])

        # 构建工具描述列表
        tool_descriptions = []
        all_sorted = high_priority + medium_priority + low_priority

        for tool_hint in all_sorted[:3]:  # 最多展示 3 个工具
            desc = f"- {tool_hint['tool'].upper()}: {tool_hint.get('usage', '未知用途')}"
            tool_descriptions.append(desc)

        # 生成理由说明
        agent_role = agent.role if hasattr(agent, 'role') else '专业 Agent'
        if len(high_priority) > 0:
            mcp_justification = f"{agent_role} 强烈建议使用 MCP 工具进行专业化分析"
        elif len(medium_priority) > 0:
            mcp_justification = f"{agent_role} 推荐使用 MCP 工具以增强分析深度"
        else:
            mcp_justification = f"{agent_role} 可选地使用 MCP 工具"

        return {
            'should_enable_mcp': bool(enabled_tools),
            'enabled_tools': enabled_tools,
            'high_priority_tools': high_priority,
            'medium_priority_tools': medium_priority,
            'mcp_justification': mcp_justification,
            'tool_descriptions': tool_descriptions
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
