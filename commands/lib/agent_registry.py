#!/usr/bin/env python3
"""
Agent Registry - Central management and routing for AI Workflow agents

This module provides intelligent agent selection, auto-activation, and
multi-agent coordination for the AI Workflow system.

Design Principles:
- Single Source of Truth: All agent definitions in commands/agents/*.md
- Keyword-based matching with confidence scoring
- Scenario-based activation detection
- Support for sequential, parallel, and hierarchical coordination
- MCP integration awareness per agent

Usage:
    from commands.lib.agent_registry import AgentRegistry

    registry = AgentRegistry()
    agent = registry.select_agent("实现用户登录功能")
    print(f"Selected: {agent.name} (confidence: {agent.score})")
"""

import os
import re
import yaml
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Agent:
    """Agent metadata and configuration"""
    name: str
    role: str
    description: str
    expertise: List[str]
    activation_keywords: List[str]
    activation_scenarios: List[str]
    available_tools: List[str]
    mcp_integrations: List[Dict[str, str]]
    collaboration_modes: List[Dict[str, str]]
    workflows: List[Dict[str, any]]
    decision_criteria: Dict[str, any]
    status: str
    priority: str
    file_path: str

    def __str__(self) -> str:
        return f"{self.name} ({self.role})"


@dataclass
class AgentMatch:
    """Agent match result with confidence score"""
    agent: Agent
    score: float
    matched_keywords: List[str]
    matched_scenarios: List[str]
    reason: str

    def __str__(self) -> str:
        return f"{self.agent.name}: {self.score:.2f} - {self.reason}"


class AgentRegistry:
    """
    Central registry for agent management and intelligent routing

    Features:
    - Auto-loads all agent definitions from commands/agents/
    - Keyword-based matching with fuzzy logic
    - Scenario detection and confidence scoring
    - Multi-agent coordination support
    - MCP integration awareness
    """

    def __init__(self, agents_dir: Optional[str] = None):
        """
        Initialize agent registry

        Args:
            agents_dir: Path to agents directory (default: commands/agents/)
        """
        if agents_dir is None:
            # Auto-detect agents directory relative to this file
            current_dir = Path(__file__).parent.parent
            agents_dir = current_dir / "agents"

        self.agents_dir = Path(agents_dir)
        self.agents: Dict[str, Agent] = {}
        self._load_agents()

    def _load_agents(self) -> None:
        """Load all agent definitions from markdown files"""
        if not self.agents_dir.exists():
            raise FileNotFoundError(f"Agents directory not found: {self.agents_dir}")

        for md_file in self.agents_dir.glob("*_agent.md"):
            try:
                agent = self._parse_agent_file(md_file)
                self.agents[agent.name] = agent
            except Exception as e:
                print(f"Warning: Failed to load {md_file.name}: {e}")

        print(f"Loaded {len(self.agents)} agents from {self.agents_dir}")

    def _parse_agent_file(self, file_path: Path) -> Agent:
        """Parse agent definition from markdown file with YAML frontmatter"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML frontmatter
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not match:
            raise ValueError(f"No YAML frontmatter found in {file_path.name}")

        frontmatter = yaml.safe_load(match.group(1))

        return Agent(
            name=frontmatter['agent_name'],
            role=frontmatter['role'],
            description=frontmatter['description'],
            expertise=frontmatter.get('expertise', []),
            activation_keywords=frontmatter.get('activation_keywords', []),
            activation_scenarios=frontmatter.get('activation_scenarios', []),
            available_tools=frontmatter.get('available_tools', []),
            mcp_integrations=frontmatter.get('mcp_integrations', []),
            collaboration_modes=frontmatter.get('collaboration_modes', []),
            workflows=frontmatter.get('workflows', []),
            decision_criteria=frontmatter.get('decision_criteria', {}),
            status=frontmatter.get('status', 'active'),
            priority=frontmatter.get('priority', 'medium'),
            file_path=str(file_path)
        )

    def select_agent(self, task_description: str, top_k: int = 1) -> List[AgentMatch]:
        """
        Select best agent(s) for a given task description

        Args:
            task_description: User's task description or request
            top_k: Number of top matches to return (default: 1)

        Returns:
            List of AgentMatch objects sorted by confidence score
        """
        matches = []

        for agent in self.agents.values():
            if agent.status != 'active':
                continue

            score, matched_kw, matched_sc, reason = self._calculate_match_score(
                agent, task_description
            )

            if score > 0:
                matches.append(AgentMatch(
                    agent=agent,
                    score=score,
                    matched_keywords=matched_kw,
                    matched_scenarios=matched_sc,
                    reason=reason
                ))

        # Sort by score (descending) and priority (critical > high > medium > low)
        priority_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        matches.sort(
            key=lambda m: (m.score, priority_order.get(m.agent.priority, 0)),
            reverse=True
        )

        return matches[:top_k]

    def _contains_chinese(self, text: str) -> bool:
        """检测文本是否包含中文字符"""
        import re
        return bool(re.search(r'[\u4e00-\u9fff]', text))

    def _calculate_match_score(
        self, agent: Agent, task_description: str
    ) -> Tuple[float, List[str], List[str], str]:
        """
        Calculate match score for an agent against task description

        Scoring logic:
        - Keyword match: +0.3 per keyword (max 0.6)
        - Scenario match: +0.4 per scenario (max 0.4)
        - Priority boost: critical=+0.1, high=+0.05

        Returns:
            (score, matched_keywords, matched_scenarios, reason)
        """
        task_lower = task_description.lower()
        score = 0.0
        matched_kw = []
        matched_sc = []
        reasons = []

        # 1. Keyword matching (max 0.6)
        keyword_score = 0.0
        for keyword in agent.activation_keywords:
            if keyword.lower() in task_lower:
                keyword_score += 0.3
                matched_kw.append(keyword)
        keyword_score = min(keyword_score, 0.6)
        score += keyword_score

        if matched_kw:
            reasons.append(f"关键词匹配: {', '.join(matched_kw)}")

        # 2. Scenario matching (max 0.4)
        scenario_score = 0.0
        for scenario in agent.activation_scenarios:
            # 智能匹配：中文使用模糊匹配，英文使用单词匹配
            is_matched = False

            if self._contains_chinese(scenario) or self._contains_chinese(task_lower):
                # 中文场景：使用模糊匹配策略
                # 策略1: 场景包含在任务中（子串）
                # 策略2: 提取关键字符，检查足够多的字符出现在任务中
                import re

                # 移除空格和标点，只保留中文和英文字母数字
                scenario_clean = re.sub(r'[^\u4e00-\u9fffa-zA-Z0-9]', '', scenario.lower())
                task_clean = re.sub(r'[^\u4e00-\u9fffa-zA-Z0-9]', '', task_lower)

                # 策略1: 简单包含检查
                if scenario_clean in task_clean or task_clean in scenario_clean:
                    is_matched = True
                else:
                    # 策略2: 字符匹配度检查（至少70%的场景字符出现在任务中）
                    matched_count = sum(1 for char in scenario_clean if char in task_clean)
                    if len(scenario_clean) > 0:
                        match_ratio = matched_count / len(scenario_clean)
                        is_matched = match_ratio >= 0.7
            else:
                # 英文场景：使用单词交集匹配
                scenario_words = set(scenario.lower().split())
                task_words = set(task_lower.split())
                is_matched = bool(scenario_words & task_words)

            if is_matched:
                scenario_score += 0.4
                matched_sc.append(scenario)

        scenario_score = min(scenario_score, 0.4)
        score += scenario_score

        if matched_sc:
            reasons.append(f"场景匹配: {matched_sc[0]}")

        # 3. Priority boost
        if agent.priority == 'critical':
            score += 0.1
            reasons.append("关键级优先")
        elif agent.priority == 'high':
            score += 0.05
            reasons.append("高优先级")

        # 4. Check confidence threshold
        threshold = agent.decision_criteria.get('confidence_threshold', 0.80)
        if score >= threshold:
            reasons.append(f"超过阈值 {threshold}")

        reason = "; ".join(reasons) if reasons else "无匹配"

        return score, matched_kw, matched_sc, reason

    def should_auto_activate(self, agent_name: str, task_description: str) -> bool:
        """
        Check if an agent should auto-activate for a task

        Args:
            agent_name: Name of the agent to check
            task_description: User's task description

        Returns:
            True if agent should auto-activate
        """
        agent = self.agents.get(agent_name)
        if not agent or agent.status != 'active':
            return False

        score, _, _, _ = self._calculate_match_score(agent, task_description)
        threshold = agent.decision_criteria.get('confidence_threshold', 0.80)

        return score >= threshold

    def get_agent(self, agent_name: str) -> Optional[Agent]:
        """Get agent by name"""
        return self.agents.get(agent_name)

    def list_agents(self, status: Optional[str] = None) -> List[Agent]:
        """
        List all agents, optionally filtered by status

        Args:
            status: Filter by status ('active', 'inactive', etc.)

        Returns:
            List of Agent objects
        """
        agents = list(self.agents.values())

        if status:
            agents = [a for a in agents if a.status == status]

        return agents

    def get_collaborators(self, agent_name: str) -> List[Dict[str, str]]:
        """
        Get collaboration modes for an agent

        Args:
            agent_name: Name of the agent

        Returns:
            List of collaboration mode definitions
        """
        agent = self.agents.get(agent_name)
        if not agent:
            return []

        return agent.collaboration_modes

    def get_mcp_integrations(self, agent_name: str) -> List[Dict[str, str]]:
        """
        Get MCP integrations for an agent

        Args:
            agent_name: Name of the agent

        Returns:
            List of MCP integration definitions
        """
        agent = self.agents.get(agent_name)
        if not agent:
            return []

        return agent.mcp_integrations

    def suggest_workflow(self, task_description: str) -> Dict[str, any]:
        """
        Suggest a multi-agent workflow for a task

        Args:
            task_description: User's task description

        Returns:
            Dictionary with workflow suggestion
        """
        matches = self.select_agent(task_description, top_k=3)

        if not matches:
            return {
                'primary_agent': None,
                'collaborators': [],
                'workflow': 'sequential',
                'confidence': 0.0
            }

        primary = matches[0]
        collaborators = []

        # Get collaborators for primary agent
        for collab in primary.agent.collaboration_modes:
            collab_agent_name = collab.get('agent')
            if collab_agent_name in self.agents:
                collaborators.append({
                    'agent': self.agents[collab_agent_name],
                    'mode': collab.get('mode'),
                    'scenario': collab.get('scenario')
                })

        return {
            'primary_agent': primary.agent,
            'primary_score': primary.score,
            'collaborators': collaborators,
            'workflow': 'sequential' if collaborators else 'single',
            'confidence': primary.score,
            'reason': primary.reason
        }


def main():
    """CLI interface for testing AgentRegistry"""
    import sys

    registry = AgentRegistry()

    if len(sys.argv) < 2:
        print("Usage: agent_registry.py <task_description>")
        print("\nExample:")
        print("  python agent_registry.py '实现用户登录功能'")
        print("  python agent_registry.py '代码审查'")
        print("  python agent_registry.py '性能优化'")
        print(f"\nLoaded agents: {', '.join(registry.agents.keys())}")
        sys.exit(1)

    task = ' '.join(sys.argv[1:])

    print(f"Task: {task}\n")

    # Select best agent
    matches = registry.select_agent(task, top_k=3)

    if not matches:
        print("No matching agents found.")
        sys.exit(0)

    print("Top Matches:")
    for i, match in enumerate(matches, 1):
        print(f"{i}. {match.agent.name} ({match.agent.role})")
        print(f"   Score: {match.score:.2f}")
        print(f"   Reason: {match.reason}")
        print(f"   Keywords: {', '.join(match.matched_keywords)}")
        if match.matched_scenarios:
            print(f"   Scenarios: {', '.join(match.matched_scenarios)}")
        print()

    # Suggest workflow
    print("Suggested Workflow:")
    workflow = registry.suggest_workflow(task)
    print(f"Primary: {workflow['primary_agent']}")
    print(f"Confidence: {workflow['primary_score']:.2f}")
    print(f"Workflow Type: {workflow['workflow']}")

    if workflow['collaborators']:
        print("\nCollaborators:")
        for collab in workflow['collaborators']:
            print(f"  - {collab['agent'].name} ({collab['mode']} mode)")
            print(f"    Scenario: {collab['scenario']}")


if __name__ == '__main__':
    main()
