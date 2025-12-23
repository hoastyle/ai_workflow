"""
Agent Execution History - 执行历史管理

负责记录和管理 Agent 执行的历史数据。

核心功能:
- 记录每次 Agent 执行的详细信息
- 支持执行历史查询和统计
- 计算 Agent 的推荐准确率
- 持久化存储执行数据
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ExecutionRecord:
    """执行记录数据结构"""

    # 时间戳
    timestamp: str

    # Agent 信息
    agent_id: str
    agent_name: str

    # 命令信息
    user_command: str
    agent_recommendation: str

    # 执行结果
    executed_command: str
    execution_status: str  # success, failure, timeout, error
    exit_code: int = 0

    # 匹配度评分
    match_score: float = 0.0

    # 执行指标
    execution_time: float = 0.0
    was_adopted: bool = False  # Agent 推荐是否被采纳

    # 效果评估
    effectiveness: float = 0.0  # 0.0 - 1.0
    user_feedback: str = ""  # 可选的用户反馈

    # 额外数据
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentExecutionHistory:
    """Agent 执行历史管理器"""

    def __init__(self, history_file: Optional[str] = None):
        """
        初始化执行历史管理器

        Args:
            history_file: 执行历史文件路径（可选，不设置时为内存管理）
        """
        self.history_file = history_file
        self.records: List[ExecutionRecord] = []
        self._load_history()

    def add_record(self, record: ExecutionRecord) -> None:
        """
        添加执行记录

        Args:
            record: 执行记录
        """
        self.records.append(record)

        # 如果配置了历史文件，则保存
        if self.history_file:
            self._save_history()

    def get_records_by_agent(self, agent_id: str) -> List[ExecutionRecord]:
        """
        获取特定 Agent 的所有执行记录

        Args:
            agent_id: Agent ID

        Returns:
            执行记录列表
        """
        return [r for r in self.records if r.agent_id == agent_id]

    def get_records_by_status(self, status: str) -> List[ExecutionRecord]:
        """
        获取特定状态的执行记录

        Args:
            status: 执行状态 (success, failure, timeout, error)

        Returns:
            执行记录列表
        """
        return [r for r in self.records if r.execution_status == status]

    def get_recent_records(self, agent_id: str, limit: int = 10) -> List[ExecutionRecord]:
        """
        获取特定 Agent 的最近执行记录

        Args:
            agent_id: Agent ID
            limit: 返回的最大记录数

        Returns:
            最近的执行记录列表
        """
        agent_records = self.get_records_by_agent(agent_id)
        return agent_records[-limit:] if agent_records else []

    def get_agent_statistics(self, agent_id: str) -> Dict[str, Any]:
        """
        获取特定 Agent 的执行统计

        Args:
            agent_id: Agent ID

        Returns:
            统计信息字典
        """
        agent_records = self.get_records_by_agent(agent_id)

        if not agent_records:
            return {
                "total_executions": 0,
                "success_count": 0,
                "failure_count": 0,
                "adoption_rate": 0.0,
                "success_rate": 0.0,
                "average_effectiveness": 0.0,
                "average_execution_time": 0.0,
            }

        total = len(agent_records)
        success_count = sum(1 for r in agent_records if r.execution_status == "success")
        failure_count = sum(1 for r in agent_records if r.execution_status == "failure")
        adopted_count = sum(1 for r in agent_records if r.was_adopted)
        avg_effectiveness = sum(r.effectiveness for r in agent_records) / total
        avg_time = sum(r.execution_time for r in agent_records) / total

        return {
            "total_executions": total,
            "success_count": success_count,
            "failure_count": failure_count,
            "adoption_rate": adopted_count / total if total > 0 else 0.0,
            "success_rate": success_count / total if total > 0 else 0.0,
            "average_effectiveness": avg_effectiveness,
            "average_execution_time": avg_time,
        }

    def get_global_statistics(self) -> Dict[str, Any]:
        """
        获取全局执行统计

        Returns:
            全局统计信息字典
        """
        if not self.records:
            return {
                "total_executions": 0,
                "total_agents": 0,
                "success_count": 0,
                "failure_count": 0,
                "adoption_rate": 0.0,
                "success_rate": 0.0,
                "average_effectiveness": 0.0,
            }

        total = len(self.records)
        success_count = sum(1 for r in self.records if r.execution_status == "success")
        failure_count = sum(1 for r in self.records if r.execution_status == "failure")
        adopted_count = sum(1 for r in self.records if r.was_adopted)
        avg_effectiveness = sum(r.effectiveness for r in self.records) / total
        unique_agents = len(set(r.agent_id for r in self.records))

        return {
            "total_executions": total,
            "total_agents": unique_agents,
            "success_count": success_count,
            "failure_count": failure_count,
            "adoption_rate": adopted_count / total if total > 0 else 0.0,
            "success_rate": success_count / total if total > 0 else 0.0,
            "average_effectiveness": avg_effectiveness,
        }

    def clear_history(self, agent_id: Optional[str] = None) -> None:
        """
        清空执行历史

        Args:
            agent_id: 如果指定，则仅清空该 Agent 的历史，否则清空所有历史
        """
        if agent_id:
            self.records = [r for r in self.records if r.agent_id != agent_id]
        else:
            self.records.clear()

        if self.history_file:
            self._save_history()

    def _load_history(self) -> None:
        """从文件加载执行历史"""
        if not self.history_file:
            return

        try:
            history_path = Path(self.history_file)
            if history_path.exists():
                with open(history_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        record = ExecutionRecord(**item)
                        self.records.append(record)
                logger.info(f"加载执行历史: {len(self.records)} 条记录")
        except Exception as e:
            logger.error(f"加载执行历史失败: {e}")

    def _save_history(self) -> None:
        """将执行历史保存到文件"""
        if not self.history_file:
            return

        try:
            history_path = Path(self.history_file)
            history_path.parent.mkdir(parents=True, exist_ok=True)

            # 限制历史记录数量
            records_to_save = self.records[-10000:]  # 保留最多 10000 条

            with open(history_path, "w", encoding="utf-8") as f:
                json.dump(
                    [asdict(r) for r in records_to_save],
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
        except Exception as e:
            logger.error(f"保存执行历史失败: {e}")

    def export_as_json(self) -> str:
        """
        导出执行历史为 JSON 字符串

        Returns:
            JSON 字符串
        """
        return json.dumps(
            [asdict(r) for r in self.records],
            ensure_ascii=False,
            indent=2,
        )

    def import_from_json(self, json_str: str) -> None:
        """
        从 JSON 字符串导入执行历史

        Args:
            json_str: JSON 字符串
        """
        try:
            data = json.loads(json_str)
            for item in data:
                record = ExecutionRecord(**item)
                self.records.append(record)
        except Exception as e:
            logger.error(f"导入执行历史失败: {e}")
