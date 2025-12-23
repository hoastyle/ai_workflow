"""
Multi-Agent Orchestrator - 多 Agent 协调器

负责处理复杂任务中的多个 Agent 协作场景。

核心功能:
- 分析任务，识别需要的多个 Agents
- 解决 Agent 之间的冲突
- 分析命令依赖关系
- 编排顺序/并行执行策略
- 协调多个 Agent 的输出

Phase 2.4 实现
"""

from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
from pathlib import Path

from .agent_registry import Agent, AgentRegistry, AgentMatch
from .agent_decision_engine import AgentDecisionEngine, DecisionResult
from .agent_command_executor import AgentCommandExecutor, ExecutionResult

logger = logging.getLogger(__name__)


class ExecutionMode(Enum):
    """执行模式"""
    SEQUENTIAL = "sequential"  # 顺序执行
    PARALLEL = "parallel"      # 并行执行
    HIERARCHICAL = "hierarchical"  # 层级执行（主 Agent 协调子 Agents）


class ConflictResolutionStrategy(Enum):
    """冲突解决策略"""
    HIGHEST_SCORE = "highest_score"  # 选择评分最高的 Agent
    USER_CHOICE = "user_choice"      # 让用户选择
    MERGE_ALL = "merge_all"          # 合并所有 Agents 的建议
    PRIORITY_BASED = "priority_based"  # 基于优先级


@dataclass
class AgentTask:
    """Agent 任务描述"""
    agent: Agent
    command: str
    task_description: str
    dependencies: List[str] = field(default_factory=list)  # 依赖的其他 Agent ID
    execution_order: int = 0  # 执行顺序（0 表示并行）

    @property
    def agent_id(self) -> str:
        """获取 Agent 唯一标识"""
        return self.agent.name


@dataclass
class OrchestrationPlan:
    """编排计划"""
    tasks: List[AgentTask]
    execution_mode: ExecutionMode
    conflict_resolution: ConflictResolutionStrategy
    estimated_duration: str = "unknown"

    def get_parallel_tasks(self) -> List[List[AgentTask]]:
        """获取并行任务组（按 execution_order 分组）"""
        if self.execution_mode != ExecutionMode.PARALLEL:
            return [[task] for task in self.tasks]

        # 按 execution_order 分组
        groups: Dict[int, List[AgentTask]] = {}
        for task in self.tasks:
            order = task.execution_order
            if order not in groups:
                groups[order] = []
            groups[order].append(task)

        # 按顺序返回
        return [groups[order] for order in sorted(groups.keys())]

    def get_sequential_tasks(self) -> List[AgentTask]:
        """获取顺序任务列表（按 execution_order 排序）"""
        return sorted(self.tasks, key=lambda t: t.execution_order)


@dataclass
class OrchestrationResult:
    """编排执行结果"""
    success: bool
    results: List[ExecutionResult]
    plan: OrchestrationPlan
    conflicts_resolved: int = 0
    total_duration: float = 0.0
    error_message: str = ""


class MultiAgentOrchestrator:
    """
    多 Agent 协调器

    处理复杂任务场景中的多个 Agent 协作：
    1. 识别任务需要的所有 Agents
    2. 解决 Agents 之间的冲突
    3. 分析依赖关系
    4. 选择执行策略（顺序/并行/层级）
    5. 编排和执行
    """

    def __init__(self, registry: Optional[AgentRegistry] = None):
        """
        初始化协调器

        Args:
            registry: Agent 注册表（可选，默认创建新实例）
        """
        self.registry = registry or AgentRegistry()
        self.decision_engine = AgentDecisionEngine()
        self.executor = AgentCommandExecutor()
        self.orchestration_history: List[OrchestrationResult] = []

    def analyze_task_complexity(self, task_description: str) -> Dict[str, any]:
        """
        分析任务复杂度，判断是否需要多个 Agents

        Args:
            task_description: 任务描述

        Returns:
            {
                'needs_multiple_agents': bool,
                'estimated_agents_count': int,
                'suggested_agents': List[str],
                'complexity_score': float (0.0-1.0)
            }
        """
        # 1. 查找所有可能的 Agents
        all_matches = self.registry.find_agents(task_description)

        # 2. 过滤高置信度的 Agents (>= 65%)
        qualified_agents = [
            match for match in all_matches
            if match.score >= 0.65
        ]

        # 3. 分析关键词多样性
        keywords_found = set()
        for match in qualified_agents:
            keywords_found.update(match.matched_keywords)

        # 4. 计算复杂度评分
        complexity_score = min(
            len(qualified_agents) * 0.2 +  # 多个高分 Agent
            len(keywords_found) * 0.05,     # 关键词多样性
            1.0
        )

        needs_multiple = (
            len(qualified_agents) >= 2 and  # 至少2个合格 Agent
            complexity_score >= 0.4          # 复杂度足够
        )

        return {
            'needs_multiple_agents': needs_multiple,
            'estimated_agents_count': len(qualified_agents),
            'suggested_agents': [match.agent.name for match in qualified_agents],
            'complexity_score': complexity_score,
            'all_matches': qualified_agents
        }

    def resolve_conflicts(
        self,
        candidates: List[AgentMatch],
        strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.HIGHEST_SCORE
    ) -> List[Agent]:
        """
        解决 Agent 冲突，选择最合适的 Agents

        Args:
            candidates: 候选 Agents
            strategy: 冲突解决策略

        Returns:
            选中的 Agents 列表
        """
        if len(candidates) <= 1:
            return [c.agent for c in candidates]

        if strategy == ConflictResolutionStrategy.HIGHEST_SCORE:
            # 选择评分最高的 Agent
            best = max(candidates, key=lambda c: c.score)
            return [best.agent]

        elif strategy == ConflictResolutionStrategy.PRIORITY_BASED:
            # 按优先级排序，选择前N个
            priority_map = {'high': 3, 'medium': 2, 'low': 1}
            sorted_candidates = sorted(
                candidates,
                key=lambda c: (
                    priority_map.get(c.agent.priority, 0),
                    c.score
                ),
                reverse=True
            )
            # 返回前3个或所有高优先级的
            high_priority = [
                c.agent for c in sorted_candidates[:3]
                if c.agent.priority == 'high'
            ]
            return high_priority if high_priority else [sorted_candidates[0].agent]

        elif strategy == ConflictResolutionStrategy.MERGE_ALL:
            # 保留所有合格的 Agents
            return [c.agent for c in candidates]

        else:  # USER_CHOICE
            # 用户选择（由调用方处理）
            return [c.agent for c in candidates]

    def analyze_dependencies(self, agents: List[Agent]) -> Dict[str, List[str]]:
        """
        分析 Agents 之间的依赖关系

        Args:
            agents: Agents 列表

        Returns:
            依赖图: {agent_id: [依赖的 agent_ids]}
        """
        dependency_graph: Dict[str, List[str]] = {}

        for agent in agents:
            agent_id = agent.name
            dependency_graph[agent_id] = []

            # 检查协作模式中的依赖
            for collab in agent.collaboration_modes:
                if collab['mode'] == 'sequential':
                    # 顺序协作意味着可能有依赖
                    dep_agent_id = collab['agent']
                    # 检查这个 agent 是否在当前列表中
                    if any(a.name == dep_agent_id for a in agents):
                        dependency_graph[agent_id].append(dep_agent_id)

        return dependency_graph

    def determine_execution_mode(
        self,
        agents: List[Agent],
        dependencies: Dict[str, List[str]]
    ) -> ExecutionMode:
        """
        确定执行模式

        Args:
            agents: Agents 列表
            dependencies: 依赖图

        Returns:
            执行模式
        """
        # 1. 检查是否有主协调 Agent（如 pm-agent）
        has_coordinator = any(
            'coordinator' in agent.role.lower() or
            'manager' in agent.role.lower()
            for agent in agents
        )

        # 检查是否有层级协作模式
        has_hierarchical_collab = any(
            any(collab.get('mode') == 'hierarchical' for collab in agent.collaboration_modes)
            for agent in agents
        )

        if has_coordinator or has_hierarchical_collab:
            # 有协调者或层级协作，使用层级模式
            return ExecutionMode.HIERARCHICAL

        # 2. 检查是否有依赖关系
        has_dependencies = any(deps for deps in dependencies.values())

        if not has_dependencies:
            # 无依赖，可以并行
            return ExecutionMode.PARALLEL

        # 3. 有依赖但无协调者，使用顺序模式
        return ExecutionMode.SEQUENTIAL

    def create_orchestration_plan(
        self,
        task_description: str,
        command_name: str,
        conflict_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.HIGHEST_SCORE
    ) -> OrchestrationPlan:
        """
        创建编排计划

        Args:
            task_description: 任务描述
            command_name: 命令名称
            conflict_strategy: 冲突解决策略

        Returns:
            编排计划
        """
        # 1. 分析任务复杂度
        complexity_analysis = self.analyze_task_complexity(task_description)

        if not complexity_analysis['needs_multiple_agents']:
            # 简单任务，单 Agent 处理
            best_match = complexity_analysis['all_matches'][0] if complexity_analysis['all_matches'] else None
            if not best_match:
                raise ValueError(f"No suitable agent found for task: {task_description}")

            task = AgentTask(
                agent=best_match.agent,
                command=command_name,
                task_description=task_description,
                execution_order=0
            )

            return OrchestrationPlan(
                tasks=[task],
                execution_mode=ExecutionMode.SEQUENTIAL,
                conflict_resolution=conflict_strategy,
                estimated_duration="5-15 minutes"
            )

        # 2. 解决冲突，选择 Agents
        selected_agents = self.resolve_conflicts(
            complexity_analysis['all_matches'],
            conflict_strategy
        )

        # 3. 分析依赖
        dependencies = self.analyze_dependencies(selected_agents)

        # 4. 确定执行模式
        execution_mode = self.determine_execution_mode(selected_agents, dependencies)

        # 5. 创建任务列表
        tasks = []
        execution_order = 0

        if execution_mode == ExecutionMode.SEQUENTIAL:
            # 顺序执行：按依赖关系排序
            sorted_agents = self._topological_sort(selected_agents, dependencies)
            for i, agent in enumerate(sorted_agents):
                task = AgentTask(
                    agent=agent,
                    command=self._infer_command_for_agent(agent, command_name),
                    task_description=task_description,
                    dependencies=dependencies.get(agent.name, []),
                    execution_order=i
                )
                tasks.append(task)

        elif execution_mode == ExecutionMode.PARALLEL:
            # 并行执行：所有 Agent 同时开始
            for agent in selected_agents:
                task = AgentTask(
                    agent=agent,
                    command=self._infer_command_for_agent(agent, command_name),
                    task_description=task_description,
                    execution_order=0  # 所有都是0，表示并行
                )
                tasks.append(task)

        else:  # HIERARCHICAL
            # 层级执行：主 Agent 在最前，其他并行
            coordinator = next(
                (a for a in selected_agents if 'coordinator' in a.role.lower() or 'manager' in a.role.lower()),
                selected_agents[0]
            )
            workers = [a for a in selected_agents if a != coordinator]

            # 主 Agent 先执行
            tasks.append(AgentTask(
                agent=coordinator,
                command=self._infer_command_for_agent(coordinator, command_name),
                task_description=task_description,
                execution_order=0
            ))

            # 工作 Agents 并行执行
            for agent in workers:
                tasks.append(AgentTask(
                    agent=agent,
                    command=self._infer_command_for_agent(agent, command_name),
                    task_description=task_description,
                    dependencies=[coordinator.name],
                    execution_order=1
                ))

        return OrchestrationPlan(
            tasks=tasks,
            execution_mode=execution_mode,
            conflict_resolution=conflict_strategy,
            estimated_duration=self._estimate_duration(len(tasks), execution_mode)
        )

    def _topological_sort(
        self,
        agents: List[Agent],
        dependencies: Dict[str, List[str]]
    ) -> List[Agent]:
        """
        拓扑排序 Agents（处理依赖关系）

        Returns:
            排序后的 Agents 列表
        """
        # 简化实现：Kahn's 算法
        in_degree = {agent.name: 0 for agent in agents}
        agent_map = {agent.name: agent for agent in agents}

        # 计算入度
        for agent_id, deps in dependencies.items():
            for dep in deps:
                if dep in in_degree:
                    in_degree[agent_id] += 1

        # 找到所有入度为0的节点
        queue = [agent_id for agent_id, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            agent_id = queue.pop(0)
            result.append(agent_map[agent_id])

            # 减少依赖此节点的其他节点的入度
            for other_id, deps in dependencies.items():
                if agent_id in deps:
                    in_degree[other_id] -= 1
                    if in_degree[other_id] == 0:
                        queue.append(other_id)

        # 如果有环，返回原始顺序
        if len(result) != len(agents):
            logger.warning("Circular dependency detected, using original order")
            return agents

        return result

    def _infer_command_for_agent(self, agent: Agent, default_command: str) -> str:
        """推断 Agent 应该使用的命令"""
        # 使用 Agent 的 available_tools 中的第一个 wf_ 命令
        for tool in agent.available_tools:
            if tool.startswith('/wf_'):
                return tool[1:]  # 去掉前缀 /
        return default_command

    def _estimate_duration(self, task_count: int, mode: ExecutionMode) -> str:
        """估算执行时间"""
        if mode == ExecutionMode.PARALLEL:
            # 并行执行，时间主要取决于最慢的任务
            return f"{task_count * 5}-{task_count * 10} minutes"
        else:
            # 顺序或层级，时间累加
            return f"{task_count * 10}-{task_count * 20} minutes"

    def format_plan(self, plan: OrchestrationPlan, verbose: bool = False) -> str:
        """
        格式化编排计划

        Args:
            plan: 编排计划
            verbose: 是否显示详细信息

        Returns:
            格式化的字符串
        """
        lines = []
        lines.append("## 🎯 Multi-Agent Orchestration Plan")
        lines.append("")
        lines.append(f"**执行模式**: {plan.execution_mode.value}")
        lines.append(f"**任务数量**: {len(plan.tasks)}")
        lines.append(f"**预计时长**: {plan.estimated_duration}")
        lines.append("")

        if plan.execution_mode == ExecutionMode.PARALLEL:
            # 并行模式：按组显示
            groups = plan.get_parallel_tasks()
            for i, group in enumerate(groups):
                if len(groups) > 1:
                    lines.append(f"### 执行组 {i + 1}")
                for task in group:
                    lines.append(f"- **{task.agent.role}** (`{task.agent.name}`)")
                    lines.append(f"  - 命令: `{task.command}`")
                    if verbose and task.agent.expertise:
                        lines.append(f"  - 专长: {', '.join(task.agent.expertise[:2])}")
                lines.append("")
        else:
            # 顺序/层级模式：按顺序显示
            tasks = plan.get_sequential_tasks()
            for i, task in enumerate(tasks):
                lines.append(f"{i + 1}. **{task.agent.role}** (`{task.agent.name}`)")
                lines.append(f"   - 命令: `{task.command}`")
                if task.dependencies:
                    lines.append(f"   - 依赖: {', '.join(task.dependencies)}")
                if verbose and task.agent.expertise:
                    lines.append(f"   - 专长: {', '.join(task.agent.expertise[:2])}")
                lines.append("")

        return "\n".join(lines)
