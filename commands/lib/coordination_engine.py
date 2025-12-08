#!/usr/bin/env python3
"""
Coordination Engine - Multi-agent workflow execution and orchestration

This module implements the execution layer for multi-agent workflows,
coordinating the execution of multiple agents working together on complex tasks.

Design Principles:
- Support three coordination modes: sequential, parallel, hierarchical
- Progress tracking and cancellation support
- Conflict detection and resolution
- Graceful error handling and recovery
- Result aggregation and validation

Usage:
    from commands.lib.coordination_engine import CoordinationEngine
    from commands.lib.agent_router import AgentRouter

    router = AgentRouter()
    workflow = router.route("实现用户认证系统")

    engine = CoordinationEngine()
    result = engine.execute(workflow)
    print(f"Status: {result.status}")
    print(f"Output: {result.output}")
"""

import time
from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

from commands.lib.agent_router import AgentWorkflow, WorkflowStep
from commands.lib.agent_registry import Agent


class ExecutionStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"       # Not started
    RUNNING = "running"       # Currently executing
    COMPLETED = "completed"   # Successfully completed
    FAILED = "failed"         # Execution failed
    CANCELLED = "cancelled"   # User cancelled
    PAUSED = "paused"         # Paused for user input


@dataclass
class StepResult:
    """Result of a single workflow step execution"""
    step: WorkflowStep
    status: ExecutionStatus
    output: str
    error: Optional[str] = None
    duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        status_emoji = {
            ExecutionStatus.COMPLETED: "✅",
            ExecutionStatus.FAILED: "❌",
            ExecutionStatus.RUNNING: "🔄",
            ExecutionStatus.PENDING: "⏳",
            ExecutionStatus.CANCELLED: "🚫"
        }
        emoji = status_emoji.get(self.status, "❓")
        return f"{emoji} {self.step.agent.name} ({self.status.value})"


@dataclass
class ExecutionResult:
    """Result of complete workflow execution"""
    workflow: AgentWorkflow
    status: ExecutionStatus
    step_results: List[StepResult]
    output: str
    conflicts: List[str] = field(default_factory=list)
    total_duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        steps_summary = "\n".join([f"  {r}" for r in self.step_results])
        return f"""
Workflow Execution: {self.status.value}
Mode: {self.workflow.mode.value}
Duration: {self.total_duration:.2f}s

Steps:
{steps_summary}

Output:
{self.output[:500]}...
"""

    def get_failed_steps(self) -> List[StepResult]:
        """Get all failed steps"""
        return [r for r in self.step_results if r.status == ExecutionStatus.FAILED]

    def get_completed_steps(self) -> List[StepResult]:
        """Get all completed steps"""
        return [r for r in self.step_results if r.status == ExecutionStatus.COMPLETED]


class CoordinationEngine:
    """
    Multi-agent coordination and workflow execution engine

    Features:
    - Sequential execution: Agents execute in order
    - Parallel execution: Agents execute concurrently (simulated)
    - Hierarchical execution: PM coordinates workers
    - Progress tracking with callbacks
    - Conflict detection and resolution
    - Error handling and recovery
    """

    def __init__(self, progress_callback: Optional[Callable[[str, float], None]] = None):
        """
        Initialize coordination engine

        Args:
            progress_callback: Optional callback(message, progress) for progress updates
        """
        self.progress_callback = progress_callback
        self._cancel_requested = False

    def execute(self, workflow: AgentWorkflow) -> ExecutionResult:
        """
        Execute a multi-agent workflow

        Args:
            workflow: AgentWorkflow to execute

        Returns:
            ExecutionResult with complete execution information
        """
        start_time = time.time()
        self._cancel_requested = False

        self._report_progress(f"Starting {workflow.mode.value} workflow with {len(workflow.steps)} steps", 0.0)

        try:
            # Execute based on coordination mode
            if workflow.mode.value == "single":
                step_results = self._execute_single(workflow)
            elif workflow.mode.value == "sequential":
                step_results = self._execute_sequential(workflow)
            elif workflow.mode.value == "parallel":
                step_results = self._execute_parallel(workflow)
            elif workflow.mode.value == "hierarchical":
                step_results = self._execute_hierarchical(workflow)
            else:
                raise ValueError(f"Unknown coordination mode: {workflow.mode}")

            # Check if cancelled
            if self._cancel_requested:
                status = ExecutionStatus.CANCELLED
                output = "Workflow execution cancelled by user"
            else:
                # Determine overall status
                failed = [r for r in step_results if r.status == ExecutionStatus.FAILED]
                if failed:
                    status = ExecutionStatus.FAILED
                    output = f"Workflow failed at step: {failed[0].step.agent.name}\nError: {failed[0].error}"
                else:
                    status = ExecutionStatus.COMPLETED
                    output = self._aggregate_outputs(step_results)

            # Detect conflicts
            conflicts = self._detect_output_conflicts(step_results)

            duration = time.time() - start_time
            self._report_progress(f"Workflow {status.value}", 1.0)

            return ExecutionResult(
                workflow=workflow,
                status=status,
                step_results=step_results,
                output=output,
                conflicts=conflicts,
                total_duration=duration
            )

        except Exception as e:
            duration = time.time() - start_time
            return ExecutionResult(
                workflow=workflow,
                status=ExecutionStatus.FAILED,
                step_results=[],
                output=f"Workflow execution failed: {str(e)}",
                total_duration=duration
            )

    def cancel(self):
        """Request cancellation of current execution"""
        self._cancel_requested = True

    def _execute_single(self, workflow: AgentWorkflow) -> List[StepResult]:
        """Execute single-agent workflow"""
        step = workflow.steps[0]
        self._report_progress(f"Executing {step.agent.name}", 0.5)

        result = self._execute_step(step, {})

        self._report_progress(f"Completed {step.agent.name}", 1.0)
        return [result]

    def _execute_sequential(self, workflow: AgentWorkflow) -> List[StepResult]:
        """
        Execute sequential workflow (A → B → C)

        Each agent receives outputs from previous agents
        """
        results = []
        context = {}  # Shared context between steps

        for i, step in enumerate(workflow.steps):
            if self._cancel_requested:
                break

            progress = (i + 1) / len(workflow.steps)
            self._report_progress(f"Step {i+1}/{len(workflow.steps)}: {step.agent.name}", progress)

            # Execute step with accumulated context
            result = self._execute_step(step, context)
            results.append(result)

            # Update context for next step
            if result.status == ExecutionStatus.COMPLETED:
                context[step.agent.name] = result.output
            else:
                # Stop on failure
                break

        return results

    def _execute_parallel(self, workflow: AgentWorkflow) -> List[StepResult]:
        """
        Execute parallel workflow (A ‖ B ‖ C → Merge)

        Simulates parallel execution (actual parallel execution would require threading)
        """
        results = []

        # Step 1: Coordinator setup
        if workflow.steps[0].role == "coordinator":
            coordinator_step = workflow.steps[0]
            self._report_progress(f"Coordinator: {coordinator_step.agent.name}", 0.1)

            coordinator_result = self._execute_step(coordinator_step, {})
            results.append(coordinator_result)

            context = {coordinator_step.agent.name: coordinator_result.output}
        else:
            context = {}

        # Step 2: Parallel workers (simulated as sequential for now)
        worker_steps = [s for s in workflow.steps if s.role == "worker"]

        for i, step in enumerate(worker_steps):
            if self._cancel_requested:
                break

            progress = 0.1 + (0.7 * (i + 1) / len(worker_steps))
            self._report_progress(f"Worker {i+1}/{len(worker_steps)}: {step.agent.name}", progress)

            result = self._execute_step(step, context)
            results.append(result)

            # Update context
            context[step.agent.name] = result.output

        # Step 3: Merge step (if exists)
        merge_steps = [s for s in workflow.steps if s.role == "primary" and s not in worker_steps]
        if merge_steps:
            merge_step = merge_steps[0]
            self._report_progress(f"Merging results: {merge_step.agent.name}", 0.9)

            merge_result = self._execute_step(merge_step, context)
            results.append(merge_result)

        return results

    def _execute_hierarchical(self, workflow: AgentWorkflow) -> List[StepResult]:
        """
        Execute hierarchical workflow (PM → {Worker1, Worker2, ...} → PM)

        PM agent coordinates workers and validates outputs
        """
        results = []

        # Step 1: PM coordination
        coordinator_step = workflow.steps[0]
        self._report_progress(f"PM Coordination: {coordinator_step.agent.name}", 0.1)

        coordinator_result = self._execute_step(coordinator_step, {})
        results.append(coordinator_result)

        context = {coordinator_step.agent.name: coordinator_result.output}

        # Step 2: Worker execution (parallel group 1)
        worker_steps = [s for s in workflow.steps if s.role == "worker"]

        for i, step in enumerate(worker_steps):
            if self._cancel_requested:
                break

            progress = 0.1 + (0.6 * (i + 1) / len(worker_steps))
            self._report_progress(f"Worker {i+1}/{len(worker_steps)}: {step.agent.name}", progress)

            result = self._execute_step(step, context)
            results.append(result)

            context[step.agent.name] = result.output

        # Step 3: PM consolidation
        consolidation_steps = [s for s in workflow.steps if s.role == "primary"]
        if consolidation_steps:
            consolidation_step = consolidation_steps[0]
            self._report_progress(f"PM Consolidation: {consolidation_step.agent.name}", 0.9)

            consolidation_result = self._execute_step(consolidation_step, context)
            results.append(consolidation_result)

        return results

    def _execute_step(self, step: WorkflowStep, context: Dict[str, str]) -> StepResult:
        """
        Execute a single workflow step

        Args:
            step: WorkflowStep to execute
            context: Context from previous steps

        Returns:
            StepResult with execution information
        """
        start_time = time.time()

        try:
            # Simulate agent execution
            # In real implementation, this would call the actual agent
            output = self._simulate_agent_execution(step, context)

            duration = time.time() - start_time

            return StepResult(
                step=step,
                status=ExecutionStatus.COMPLETED,
                output=output,
                duration=duration,
                metadata={"context_size": len(context)}
            )

        except Exception as e:
            duration = time.time() - start_time

            return StepResult(
                step=step,
                status=ExecutionStatus.FAILED,
                output="",
                error=str(e),
                duration=duration
            )

    def _simulate_agent_execution(self, step: WorkflowStep, context: Dict[str, str]) -> str:
        """
        Simulate agent execution (placeholder for actual implementation)

        In real implementation, this would:
        1. Load agent's prompt and tools
        2. Prepare context with previous outputs
        3. Execute agent's workflow
        4. Return result
        """
        agent_name = step.agent.name
        role = step.role
        dependencies = step.dependencies

        # Build context summary
        context_summary = ""
        if dependencies:
            context_summary = "\n".join([
                f"  - {dep}: {context.get(dep, 'N/A')[:100]}..."
                for dep in dependencies
            ])

        output = f"""
[{agent_name}] ({role})
Dependencies: {', '.join(dependencies) if dependencies else 'None'}

Context:
{context_summary}

Execution: Successfully processed task
Status: ✅ Completed
"""
        return output.strip()

    def _aggregate_outputs(self, results: List[StepResult]) -> str:
        """
        Aggregate outputs from multiple steps into final result

        Args:
            results: List of StepResult objects

        Returns:
            Aggregated output string
        """
        completed = [r for r in results if r.status == ExecutionStatus.COMPLETED]

        if not completed:
            return "No successful outputs"

        # Use last step output as primary (usually the consolidation step)
        primary_output = completed[-1].output

        # Include summaries from other steps
        other_outputs = "\n".join([
            f"[{r.step.agent.name}]: {r.output[:200]}..."
            for r in completed[:-1]
        ])

        return f"""
Primary Output:
{primary_output}

Additional Context:
{other_outputs}
""".strip()

    def _detect_output_conflicts(self, results: List[StepResult]) -> List[str]:
        """
        Detect conflicts in agent outputs

        Args:
            results: List of StepResult objects

        Returns:
            List of conflict descriptions
        """
        conflicts = []

        # Check for contradictory outputs (simple heuristic)
        completed = [r for r in results if r.status == ExecutionStatus.COMPLETED]

        if len(completed) > 1:
            # Check for common conflict patterns
            outputs = [r.output for r in completed]

            # Example conflict detection (can be enhanced)
            for i, output1 in enumerate(outputs):
                for output2 in outputs[i+1:]:
                    if self._outputs_conflict(output1, output2):
                        conflicts.append(
                            f"Potential conflict between {completed[i].step.agent.name} "
                            f"and {completed[i+1].step.agent.name}"
                        )

        return conflicts

    def _outputs_conflict(self, output1: str, output2: str) -> bool:
        """
        Check if two outputs conflict (simple heuristic)

        In real implementation, this could use semantic similarity,
        keyword matching, or LLM-based conflict detection
        """
        # Simple heuristic: Check for contradictory keywords
        contradictions = [
            ("yes", "no"),
            ("true", "false"),
            ("approved", "rejected"),
            ("pass", "fail"),
        ]

        output1_lower = output1.lower()
        output2_lower = output2.lower()

        for word1, word2 in contradictions:
            if word1 in output1_lower and word2 in output2_lower:
                return True
            if word2 in output1_lower and word1 in output2_lower:
                return True

        return False

    def _report_progress(self, message: str, progress: float):
        """Report progress to callback if available"""
        if self.progress_callback:
            self.progress_callback(message, progress)


def main():
    """CLI interface for testing CoordinationEngine"""
    import sys
    from commands.lib.agent_router import AgentRouter

    router = AgentRouter()

    if len(sys.argv) < 2:
        print("Usage: coordination_engine.py <task_description> [mode]")
        print("\nModes: single, sequential, parallel, hierarchical")
        print("\nExamples:")
        print('  python coordination_engine.py "实现用户登录功能"')
        print('  python coordination_engine.py "代码审查" sequential')
        sys.exit(1)

    task = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else None

    # Generate workflow
    print(f"Task: {task}\n")
    print("Step 1: Generating workflow...")
    workflow = router.route(task, mode=mode)
    print(workflow)

    # Execute workflow
    print("\nStep 2: Executing workflow...")

    def progress_callback(message: str, progress: float):
        bar_length = 30
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"\r[{bar}] {progress*100:.0f}% - {message}", end="", flush=True)

    engine = CoordinationEngine(progress_callback=progress_callback)
    result = engine.execute(workflow)

    print("\n\nStep 3: Execution complete")
    print(result)

    if result.conflicts:
        print("\n⚠️  Conflicts detected:")
        for conflict in result.conflicts:
            print(f"  - {conflict}")


if __name__ == '__main__':
    main()
