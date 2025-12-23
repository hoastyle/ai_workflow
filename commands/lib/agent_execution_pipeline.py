"""
Agent Execution Pipeline - Phase 2.5 端到端集成

整合 Phase 2.1-2.4 的所有组件：
- Phase 2.1: 决策引擎 (AgentDecisionEngine)
- Phase 2.2: 执行器 (AgentCommandExecutor)
- Phase 2.3: 反馈系统 (AgentFeedbackSystem)
- Phase 2.4: 多Agent协调 (MultiAgentOrchestrator)

提供统一的端到端执行接口。
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import logging

from commands.lib.agent_decision_engine import AgentDecisionEngine, DecisionResult
from commands.lib.agent_command_executor import AgentCommandExecutor, ExecutionResult
from commands.lib.agent_feedback_system import AgentFeedbackSystem
from commands.lib.agent_execution_history import AgentExecutionHistory
from commands.lib.agent_registry import Agent
from commands.lib.multi_agent_orchestrator import (
    MultiAgentOrchestrator,
    ExecutionMode,
    ConflictResolutionStrategy,
    AgentTask,
    OrchestrationResult
)

logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """执行管道配置"""

    # 决策引擎配置
    decision_confidence_threshold: float = 0.85
    auto_execute_threshold: float = 0.85

    # 执行器配置
    execution_timeout: int = 30
    enable_mcp_tools: bool = True

    # 反馈系统配置
    enable_feedback: bool = True
    feedback_min_samples: int = 5

    # 协调器配置
    default_execution_mode: ExecutionMode = ExecutionMode.SEQUENTIAL
    default_conflict_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.PRIORITY_BASED

    # 管道配置
    enable_history: bool = True
    max_retry_attempts: int = 3


@dataclass
class PipelineResult:
    """执行管道结果"""

    # 基本信息
    success: bool
    pipeline_id: str
    timestamp: datetime = field(default_factory=datetime.now)

    # 各阶段结果
    decision_result: Optional[DecisionResult] = None
    execution_result: Optional[ExecutionResult] = None
    orchestration_result: Optional[OrchestrationResult] = None

    # 反馈和统计
    feedback_score: Optional[float] = None
    agent_scores: Dict[str, float] = field(default_factory=dict)

    # 错误信息
    error: Optional[str] = None
    error_stage: Optional[str] = None

    # 性能指标
    total_duration_ms: float = 0.0
    decision_duration_ms: float = 0.0
    execution_duration_ms: float = 0.0

    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentExecutionPipeline:
    """
    Agent 执行管道

    整合决策、执行、反馈、协调的完整流程。
    """

    def __init__(self, config: Optional[PipelineConfig] = None):
        """初始化执行管道"""
        self.config = config or PipelineConfig()

        # 初始化各组件
        self.decision_engine = AgentDecisionEngine()
        self.executor = AgentCommandExecutor()
        self.feedback_system = AgentFeedbackSystem()
        self.orchestrator = MultiAgentOrchestrator()

        # 初始化历史记录
        if self.config.enable_history:
            self.history = AgentExecutionHistory()
        else:
            self.history = None

        # 运行时状态
        self._pipeline_counter = 0

        logger.info("AgentExecutionPipeline initialized")

    def execute_single_agent(
        self,
        user_input: str,
        command_name: str,
        context: Optional[Dict[str, Any]] = None
    ) -> PipelineResult:
        """
        执行单个 Agent 的完整流程

        Args:
            user_input: 用户输入/任务描述
            command_name: 当前执行的命令名
            context: 上下文信息

        Returns:
            PipelineResult: 执行结果
        """
        start_time = datetime.now()
        self._pipeline_counter += 1
        pipeline_id = f"pipeline_{self._pipeline_counter}_{start_time.strftime('%Y%m%d_%H%M%S')}"

        result = PipelineResult(
            success=False,
            pipeline_id=pipeline_id
        )

        try:
            # Stage 1: 决策引擎
            logger.info(f"[{pipeline_id}] Stage 1: Decision")
            decision_start = datetime.now()

            decision_result = self.decision_engine.analyze_and_recommend(
                user_input=user_input,
                command_name=command_name,
                context=context or {}
            )

            decision_duration = (datetime.now() - decision_start).total_seconds() * 1000
            result.decision_result = decision_result
            result.decision_duration_ms = decision_duration

            # 检查是否应该执行
            if decision_result.confidence < self.config.decision_confidence_threshold:
                result.success = True
                result.metadata['skipped'] = True
                result.metadata['reason'] = 'Low confidence decision'
                logger.info(f"[{pipeline_id}] Skipped: Low confidence ({decision_result.confidence})")
                return result

            # Stage 2: 执行器
            logger.info(f"[{pipeline_id}] Stage 2: Execution")
            execution_start = datetime.now()

            execution_result = self.executor.execute_command(
                command=decision_result.recommended_command,
                context=context or {},
                timeout=self.config.execution_timeout
            )

            execution_duration = (datetime.now() - execution_start).total_seconds() * 1000
            result.execution_result = execution_result
            result.execution_duration_ms = execution_duration

            # Stage 3: 反馈系统 (如果启用)
            if self.config.enable_feedback:
                logger.info(f"[{pipeline_id}] Stage 3: Feedback")

                # 记录执行历史
                if self.history:
                    self.history.record_execution(
                        agent_name=decision_result.matched_agent.name if decision_result.matched_agent else "unknown",
                        command=decision_result.recommended_command,
                        success=execution_result.success,
                        duration_ms=execution_duration,
                        context=context or {}
                    )

                # 评估有效性
                effectiveness = self.feedback_system.evaluate_execution_effectiveness(
                    agent_name=decision_result.matched_agent.name if decision_result.matched_agent else "unknown",
                    success=execution_result.success,
                    duration_ms=execution_duration
                )

                result.feedback_score = effectiveness

                # 更新 Agent 评分
                if decision_result.matched_agent:
                    agent_score = self.feedback_system.get_agent_score(
                        decision_result.matched_agent.name
                    )
                    if agent_score:
                        result.agent_scores[decision_result.matched_agent.name] = agent_score.avg_score

            # 计算总耗时
            result.total_duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            result.success = execution_result.success

            logger.info(f"[{pipeline_id}] Pipeline completed: {result.success}")

        except Exception as e:
            result.success = False
            result.error = str(e)
            result.error_stage = self._determine_error_stage(result)
            logger.error(f"[{pipeline_id}] Pipeline error: {e}", exc_info=True)

        return result

    def execute_multi_agent(
        self,
        tasks: List[AgentTask],
        execution_mode: Optional[ExecutionMode] = None,
        conflict_strategy: Optional[ConflictResolutionStrategy] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> PipelineResult:
        """
        执行多 Agent 协调流程

        Args:
            tasks: Agent 任务列表
            execution_mode: 执行模式 (默认使用配置)
            conflict_strategy: 冲突解决策略 (默认使用配置)
            context: 上下文信息

        Returns:
            PipelineResult: 执行结果
        """
        start_time = datetime.now()
        self._pipeline_counter += 1
        pipeline_id = f"multi_pipeline_{self._pipeline_counter}_{start_time.strftime('%Y%m%d_%H%M%S')}"

        result = PipelineResult(
            success=False,
            pipeline_id=pipeline_id
        )

        try:
            logger.info(f"[{pipeline_id}] Multi-agent orchestration started")

            # 使用协调器执行
            mode = execution_mode or self.config.default_execution_mode
            strategy = conflict_strategy or self.config.default_conflict_strategy

            orchestration_result = self.orchestrator.execute_plan(
                tasks=tasks,
                mode=mode,
                conflict_strategy=strategy,
                context=context or {}
            )

            result.orchestration_result = orchestration_result
            result.success = orchestration_result.success

            # 记录每个 Agent 的执行历史和反馈
            if self.config.enable_feedback and self.history:
                for agent_name, task_result in orchestration_result.task_results.items():
                    self.history.record_execution(
                        agent_name=agent_name,
                        command=tasks[0].command if tasks else "unknown",  # 简化处理
                        success=task_result.get('success', False),
                        duration_ms=task_result.get('duration_ms', 0.0),
                        context=context or {}
                    )

                    # 评估有效性
                    effectiveness = self.feedback_system.evaluate_execution_effectiveness(
                        agent_name=agent_name,
                        success=task_result.get('success', False),
                        duration_ms=task_result.get('duration_ms', 0.0)
                    )

                    # 更新评分
                    agent_score = self.feedback_system.get_agent_score(agent_name)
                    if agent_score:
                        result.agent_scores[agent_name] = agent_score.avg_score

            # 计算总耗时
            result.total_duration_ms = (datetime.now() - start_time).total_seconds() * 1000

            logger.info(f"[{pipeline_id}] Multi-agent orchestration completed: {result.success}")

        except Exception as e:
            result.success = False
            result.error = str(e)
            result.error_stage = "orchestration"
            logger.error(f"[{pipeline_id}] Multi-agent error: {e}", exc_info=True)

        return result

    def get_pipeline_statistics(self) -> Dict[str, Any]:
        """获取管道统计信息"""
        stats = {
            'total_pipelines_executed': self._pipeline_counter,
            'config': {
                'decision_threshold': self.config.decision_confidence_threshold,
                'execution_timeout': self.config.execution_timeout,
                'feedback_enabled': self.config.enable_feedback,
                'history_enabled': self.config.enable_history
            }
        }

        # 添加历史统计
        if self.history:
            stats['execution_history'] = self.history.get_statistics()

        # 添加反馈统计
        if self.config.enable_feedback:
            stats['feedback_summary'] = self.feedback_system.generate_feedback_report()

        return stats

    def _determine_error_stage(self, result: PipelineResult) -> str:
        """确定错误发生的阶段"""
        if result.decision_result is None:
            return "decision"
        elif result.execution_result is None:
            return "execution"
        elif self.config.enable_feedback:
            return "feedback"
        else:
            return "unknown"

    def reset_statistics(self):
        """重置统计信息"""
        self._pipeline_counter = 0
        if self.history:
            self.history = AgentExecutionHistory()
        logger.info("Pipeline statistics reset")
