"""
Agent Feedback System - 反馈验证系统

负责验证 Agent 推荐是否有效，收集反馈进行改进。

核心功能:
- 记录 Agent 执行历史
- 评估 Agent 推荐的有效性
- 更新 Agent 的推荐准确率
- 识别高效和低效的 Agent
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import logging

from .agent_execution_history import AgentExecutionHistory, ExecutionRecord

logger = logging.getLogger(__name__)


@dataclass
class AgentScore:
    """Agent 评分信息"""

    agent_id: str
    agent_name: str

    # 推荐采纳率 (0.0 - 1.0)
    adoption_rate: float = 0.5

    # 推荐成功率 (0.0 - 1.0)
    success_rate: float = 0.5

    # 平均有效性评分 (0.0 - 1.0)
    average_effectiveness: float = 0.5

    # 综合评分 (0.0 - 1.0)
    composite_score: float = 0.5

    # 推荐次数
    total_recommendations: int = 0

    # 最后更新时间
    last_updated: str = ""


class AgentFeedbackSystem:
    """Agent 反馈系统"""

    def __init__(self, history_file: Optional[str] = None):
        """
        初始化反馈系统

        Args:
            history_file: 执行历史文件路径（可选）
        """
        self.history = AgentExecutionHistory(history_file)
        self.agent_scores: Dict[str, AgentScore] = {}

    def record_execution(
        self,
        agent_id: str,
        agent_name: str,
        user_command: str,
        agent_recommendation: str,
        executed_command: str,
        execution_status: str,
        exit_code: int = 0,
        match_score: float = 0.0,
        execution_time: float = 0.0,
        was_adopted: bool = False,
        metadata: Dict[str, Any] = None,
    ) -> ExecutionRecord:
        """
        记录 Agent 执行

        Args:
            agent_id: Agent ID
            agent_name: Agent 名称
            user_command: 用户命令
            agent_recommendation: Agent 推荐
            executed_command: 实际执行的命令
            execution_status: 执行状态
            exit_code: 退出码
            match_score: 匹配度
            execution_time: 执行时间
            was_adopted: 是否采纳了 Agent 推荐
            metadata: 额外元数据

        Returns:
            ExecutionRecord: 执行记录
        """
        record = ExecutionRecord(
            timestamp=datetime.now().isoformat(),
            agent_id=agent_id,
            agent_name=agent_name,
            user_command=user_command,
            agent_recommendation=agent_recommendation,
            executed_command=executed_command,
            execution_status=execution_status,
            exit_code=exit_code,
            match_score=match_score,
            execution_time=execution_time,
            was_adopted=was_adopted,
            metadata=metadata or {},
        )

        self.history.add_record(record)
        return record

    def evaluate_effectiveness(
        self,
        execution_status: str,
        was_adopted: bool,
        match_score: float,
    ) -> float:
        """
        评估 Agent 推荐的有效性

        Args:
            execution_status: 执行状态
            was_adopted: 是否被采纳
            match_score: 匹配度

        Returns:
            有效性评分 (0.0 - 1.0)
        """
        # 基础评分：根据执行状态
        status_score = {
            "success": 1.0,
            "failure": 0.3,
            "timeout": 0.2,
            "error": 0.1,
        }.get(execution_status, 0.0)

        # 采纳奖励：如果 Agent 推荐被采纳
        adoption_bonus = 0.2 if was_adopted else 0.0

        # 匹配度奖励：高匹配度的推荐即使失败也有一定价值
        match_bonus = match_score * 0.2

        # 综合评分
        effectiveness = min(1.0, status_score + adoption_bonus + match_bonus)

        return effectiveness

    def update_agent_score(self, agent_id: str, agent_name: str) -> AgentScore:
        """
        更新 Agent 的评分

        Args:
            agent_id: Agent ID
            agent_name: Agent 名称

        Returns:
            更新后的 Agent 评分
        """
        stats = self.history.get_agent_statistics(agent_id)

        if not stats or stats["total_executions"] == 0:
            # 新 Agent，初始化评分
            score = AgentScore(
                agent_id=agent_id,
                agent_name=agent_name,
                adoption_rate=0.5,
                success_rate=0.5,
                average_effectiveness=0.5,
                composite_score=0.5,
                total_recommendations=0,
                last_updated=datetime.now().isoformat(),
            )
        else:
            # 根据历史数据计算评分
            adoption_rate = stats.get("adoption_rate", 0.5)
            success_rate = stats.get("success_rate", 0.5)
            avg_effectiveness = stats.get("average_effectiveness", 0.5)

            # 综合评分：加权平均
            composite_score = (
                adoption_rate * 0.3 + success_rate * 0.4 + avg_effectiveness * 0.3
            )

            score = AgentScore(
                agent_id=agent_id,
                agent_name=agent_name,
                adoption_rate=adoption_rate,
                success_rate=success_rate,
                average_effectiveness=avg_effectiveness,
                composite_score=composite_score,
                total_recommendations=stats.get("total_executions", 0),
                last_updated=datetime.now().isoformat(),
            )

        self.agent_scores[agent_id] = score
        return score

    def get_agent_score(self, agent_id: str) -> Optional[AgentScore]:
        """
        获取 Agent 的评分

        Args:
            agent_id: Agent ID

        Returns:
            Agent 评分，如果不存在则返回 None
        """
        return self.agent_scores.get(agent_id)

    def get_top_agents(self, limit: int = 5) -> List[AgentScore]:
        """
        获取评分最高的 Agent

        Args:
            limit: 返回的最大 Agent 数量

        Returns:
            按评分排序的 Agent 列表
        """
        sorted_agents = sorted(
            self.agent_scores.values(),
            key=lambda x: x.composite_score,
            reverse=True,
        )
        return sorted_agents[:limit]

    def get_bottom_agents(self, limit: int = 5) -> List[AgentScore]:
        """
        获取评分最低的 Agent

        Args:
            limit: 返回的最大 Agent 数量

        Returns:
            按评分排序的 Agent 列表
        """
        sorted_agents = sorted(
            self.agent_scores.values(),
            key=lambda x: x.composite_score,
        )
        return sorted_agents[:limit]

    def get_all_agent_scores(self) -> Dict[str, AgentScore]:
        """
        获取所有 Agent 的评分

        Returns:
            Agent ID 到评分的映射
        """
        return self.agent_scores.copy()

    def should_recommend_agent(
        self,
        agent_id: str,
        min_score: float = 0.5,
    ) -> bool:
        """
        判断是否应该推荐某个 Agent

        Args:
            agent_id: Agent ID
            min_score: 最低推荐评分

        Returns:
            是否应该推荐
        """
        score = self.get_agent_score(agent_id)
        if not score:
            # 新 Agent，保守推荐
            return True

        return score.composite_score >= min_score

    def get_recommendation_impact(self) -> Dict[str, Any]:
        """
        获取 Agent 推荐的整体影响

        Returns:
            影响统计信息
        """
        global_stats = self.history.get_global_statistics()

        return {
            "total_recommendations": global_stats.get("total_executions", 0),
            "adoption_rate": global_stats.get("adoption_rate", 0.0),
            "success_rate": global_stats.get("success_rate", 0.0),
            "average_effectiveness": global_stats.get("average_effectiveness", 0.0),
            "total_agents": global_stats.get("total_agents", 0),
        }

    def generate_feedback_report(self) -> str:
        """
        生成反馈报告

        Returns:
            反馈报告字符串
        """
        report = []
        report.append("=" * 80)
        report.append("Agent Feedback System Report")
        report.append("=" * 80)
        report.append("")

        # 全局统计
        impact = self.get_recommendation_impact()
        report.append("Global Statistics:")
        report.append(f"  Total Recommendations: {impact['total_recommendations']}")
        report.append(f"  Adoption Rate: {impact['adoption_rate']:.1%}")
        report.append(f"  Success Rate: {impact['success_rate']:.1%}")
        report.append(f"  Average Effectiveness: {impact['average_effectiveness']:.2f}")
        report.append(f"  Total Agents: {impact['total_agents']}")
        report.append("")

        # 顶级 Agent
        report.append("Top 5 Agents:")
        for agent in self.get_top_agents(5):
            report.append(
                f"  {agent.agent_name} ({agent.agent_id}): "
                f"Score={agent.composite_score:.2f}, "
                f"Adoptions={agent.total_recommendations}, "
                f"Success={agent.success_rate:.1%}"
            )
        report.append("")

        # 低效 Agent
        report.append("Bottom 5 Agents:")
        for agent in self.get_bottom_agents(5):
            report.append(
                f"  {agent.agent_name} ({agent.agent_id}): "
                f"Score={agent.composite_score:.2f}, "
                f"Adoptions={agent.total_recommendations}, "
                f"Success={agent.success_rate:.1%}"
            )
        report.append("")

        report.append("=" * 80)
        return "\n".join(report)
