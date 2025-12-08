#!/usr/bin/env python3
"""
Auto-Activation Demo - Integration example for TaskAnalyzer and AgentRouter

This script demonstrates the complete auto-activation workflow:
1. User provides a task description
2. TaskAnalyzer analyzes the task and recommends agents
3. AgentRouter creates a workflow and coordinates agents
4. User can override with manual agent selection

Usage:
    python auto_activation_demo.py "实现用户登录功能"
    python auto_activation_demo.py "@architect-agent \"设计系统架构\""
    python auto_activation_demo.py "优化数据库查询性能" --mode sequential
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from commands.lib.task_analyzer import TaskAnalyzer
from commands.lib.agent_router import AgentRouter
from commands.lib.agent_registry import AgentRegistry


def print_separator(char="-", length=60):
    """Print a separator line"""
    print(char * length)


def demonstrate_auto_activation(task_description: str, mode: str = None):
    """
    Complete auto-activation demonstration

    Args:
        task_description: User's task description
        mode: Optional coordination mode override
    """
    print(f"\n{'=' * 70}")
    print(f"  AI WORKFLOW AUTO-ACTIVATION DEMO")
    print(f"{'=' * 70}\n")

    # Step 1: Initialize components
    print("Step 1: Initializing components...")
    registry = AgentRegistry()
    analyzer = TaskAnalyzer(registry)
    router = AgentRouter(registry)
    print(f"✅ Loaded {len(registry.agents)} agents\n")

    # Step 2: Check for manual override
    print("Step 2: Checking for manual agent override...")
    override = router.suggest_manual_override(task_description)

    if override:
        print(f"✅ Manual override detected!")
        print(f"   Agent: {override['agent']}")
        print(f"   Task: {override['task']}")
        task_description = override['task']
        # Force single mode for manual override
        mode = "single"
        print()
    else:
        print("❌ No manual override (using auto-activation)\n")

    # Step 3: Task Analysis
    print_separator()
    print("Step 3: Analyzing task...")
    print_separator()
    analysis = analyzer.analyze(task_description)

    print(f"\n📋 Task Analysis Results:")
    print(f"   Description: {analysis.task_description}")
    print(f"   Intent: {analysis.intent.value} (confidence: {analysis.intent_confidence:.0%})")
    print(f"   Complexity: {analysis.complexity.value}")
    print(f"   Estimated Effort: {analysis.estimated_effort}")
    print(f"   Overall Confidence: {analysis.confidence:.0%}")

    if analysis.primary_agent:
        print(f"\n   Primary Agent: {analysis.primary_agent.agent.name}")
        print(f"   Agent Score: {analysis.primary_agent.score:.0%}")
        print(f"   Reason: {analysis.primary_agent.reason}")

    if analysis.fallback_agents:
        print(f"\n   Fallback Agents:")
        for i, agent in enumerate(analysis.fallback_agents, 1):
            print(f"      {i}. {agent.agent.name} ({agent.score:.0%})")

    if analysis.technical_stack:
        print(f"\n   Technical Stack: {', '.join(analysis.technical_stack)}")

    print(f"\n   Explanation: {analysis.explanation}")

    if analysis.suggestions:
        print(f"\n   💡 Suggestions:")
        for suggestion in analysis.suggestions:
            print(f"      • {suggestion}")

    # Step 4: Workflow Generation
    print_separator()
    print("\nStep 4: Generating workflow...")
    print_separator()

    try:
        if override and override['agent']:
            # Manual override: get specific agent
            specific_agent = registry.get_agent(override['agent'])
            if specific_agent:
                from commands.lib.agent_registry import AgentMatch
                primary_match = AgentMatch(
                    agent=specific_agent,
                    score=1.0,
                    matched_keywords=[],
                    matched_scenarios=[],
                    reason="Manual override"
                )
                workflow = router._create_single_workflow(primary_match)
            else:
                print(f"❌ Error: Agent '{override['agent']}' not found")
                return
        else:
            # Auto-activation
            workflow = router.route(task_description, mode=mode)

        print(workflow)

        # Step 5: Conflict Detection
        print_separator()
        print("Step 5: Checking for conflicts...")
        print_separator()

        conflicts = router.detect_conflicts(workflow.steps)
        if conflicts:
            print("\n⚠️  Potential Conflicts Detected:")
            for conflict in conflicts:
                print(f"   • {conflict}")
        else:
            print("\n✅ No conflicts detected")

        # Step 6: Execution Plan
        print_separator()
        print("\nStep 6: Execution Plan")
        print_separator()

        print(f"\n📌 Workflow Mode: {workflow.mode.value}")
        print(f"📌 Primary Agent: {workflow.primary_agent.name}")
        print(f"📌 Total Steps: {len(workflow.steps)}")
        print(f"📌 Estimated Time: {workflow.estimated_time}")
        print(f"📌 Confidence: {workflow.confidence:.0%}")

        print(f"\n🔄 Execution Sequence:")
        for i, step in enumerate(workflow.steps, 1):
            deps = f" (depends on: {', '.join(step.dependencies)})" if step.dependencies else ""
            parallel = f" [parallel group {step.parallel_group}]" if step.parallel_group else ""
            print(f"   {i}. {step.agent.name} ({step.role}){deps}{parallel}")

    except Exception as e:
        print(f"\n❌ Error generating workflow: {e}")
        return

    # Step 7: Summary
    print_separator("=", 70)
    print("\n✅ AUTO-ACTIVATION COMPLETE")
    print_separator("=", 70))

    print(f"""
Summary:
--------
Task: {task_description}
Intent: {analysis.intent.value} ({analysis.intent_confidence:.0%})
Workflow Mode: {workflow.mode.value}
Primary Agent: {workflow.primary_agent.name}
Agents Involved: {len(workflow.steps)}
Estimated Time: {workflow.estimated_time}
Overall Confidence: {min(analysis.confidence, workflow.confidence * 100):.0%}

Next Steps:
-----------
1. Review the workflow execution plan
2. Confirm agent selections
3. Execute workflow with: /wf_05_code "{task_description}"
4. Monitor progress and adjust as needed
    """)


def run_multiple_examples():
    """Run multiple example scenarios"""
    examples = [
        ("实现用户登录功能", None),
        ("修复支付API的bug", None),
        ("优化数据库查询性能", "sequential"),
        ("代码审查整个项目", "parallel"),
        ("设计微服务架构", "hierarchical"),
        ('@architect-agent "设计数据库架构"', None),
    ]

    print("\n" + "=" * 70)
    print("  RUNNING MULTIPLE AUTO-ACTIVATION EXAMPLES")
    print("=" * 70)

    for i, (task, mode) in enumerate(examples, 1):
        print(f"\n\nExample {i}/{len(examples)}")
        demonstrate_auto_activation(task, mode)
        input("\nPress Enter to continue to next example...")


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: auto_activation_demo.py <task_description> [--mode MODE]")
        print("\nModes: single, sequential, parallel, hierarchical")
        print("\nExamples:")
        print('  python auto_activation_demo.py "实现用户登录功能"')
        print('  python auto_activation_demo.py "代码审查" --mode sequential')
        print('  python auto_activation_demo.py "@architect-agent \\"设计系统架构\\""')
        print('\n  python auto_activation_demo.py --examples  # Run all examples')
        sys.exit(1)

    # Check for --examples flag
    if sys.argv[1] == '--examples':
        run_multiple_examples()
        sys.exit(0)

    # Parse arguments
    task = sys.argv[1]
    mode = None

    if len(sys.argv) > 2 and sys.argv[2] == '--mode':
        if len(sys.argv) < 4:
            print("Error: --mode requires a value")
            sys.exit(1)
        mode = sys.argv[3]

    # Run single demonstration
    demonstrate_auto_activation(task, mode)


if __name__ == '__main__':
    main()
