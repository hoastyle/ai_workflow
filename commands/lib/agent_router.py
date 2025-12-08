#!/usr/bin/env python3
"""
Agent Router - Multi-agent coordination and workflow orchestration

This module provides intelligent routing and coordination for multiple agents
working together on complex tasks.

Design Principles:
- Support three coordination modes: sequential, parallel, hierarchical
- Dynamic workflow generation based on task complexity
- Conflict detection and resolution
- Progress tracking across multiple agents
- Graceful degradation when agents fail

Usage:
    from commands.lib.agent_router import AgentRouter
    from commands.lib.agent_registry import AgentRegistry

    registry = AgentRegistry()
    router = AgentRouter(registry)

    workflow = router.route("实现用户认证系统")
    print(f"Workflow: {workflow['mode']}")
    print(f"Agents: {[a.name for a in workflow['agents']]}")
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum

from commands.lib.agent_registry import AgentRegistry, Agent, AgentMatch


class CoordinationMode(Enum):
    """Agent coordination modes"""
    SINGLE = "single"           # Single agent handles the task
    SEQUENTIAL = "sequential"   # Agents work in sequence (A → B → C)
    PARALLEL = "parallel"       # Agents work in parallel (A ‖ B ‖ C)
    HIERARCHICAL = "hierarchical"  # Coordinator delegates to workers


@dataclass
class WorkflowStep:
    """A single step in a multi-agent workflow"""
    agent: Agent
    role: str  # "primary", "collaborator", "coordinator", "worker"
    dependencies: List[str]  # List of agent names this step depends on
    parallel_group: Optional[int] = None  # For parallel execution grouping


@dataclass
class AgentWorkflow:
    """Complete multi-agent workflow definition"""
    mode: CoordinationMode
    primary_agent: Agent
    steps: List[WorkflowStep]
    estimated_time: str
    confidence: float
    explanation: str

    def __str__(self) -> str:
        steps_str = "\n".join([
            f"  {i+1}. {step.agent.name} ({step.role})"
            for i, step in enumerate(self.steps)
        ])
        return f"""
Workflow: {self.mode.value}
Primary Agent: {self.primary_agent.name}
Confidence: {self.confidence:.0%}

Steps:
{steps_str}

Estimated Time: {self.estimated_time}
Explanation: {self.explanation}
"""


class AgentRouter:
    """
    Multi-agent coordination and workflow orchestration

    Features:
    - Automatic workflow generation based on task complexity
    - Three coordination modes (single, sequential, parallel, hierarchical)
    - Intelligent agent selection and ordering
    - Conflict detection and resolution
    - Progress tracking
    """

    def __init__(self, registry: Optional[AgentRegistry] = None):
        """
        Initialize agent router

        Args:
            registry: AgentRegistry instance (creates new if None)
        """
        self.registry = registry or AgentRegistry()

    def route(self, task_description: str, mode: Optional[str] = None) -> AgentWorkflow:
        """
        Route a task to appropriate agents and generate workflow

        Args:
            task_description: User's task description
            mode: Optional override for coordination mode
                  ("single", "sequential", "parallel", "hierarchical")

        Returns:
            AgentWorkflow with complete execution plan
        """
        # Step 1: Get primary agent and collaborators
        matches = self.registry.select_agent(task_description, top_k=3)

        if not matches:
            raise ValueError("No suitable agents found for task")

        primary_match = matches[0]
        primary_agent = primary_match.agent

        # Step 2: Determine coordination mode
        if mode:
            coord_mode = CoordinationMode(mode)
        else:
            coord_mode = self._determine_coordination_mode(
                task_description, primary_agent, matches
            )

        # Step 3: Generate workflow based on mode
        if coord_mode == CoordinationMode.SINGLE:
            workflow = self._create_single_workflow(primary_match)
        elif coord_mode == CoordinationMode.SEQUENTIAL:
            workflow = self._create_sequential_workflow(primary_match, task_description)
        elif coord_mode == CoordinationMode.PARALLEL:
            workflow = self._create_parallel_workflow(primary_match, task_description)
        else:  # HIERARCHICAL
            workflow = self._create_hierarchical_workflow(primary_match, task_description)

        return workflow

    def _determine_coordination_mode(
        self,
        task_description: str,
        primary_agent: Agent,
        matches: List[AgentMatch]
    ) -> CoordinationMode:
        """
        Automatically determine the best coordination mode

        Logic:
        - Single: Simple task, high confidence primary agent
        - Sequential: Multi-step task requiring different expertise
        - Parallel: Independent sub-tasks that can run concurrently
        - Hierarchical: Complex task requiring PM coordination
        """
        desc_lower = task_description.lower()

        # Check for hierarchical indicators
        hierarchical_keywords = [
            '系统', '架构', '完整', '端到端', 'system', 'architecture', 'complete', 'full'
        ]
        if any(kw in desc_lower for kw in hierarchical_keywords):
            return CoordinationMode.HIERARCHICAL

        # Check for parallel indicators
        parallel_keywords = [
            '同时', '并行', '多个', 'parallel', 'multiple', 'concurrent'
        ]
        if any(kw in desc_lower for kw in parallel_keywords):
            return CoordinationMode.PARALLEL

        # Check if primary agent has collaborators defined
        if primary_agent.collaboration_modes:
            # Check for sequential collaboration patterns
            sequential_modes = [
                c for c in primary_agent.collaboration_modes
                if c.get('mode') == 'sequential'
            ]
            if sequential_modes:
                return CoordinationMode.SEQUENTIAL

        # Default to single if high confidence
        if matches[0].score >= 0.90:
            return CoordinationMode.SINGLE

        # Otherwise sequential (safest multi-agent mode)
        return CoordinationMode.SEQUENTIAL

    def _create_single_workflow(self, primary_match: AgentMatch) -> AgentWorkflow:
        """Create workflow for single agent"""
        step = WorkflowStep(
            agent=primary_match.agent,
            role="primary",
            dependencies=[]
        )

        return AgentWorkflow(
            mode=CoordinationMode.SINGLE,
            primary_agent=primary_match.agent,
            steps=[step],
            estimated_time=self._estimate_time([step]),
            confidence=primary_match.score,
            explanation=f"{primary_match.agent.name} can handle this task independently"
        )

    def _create_sequential_workflow(
        self,
        primary_match: AgentMatch,
        task_description: str
    ) -> AgentWorkflow:
        """
        Create sequential workflow (A → B → C)

        Example: Architect → Code → Test → Review
        """
        steps = []
        primary_agent = primary_match.agent

        # Step 1: Primary agent
        steps.append(WorkflowStep(
            agent=primary_agent,
            role="primary",
            dependencies=[]
        ))

        # Step 2-N: Add collaborators in sequence
        for collab in primary_agent.collaboration_modes:
            if collab.get('mode') != 'sequential':
                continue

            collab_agent_name = collab.get('agent')
            collab_agent = self.registry.get_agent(collab_agent_name)

            if collab_agent and collab_agent.status == 'active':
                steps.append(WorkflowStep(
                    agent=collab_agent,
                    role="collaborator",
                    dependencies=[steps[-1].agent.name]  # Depends on previous
                ))

        return AgentWorkflow(
            mode=CoordinationMode.SEQUENTIAL,
            primary_agent=primary_agent,
            steps=steps,
            estimated_time=self._estimate_time(steps),
            confidence=primary_match.score * 0.95,  # Slight reduction for coordination
            explanation=f"Sequential workflow: {' → '.join([s.agent.name for s in steps])}"
        )

    def _create_parallel_workflow(
        self,
        primary_match: AgentMatch,
        task_description: str
    ) -> AgentWorkflow:
        """
        Create parallel workflow (A ‖ B ‖ C → Merge)

        Example: Multiple reviewers analyzing different aspects simultaneously
        """
        steps = []
        primary_agent = primary_match.agent

        # Step 1: Primary agent (coordinator)
        coordinator_step = WorkflowStep(
            agent=primary_agent,
            role="coordinator",
            dependencies=[]
        )
        steps.append(coordinator_step)

        # Step 2: Parallel workers
        parallel_agents = []
        for collab in primary_agent.collaboration_modes:
            if collab.get('mode') != 'parallel':
                continue

            collab_agent_name = collab.get('agent')
            collab_agent = self.registry.get_agent(collab_agent_name)

            if collab_agent and collab_agent.status == 'active':
                parallel_agents.append(collab_agent)

        # Add parallel workers (all depend on coordinator, all in group 1)
        for agent in parallel_agents:
            steps.append(WorkflowStep(
                agent=agent,
                role="worker",
                dependencies=[coordinator_step.agent.name],
                parallel_group=1
            ))

        # Step 3: Merge step (primary agent consolidates results)
        if parallel_agents:
            steps.append(WorkflowStep(
                agent=primary_agent,
                role="primary",
                dependencies=[a.name for a in parallel_agents]
            ))

        return AgentWorkflow(
            mode=CoordinationMode.PARALLEL,
            primary_agent=primary_agent,
            steps=steps,
            estimated_time=self._estimate_time(steps, parallel=True),
            confidence=primary_match.score * 0.90,  # Reduction for coordination complexity
            explanation=f"Parallel workflow with {len(parallel_agents)} concurrent agents"
        )

    def _create_hierarchical_workflow(
        self,
        primary_match: AgentMatch,
        task_description: str
    ) -> AgentWorkflow:
        """
        Create hierarchical workflow (PM → {Worker1, Worker2, ...})

        Example: PM agent coordinates multiple specialized agents
        """
        steps = []

        # Always use PM agent as coordinator for hierarchical mode
        pm_agent = self.registry.get_agent("pm-agent")

        if not pm_agent:
            # Fallback to sequential if PM agent not available
            return self._create_sequential_workflow(primary_match, task_description)

        # Step 1: PM agent as coordinator
        coordinator_step = WorkflowStep(
            agent=pm_agent,
            role="coordinator",
            dependencies=[]
        )
        steps.append(coordinator_step)

        # Step 2: Identify worker agents based on task
        # Get top 3 agents for the task
        matches = self.registry.select_agent(task_description, top_k=3)

        # Add workers
        for match in matches:
            if match.agent.name != "pm-agent":  # Don't duplicate PM
                steps.append(WorkflowStep(
                    agent=match.agent,
                    role="worker",
                    dependencies=[pm_agent.name],
                    parallel_group=1  # Workers can work in parallel
                ))

        # Step 3: PM consolidates and validates
        worker_names = [s.agent.name for s in steps if s.role == "worker"]
        if worker_names:
            steps.append(WorkflowStep(
                agent=pm_agent,
                role="primary",
                dependencies=worker_names
            ))

        return AgentWorkflow(
            mode=CoordinationMode.HIERARCHICAL,
            primary_agent=pm_agent,
            steps=steps,
            estimated_time=self._estimate_time(steps, parallel=True),
            confidence=primary_match.score * 0.85,  # More coordination = higher risk
            explanation=f"PM coordinates {len(worker_names)} specialized agents"
        )

    def _estimate_time(self, steps: List[WorkflowStep], parallel: bool = False) -> str:
        """
        Estimate total workflow execution time

        Args:
            steps: List of workflow steps
            parallel: Whether parallel execution is involved
        """
        if len(steps) == 1:
            return "15-30 minutes"

        if parallel:
            # Parallel workflows take time of longest branch + coordination overhead
            return f"{30 * len(steps)}-{60 * len(steps)} minutes"
        else:
            # Sequential workflows accumulate time
            return f"{20 * len(steps)}-{40 * len(steps)} minutes"

    def suggest_manual_override(self, user_input: str) -> Optional[Dict[str, str]]:
        """
        Parse manual agent override syntax: @agent-name "task description"

        Args:
            user_input: User's input string

        Returns:
            Dict with 'agent' and 'task' if override detected, None otherwise
        """
        import re

        # Pattern: @agent-name "task description"
        pattern = r'@([\w-]+)\s+"([^"]+)"'
        match = re.match(pattern, user_input.strip())

        if match:
            agent_name = match.group(1)
            task_desc = match.group(2)

            # Verify agent exists
            if self.registry.get_agent(agent_name):
                return {
                    'agent': agent_name,
                    'task': task_desc
                }

        return None

    def detect_conflicts(self, steps: List[WorkflowStep]) -> List[str]:
        """
        Detect potential conflicts in workflow

        Returns:
            List of conflict warnings
        """
        conflicts = []

        # Check for duplicate agents
        agent_names = [s.agent.name for s in steps]
        duplicates = [name for name in agent_names if agent_names.count(name) > 1]
        if duplicates:
            conflicts.append(f"Duplicate agents detected: {set(duplicates)}")

        # Check for circular dependencies
        dependencies_map = {s.agent.name: s.dependencies for s in steps}
        for agent_name, deps in dependencies_map.items():
            if agent_name in deps:
                conflicts.append(f"Circular dependency: {agent_name} depends on itself")

        return conflicts


def main():
    """CLI interface for testing AgentRouter"""
    import sys

    router = AgentRouter()

    if len(sys.argv) < 2:
        print("Usage: agent_router.py <task_description> [mode]")
        print("\nModes: single, sequential, parallel, hierarchical")
        print("\nExamples:")
        print('  python agent_router.py "实现用户登录功能"')
        print('  python agent_router.py "代码审查" sequential')
        print('  python agent_router.py "@architect-agent \\"设计系统架构\\""')
        sys.exit(1)

    task = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else None

    # Check for manual override
    override = router.suggest_manual_override(task)
    if override:
        print(f"Manual Override Detected:")
        print(f"  Agent: {override['agent']}")
        print(f"  Task: {override['task']}")
        print()
        task = override['task']
        # Route to specific agent by setting primary
        primary = router.registry.get_agent(override['agent'])
        if primary:
            from commands.lib.agent_registry import AgentMatch
            primary_match = AgentMatch(
                agent=primary,
                score=1.0,
                matched_keywords=[],
                matched_scenarios=[],
                reason="Manual override"
            )
            workflow = router._create_single_workflow(primary_match)
        else:
            print(f"Error: Agent '{override['agent']}' not found")
            sys.exit(1)
    else:
        # Normal routing
        workflow = router.route(task, mode=mode)

    print(workflow)

    # Check for conflicts
    conflicts = router.detect_conflicts(workflow.steps)
    if conflicts:
        print("\n⚠️  Potential Conflicts:")
        for conflict in conflicts:
            print(f"  - {conflict}")


if __name__ == '__main__':
    main()
