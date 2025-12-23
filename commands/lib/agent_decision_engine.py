"""
Agent Decision Engine - 决策引擎

负责在 Agent 推荐和用户命令冲突时做出决策。

核心功能:
- 计算 Agent 匹配度评分
- 根据匹配度阈值选择决策模式
- 格式化用户选项
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class DecisionResult:
    """决策结果数据结构"""

    # 最终执行的命令
    final_command: str

    # 决策模式: "auto", "prompt", "info"
    decision_mode: str

    # Agent 匹配度评分 (0.0-1.0)
    match_score: float

    # Agent 推荐的命令
    agent_recommendation: Optional[str]

    # 用户原始命令
    user_command: str

    # 选项（如果 decision_mode == "prompt"）
    options: Optional[List[Dict[str, str]]] = None

    # 决策说明
    reason: str = ""


class AgentDecisionEngine:
    """Agent 决策引擎"""

    # 决策阈值
    HIGH_CONFIDENCE_THRESHOLD = 0.85  # ≥85%: 自动执行 Agent 推荐
    MEDIUM_CONFIDENCE_THRESHOLD = 0.65  # 65-85%: 显示选项让用户选择

    def __init__(self):
        """初始化决策引擎"""
        self.decision_history = []  # 决策历史记录

    def decide(
        self,
        agent_context: Dict,
        user_command: str,
        decision_mode: str = "auto",
    ) -> DecisionResult:
        """
        主决策方法

        Args:
            agent_context: Agent激活上下文
                - agent_id: Agent ID
                - recommendation: 推荐的命令
                - confidence: Agent 的置信度
                - agent_name: Agent 名称
            user_command: 用户执行的命令
            decision_mode: 强制决策模式
                - "auto": 根据匹配度自动决策（默认）
                - "prompt": 总是显示选项
                - "force_agent": 强制使用 Agent 推荐
                - "force_user": 强制使用用户命令

        Returns:
            DecisionResult: 决策结果
        """
        try:
            # 提取 Agent 推荐
            agent_recommendation = agent_context.get("recommendation", "")

            # 如果 Agent 推荐和用户命令相同，直接返回
            if agent_recommendation == user_command:
                return DecisionResult(
                    final_command=user_command,
                    decision_mode="auto",
                    match_score=1.0,
                    agent_recommendation=agent_recommendation,
                    user_command=user_command,
                    reason="Agent 推荐与用户命令一致",
                )

            # 计算匹配度评分
            match_score = self.calculate_match_score(agent_context, user_command)

            # 处理强制决策模式
            if decision_mode == "force_agent":
                return self._create_decision(
                    final_command=agent_recommendation,
                    mode="auto",
                    score=match_score,
                    agent_rec=agent_recommendation,
                    user_cmd=user_command,
                    reason="强制使用 Agent 推荐",
                )

            if decision_mode == "force_user":
                return self._create_decision(
                    final_command=user_command,
                    mode="auto",
                    score=match_score,
                    agent_rec=agent_recommendation,
                    user_cmd=user_command,
                    reason="强制使用用户命令",
                )

            # 自动决策模式
            if decision_mode == "auto":
                actual_mode = self.get_decision_mode(match_score)

                if actual_mode == "auto":
                    # 高置信度：自动使用 Agent 推荐
                    return self._create_decision(
                        final_command=agent_recommendation,
                        mode="auto",
                        score=match_score,
                        agent_rec=agent_recommendation,
                        user_cmd=user_command,
                        reason=f"高匹配度 ({match_score:.0%})，自动使用 Agent 推荐",
                    )

                elif actual_mode == "prompt":
                    # 中等置信度：显示选项
                    options = self.get_option_descriptions()
                    return DecisionResult(
                        final_command="",  # 需要用户选择
                        decision_mode="prompt",
                        match_score=match_score,
                        agent_recommendation=agent_recommendation,
                        user_command=user_command,
                        options=options,
                        reason=f"中等匹配度 ({match_score:.0%})，建议用户选择",
                    )

                else:  # "info"
                    # 低置信度：执行用户命令，仅提示 Agent 信息
                    return self._create_decision(
                        final_command=user_command,
                        mode="info",
                        score=match_score,
                        agent_rec=agent_recommendation,
                        user_cmd=user_command,
                        reason=f"低匹配度 ({match_score:.0%})，执行用户命令，仅提示 Agent 信息",
                    )

            # 强制显示选项模式
            if decision_mode == "prompt":
                options = self.get_option_descriptions()
                return DecisionResult(
                    final_command="",
                    decision_mode="prompt",
                    match_score=match_score,
                    agent_recommendation=agent_recommendation,
                    user_command=user_command,
                    options=options,
                    reason="强制显示选项模式",
                )

            # 默认：使用用户命令
            return self._create_decision(
                final_command=user_command,
                mode="auto",
                score=match_score,
                agent_rec=agent_recommendation,
                user_cmd=user_command,
                reason="未知决策模式，默认使用用户命令",
            )

        except Exception as e:
            logger.error(f"决策引擎错误: {e}")
            # 错误时默认使用用户命令
            return self._create_decision(
                final_command=user_command,
                mode="auto",
                score=0.0,
                agent_rec=agent_context.get("recommendation", ""),
                user_cmd=user_command,
                reason=f"决策引擎错误: {e}",
            )

    def calculate_match_score(self, agent_context: Dict, user_command: str) -> float:
        """
        计算 Agent 匹配度 (0.0-1.0)

        评分组成:
        - 关键词匹配: 40%
        - 上下文匹配: 20%
        - Agent 置信度: 40%

        Args:
            agent_context: Agent 上下文
            user_command: 用户命令

        Returns:
            匹配度分数 (0.0-1.0)
        """
        try:
            # 提取关键信息
            agent_recommendation = agent_context.get("recommendation", "")
            base_confidence = agent_context.get("confidence", 0.5)

            # 如果推荐为空，返回置信度分数
            if not agent_recommendation:
                return max(0.0, min(1.0, base_confidence))

            # 1. 关键词匹配 (40%) - 最重要的因素
            keyword_score = self._calculate_keyword_match(
                agent_recommendation, user_command
            )

            # 2. 上下文匹配 (20%)
            context_score = self._calculate_context_match(agent_context, user_command)

            # 3. Agent 置信度 (40%) - Agent 本身的置信度
            confidence_score = base_confidence

            # 综合评分
            final_score = (
                keyword_score * 0.4 + context_score * 0.2 + confidence_score * 0.4
            )

            # 确保在 0.0-1.0 范围内
            return max(0.0, min(1.0, final_score))

        except Exception as e:
            logger.error(f"匹配度计算错误: {e}")
            return 0.5  # 默认中等匹配度

    def _calculate_keyword_match(
        self, agent_recommendation: str, user_command: str
    ) -> float:
        """
        计算关键词匹配度

        使用多种匹配策略：
        1. 完全匹配（相同字符串）
        2. 前缀匹配（主命令相同）
        3. Jaccard 相似度（关键词相似）

        Args:
            agent_recommendation: Agent 推荐的命令
            user_command: 用户命令

        Returns:
            关键词匹配分数 (0.0-1.0)
        """
        if not agent_recommendation or not user_command:
            return 0.0

        agent_lower = agent_recommendation.lower()
        user_lower = user_command.lower()

        # 1. 完全匹配
        if agent_lower == user_lower:
            return 1.0

        # 2. 前缀匹配（主命令相同）
        agent_parts = agent_lower.split()
        user_parts = user_lower.split()

        if agent_parts and user_parts and agent_parts[0] == user_parts[0]:
            # 主命令相同，给予较高分数
            return 0.75

        # 3. Jaccard 相似度（关键词匹配）
        agent_keywords = set(agent_parts)
        user_keywords = set(user_parts)

        intersection = agent_keywords & user_keywords
        union = agent_keywords | user_keywords

        if not union:
            return 0.0

        jaccard_score = len(intersection) / len(union)

        # 如果包含主命令匹配，提高分数
        if agent_parts and user_parts and agent_parts[0] == user_parts[0]:
            jaccard_score = min(1.0, jaccard_score * 1.5)

        return min(1.0, jaccard_score)

    def _calculate_context_match(
        self, agent_context: Dict, user_command: str
    ) -> float:
        """
        计算上下文匹配度

        Args:
            agent_context: Agent 上下文
            user_command: 用户命令

        Returns:
            上下文匹配分数 (0.0-1.0)
        """
        # 简化实现：基于 Agent 的专长匹配
        agent_expertise = agent_context.get("expertise", [])
        user_cmd_lower = user_command.lower()

        # 检查用户命令是否包含 Agent 专长的关键词
        matches = 0
        for expertise in agent_expertise:
            if any(keyword.lower() in user_cmd_lower for keyword in expertise.split()):
                matches += 1

        if not agent_expertise:
            return 0.5  # 无专长信息，返回中等分数

        return min(1.0, matches / len(agent_expertise))

    def get_decision_mode(self, match_score: float) -> str:
        """
        根据匹配度获取决策模式

        Args:
            match_score: 匹配度分数 (0.0-1.0)

        Returns:
            决策模式: "auto", "prompt", "info"
        """
        if match_score >= self.HIGH_CONFIDENCE_THRESHOLD:
            return "auto"  # 高置信度：自动执行
        elif match_score >= self.MEDIUM_CONFIDENCE_THRESHOLD:
            return "prompt"  # 中等置信度：显示选项
        else:
            return "info"  # 低置信度：仅提示信息

    def format_options(self, agent_cmd: str, user_cmd: str) -> str:
        """
        格式化三个选项供用户选择

        Args:
            agent_cmd: Agent 推荐的命令
            user_cmd: 用户命令

        Returns:
            格式化的选项字符串
        """
        options = self.get_option_descriptions()

        output = "## 🤖 Agent 推荐冲突\n\n"
        output += f"**Agent 推荐**: {agent_cmd}\n"
        output += f"**用户命令**: {user_cmd}\n\n"
        output += "请选择:\n\n"

        for i, option in enumerate(options, 1):
            label = option["label"]
            description = option["description"]
            output += f"{i}. **{label}**: {description}\n"

        return output

    def get_option_descriptions(self) -> List[Dict[str, str]]:
        """
        获取三个选项的描述

        Returns:
            选项列表，每个选项包含 label 和 description
        """
        return [
            {
                "label": "使用 Agent 推荐",
                "description": "改用 Agent 推荐的命令（AI 倾向）",
            },
            {
                "label": "继续用户命令",
                "description": "继续执行用户的原始命令",
            },
            {
                "label": "并行执行",
                "description": "先执行 Agent 推荐，再执行用户命令",
            },
        ]

    def _create_decision(
        self,
        final_command: str,
        mode: str,
        score: float,
        agent_rec: str,
        user_cmd: str,
        reason: str,
    ) -> DecisionResult:
        """
        创建决策结果的辅助方法

        Args:
            final_command: 最终执行的命令
            mode: 决策模式
            score: 匹配度评分
            agent_rec: Agent 推荐
            user_cmd: 用户命令
            reason: 决策理由

        Returns:
            DecisionResult
        """
        result = DecisionResult(
            final_command=final_command,
            decision_mode=mode,
            match_score=score,
            agent_recommendation=agent_rec,
            user_command=user_cmd,
            reason=reason,
        )

        # 记录决策历史
        self.decision_history.append(
            {
                "final_command": final_command,
                "mode": mode,
                "score": score,
                "reason": reason,
            }
        )

        return result
