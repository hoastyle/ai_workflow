#!/usr/bin/env python3
"""
Task Analyzer - Intelligent task description analysis for agent activation

This module provides advanced task analysis capabilities that build on
AgentRegistry's keyword matching, adding:
- Intent recognition (what is the user trying to achieve?)
- Task classification (development phase, complexity, urgency)
- Context extraction (technical stack, dependencies)
- Confidence assessment for agent recommendations

Design Principles:
- Lightweight wrapper around AgentRegistry
- Focus on "why" not just "what" (intent vs keywords)
- Provide explainable recommendations
- Support manual override

Usage:
    from commands.lib.task_analyzer import TaskAnalyzer

    analyzer = TaskAnalyzer()
    analysis = analyzer.analyze("实现用户登录功能")
    print(f"Primary intent: {analysis.intent}")
    print(f"Recommended agent: {analysis.primary_agent}")
    print(f"Confidence: {analysis.confidence}%")
"""

import re
from typing import List, Optional, Dict
from dataclasses import dataclass
from enum import Enum

from commands.lib.agent_registry import AgentRegistry, AgentMatch


class TaskIntent(Enum):
    """High-level intent classification"""
    PLANNING = "planning"              # 规划、设计
    IMPLEMENTATION = "implementation"  # 实现、编码
    DEBUGGING = "debugging"            # 调试、修复
    TESTING = "testing"                # 测试、验证
    REVIEWING = "reviewing"            # 审查、质量检查
    REFACTORING = "refactoring"        # 重构、优化
    DOCUMENTATION = "documentation"    # 文档、说明
    RESEARCH = "research"              # 研究、调研
    CONTEXT_LOADING = "context"        # 上下文加载
    UNCLEAR = "unclear"                # 意图不明


class TaskComplexity(Enum):
    """Task complexity classification"""
    SIMPLE = "simple"       # 简单（单文件小改动）
    MODERATE = "moderate"   # 中等（多文件或复杂逻辑）
    COMPLEX = "complex"     # 复杂（架构级改动）


@dataclass
class TaskAnalysis:
    """Complete task analysis result"""
    # Raw input
    task_description: str

    # Intent analysis
    intent: TaskIntent
    intent_confidence: float  # 0.0-1.0

    # Agent recommendations
    primary_agent: Optional[AgentMatch]
    fallback_agents: List[AgentMatch]

    # Task characteristics
    complexity: TaskComplexity
    estimated_effort: str  # "5-10 minutes", "1-2 hours", etc.

    # Technical context
    keywords: List[str]
    technical_stack: List[str]  # Extracted from description

    # Metadata
    confidence: float  # Overall confidence (0-100)
    explanation: str   # Human-readable explanation
    suggestions: List[str]  # Additional suggestions

    def __str__(self) -> str:
        return f"""
Task Analysis
=============
Description: {self.task_description}
Intent: {self.intent.value} (confidence: {self.intent_confidence:.0%})
Complexity: {self.complexity.value}
Estimated Effort: {self.estimated_effort}

Recommended Agent:
  {self.primary_agent}

Overall Confidence: {self.confidence:.0%}
Explanation: {self.explanation}
"""


class TaskAnalyzer:
    """
    Advanced task analyzer with intent recognition

    Features:
    - Intent classification (9 categories)
    - Complexity assessment
    - Effort estimation
    - Technical stack extraction
    - Explainable recommendations
    """

    def __init__(self, registry: Optional[AgentRegistry] = None):
        """
        Initialize task analyzer

        Args:
            registry: AgentRegistry instance (creates new if None)
        """
        self.registry = registry or AgentRegistry()

        # Intent detection patterns
        self.intent_patterns = {
            TaskIntent.PLANNING: [
                r'规划', r'设计', r'plan', r'design', r'架构',
                r'方案', r'策略', r'roadmap'
            ],
            TaskIntent.IMPLEMENTATION: [
                r'实现', r'开发', r'编写', r'添加', r'创建',
                r'implement', r'develop', r'create', r'add', r'build'
            ],
            TaskIntent.DEBUGGING: [
                r'调试', r'修复', r'解决', r'bug', r'debug',
                r'fix', r'error', r'问题', r'错误'
            ],
            TaskIntent.TESTING: [
                r'测试', r'验证', r'test', r'verify', r'coverage',
                r'覆盖率', r'单元测试', r'集成测试'
            ],
            TaskIntent.REVIEWING: [
                r'审查', r'检查', r'review', r'check', r'质量',
                r'quality', r'评审', r'inspect'
            ],
            TaskIntent.REFACTORING: [
                r'重构', r'优化', r'改进', r'refactor', r'optimize',
                r'improve', r'cleanup', r'清理'
            ],
            TaskIntent.DOCUMENTATION: [
                r'文档', r'说明', r'注释', r'document', r'doc',
                r'readme', r'api文档', r'使用指南'
            ],
            TaskIntent.RESEARCH: [
                r'研究', r'调研', r'评估', r'对比', r'research',
                r'evaluate', r'compare', r'分析'
            ],
            TaskIntent.CONTEXT_LOADING: [
                r'加载', r'上下文', r'恢复', r'load', r'context',
                r'prime', r'初始化'
            ]
        }

        # Complexity indicators
        self.complexity_indicators = {
            'high': ['架构', '系统', '重构', '迁移', '集成', 'architecture', 'system', 'migration'],
            'medium': ['模块', '组件', '功能', 'module', 'component', 'feature'],
            'low': ['修复', '添加', '更新', 'fix', 'add', 'update']
        }

    def analyze(self, task_description: str) -> TaskAnalysis:
        """
        Analyze task description and recommend agents

        Args:
            task_description: User's task description

        Returns:
            TaskAnalysis with complete analysis result
        """
        # Step 1: Detect intent
        intent, intent_conf = self._detect_intent(task_description)

        # Step 2: Get agent recommendations
        matches = self.registry.select_agent(task_description, top_k=3)
        primary = matches[0] if matches else None
        fallback = matches[1:] if len(matches) > 1 else []

        # Step 3: Assess complexity
        complexity = self._assess_complexity(task_description)

        # Step 4: Estimate effort
        effort = self._estimate_effort(complexity, intent)

        # Step 5: Extract keywords and technical stack
        keywords = self._extract_keywords(task_description)
        tech_stack = self._extract_technical_stack(task_description)

        # Step 6: Calculate overall confidence
        agent_conf = primary.score if primary else 0.0
        overall_conf = (intent_conf * 0.4 + agent_conf * 0.6)  # Weighted average

        # Step 7: Generate explanation
        explanation = self._generate_explanation(
            intent, primary, complexity, intent_conf, agent_conf
        )

        # Step 8: Generate suggestions
        suggestions = self._generate_suggestions(
            intent, primary, complexity, overall_conf
        )

        return TaskAnalysis(
            task_description=task_description,
            intent=intent,
            intent_confidence=intent_conf,
            primary_agent=primary,
            fallback_agents=fallback,
            complexity=complexity,
            estimated_effort=effort,
            keywords=keywords,
            technical_stack=tech_stack,
            confidence=overall_conf * 100,
            explanation=explanation,
            suggestions=suggestions
        )

    def _detect_intent(self, description: str) -> tuple[TaskIntent, float]:
        """
        Detect primary intent from description

        Returns:
            (intent, confidence)
        """
        desc_lower = description.lower()
        scores = {}

        for intent, patterns in self.intent_patterns.items():
            score = 0.0
            for pattern in patterns:
                if re.search(pattern, desc_lower):
                    score += 1.0

            if score > 0:
                scores[intent] = score / len(patterns)  # Normalize

        if not scores:
            return TaskIntent.UNCLEAR, 0.0

        # Get highest scoring intent
        best_intent = max(scores.items(), key=lambda x: x[1])
        return best_intent[0], best_intent[1]

    def _assess_complexity(self, description: str) -> TaskComplexity:
        """Assess task complexity based on indicators"""
        desc_lower = description.lower()

        # Check for high complexity indicators
        for indicator in self.complexity_indicators['high']:
            if indicator in desc_lower:
                return TaskComplexity.COMPLEX

        # Check for medium complexity indicators
        for indicator in self.complexity_indicators['medium']:
            if indicator in desc_lower:
                return TaskComplexity.MODERATE

        # Default to simple
        return TaskComplexity.SIMPLE

    def _estimate_effort(self, complexity: TaskComplexity, intent: TaskIntent) -> str:
        """Estimate effort based on complexity and intent"""
        base_estimates = {
            TaskComplexity.SIMPLE: "5-15 minutes",
            TaskComplexity.MODERATE: "30 minutes - 1 hour",
            TaskComplexity.COMPLEX: "2-4 hours"
        }

        # Adjust for intent
        if intent in [TaskIntent.RESEARCH, TaskIntent.PLANNING]:
            # Research and planning can be longer
            complexity_map = {
                TaskComplexity.SIMPLE: "15-30 minutes",
                TaskComplexity.MODERATE: "1-2 hours",
                TaskComplexity.COMPLEX: "4-8 hours"
            }
            return complexity_map[complexity]

        return base_estimates[complexity]

    def _extract_keywords(self, description: str) -> List[str]:
        """Extract important keywords from description"""
        # Simple keyword extraction (can be enhanced with NLP)
        words = re.findall(r'\b[a-zA-Z\u4e00-\u9fff]{2,}\b', description)
        # Remove common stop words
        stop_words = {'的', '和', '与', '或', '是', 'the', 'a', 'an', 'and', 'or', 'is'}
        return [w for w in words if w.lower() not in stop_words][:10]

    def _extract_technical_stack(self, description: str) -> List[str]:
        """Extract technical stack mentions from description"""
        # Common tech stack patterns
        tech_patterns = [
            r'Python', r'JavaScript', r'TypeScript', r'React', r'Vue',
            r'Flask', r'Django', r'FastAPI', r'Express', r'Node',
            r'PostgreSQL', r'MongoDB', r'Redis', r'Docker', r'Kubernetes',
            r'JWT', r'OAuth', r'REST', r'GraphQL', r'gRPC'
        ]

        found_tech = []
        for pattern in tech_patterns:
            if re.search(pattern, description, re.IGNORECASE):
                found_tech.append(pattern)

        return found_tech

    def _generate_explanation(
        self,
        intent: TaskIntent,
        primary: Optional[AgentMatch],
        complexity: TaskComplexity,
        intent_conf: float,
        agent_conf: float
    ) -> str:
        """Generate human-readable explanation"""
        parts = []

        # Intent explanation
        if intent_conf > 0.7:
            parts.append(f"检测到明确的 '{intent.value}' 意图")
        elif intent_conf > 0.4:
            parts.append(f"可能是 '{intent.value}' 任务")
        else:
            parts.append("意图不太明确")

        # Agent recommendation
        if primary and agent_conf > 0.8:
            parts.append(f"强烈推荐 {primary.agent.name} ({agent_conf:.0%} 匹配)")
        elif primary:
            parts.append(f"建议使用 {primary.agent.name} ({agent_conf:.0%} 匹配)")
        else:
            parts.append("未找到合适的 agent")

        # Complexity note
        if complexity == TaskComplexity.COMPLEX:
            parts.append("任务较复杂，可能需要多 agent 协作")

        return "；".join(parts) + "。"

    def _generate_suggestions(
        self,
        intent: TaskIntent,
        primary: Optional[AgentMatch],
        complexity: TaskComplexity,
        confidence: float
    ) -> List[str]:
        """Generate actionable suggestions"""
        suggestions = []

        # Low confidence warning
        if confidence < 0.6:
            suggestions.append(
                "⚠️ 信心较低，建议提供更详细的任务描述"
            )

        # Complexity-based suggestions
        if complexity == TaskComplexity.COMPLEX:
            suggestions.append(
                "💡 复杂任务建议先运行 /wf_04_ask 进行架构咨询"
            )

        # Intent-based suggestions
        if intent == TaskIntent.IMPLEMENTATION:
            suggestions.append(
                "✅ 实现完成后记得运行 /wf_07_test 添加测试"
            )
        elif intent == TaskIntent.UNCLEAR:
            suggestions.append(
                "❓ 意图不清楚，请明确是要规划、实现、调试还是其他操作"
            )

        # Agent-specific suggestions
        if primary and primary.agent.name == "code-agent":
            suggestions.append(
                "📝 代码实现后建议运行 /wf_08_review 检查质量"
            )

        return suggestions


def main():
    """CLI interface for testing TaskAnalyzer"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: task_analyzer.py <task_description>")
        print("\nExample:")
        print("  python task_analyzer.py '实现用户登录功能'")
        print("  python task_analyzer.py '修复支付API的bug'")
        print("  python task_analyzer.py '设计数据库架构'")
        sys.exit(1)

    task = ' '.join(sys.argv[1:])

    print(f"Analyzing task: {task}\n")

    analyzer = TaskAnalyzer()
    analysis = analyzer.analyze(task)

    print(analysis)

    if analysis.fallback_agents:
        print("Fallback Options:")
        for i, match in enumerate(analysis.fallback_agents, 1):
            print(f"  {i}. {match}")

    if analysis.suggestions:
        print("\nSuggestions:")
        for suggestion in analysis.suggestions:
            print(f"  {suggestion}")


if __name__ == '__main__':
    main()
