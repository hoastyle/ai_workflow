"""
Agent-MCP Coordination System - Usage Examples

Demonstrates how to use the AgentRouter with automatic MCP tool selection.
"""

from commands.lib.agent_router import AgentRouter, CoordinationMode
from commands.lib.agent_registry import AgentRegistry, Agent
from commands.lib.mcp_selector import MCPSelector, Task


# ============================================================================
# Example 1: Basic Single Agent Workflow with MCP
# ============================================================================

def example_1_basic_single_agent():
    """
    Example 1: Single agent workflow with automatic MCP tool selection

    Demonstrates:
    - Creating a basic task
    - Routing to a single agent
    - Automatic MCP tool selection based on agent and task
    """
    print("=" * 80)
    print("Example 1: Basic Single Agent Workflow")
    print("=" * 80)

    # Create router
    router = AgentRouter()

    # Define task
    task = "实现用户登录功能"

    # Route task to single agent
    workflow = router.route(task, mode="single")

    print(f"\nTask: {task}")
    print(f"Coordination Mode: {workflow.mode}")
    print(f"Number of Steps: {len(workflow.steps)}")

    # Display workflow steps and MCP tools
    for i, step in enumerate(workflow.steps, 1):
        print(f"\nStep {i}:")
        print(f"  Agent: {step.agent.name}")
        print(f"  Role: {step.role}")
        print(f"  MCP Tools: {', '.join(step.mcp_tools)}")

    # Generate prompt
    prompt = workflow.to_prompt()
    print(f"\n{'-' * 80}")
    print("Generated Prompt:")
    print(f"{'-' * 80}")
    print(prompt[:500] + "..." if len(prompt) > 500 else prompt)


# ============================================================================
# Example 2: UI Task with Conditional MCP Activation
# ============================================================================

def example_2_ui_task_with_magic():
    """
    Example 2: UI task that conditionally activates Magic MCP tool

    Demonstrates:
    - Keyword-based conditional MCP activation
    - Magic tool activation for UI tasks
    - How task description affects MCP selection
    """
    print("\n" + "=" * 80)
    print("Example 2: UI Task with Conditional Magic Activation")
    print("=" * 80)

    router = AgentRouter()

    # Task with UI keywords
    ui_task = "实现用户界面登录页面组件，包含按钮和表单"

    workflow = router.route(ui_task, mode="single")

    print(f"\nTask: {ui_task}")

    for step in workflow.steps:
        print(f"\nAgent: {step.agent.name}")
        print(f"MCP Tools: {', '.join(step.mcp_tools)}")

        if "magic" in step.mcp_tools:
            print("  ✅ Magic tool activated (UI task detected)")
        else:
            print("  ❌ Magic tool not activated (no UI keywords)")


# ============================================================================
# Example 3: Sequential Workflow with Multiple Agents
# ============================================================================

def example_3_sequential_workflow():
    """
    Example 3: Sequential workflow with multiple agents

    Demonstrates:
    - Multi-agent sequential coordination
    - Different MCP tools for different agents
    - Workflow step dependencies
    """
    print("\n" + "=" * 80)
    print("Example 3: Sequential Workflow")
    print("=" * 80)

    router = AgentRouter()

    # Complex task requiring multiple agents
    task = "设计、实现并审查用户认证系统"

    workflow = router.route(task, mode="sequential")

    print(f"\nTask: {task}")
    print(f"Coordination Mode: {workflow.mode}")
    print(f"Number of Steps: {len(workflow.steps)}")

    for i, step in enumerate(workflow.steps, 1):
        print(f"\nStep {i}: {step.agent.name}")
        print(f"  Role: {step.role}")
        print(f"  MCP Tools: {', '.join(step.mcp_tools)}")
        if step.dependencies:
            print(f"  Dependencies: {', '.join(step.dependencies)}")


# ============================================================================
# Example 4: Parallel Workflow for Independent Tasks
# ============================================================================

def example_4_parallel_workflow():
    """
    Example 4: Parallel workflow for independent tasks

    Demonstrates:
    - Parallel agent coordination
    - Independent task execution
    - Parallel group assignment
    """
    print("\n" + "=" * 80)
    print("Example 4: Parallel Workflow")
    print("=" * 80)

    router = AgentRouter()

    # Task with parallel work
    task = "同时实现前端界面、后端API和数据库设计"

    workflow = router.route(task, mode="parallel")

    print(f"\nTask: {task}")
    print(f"Coordination Mode: {workflow.mode}")

    # Group steps by parallel group
    parallel_groups = {}
    for step in workflow.steps:
        group = step.parallel_group or 0
        if group not in parallel_groups:
            parallel_groups[group] = []
        parallel_groups[group].append(step)

    for group_id, steps in parallel_groups.items():
        print(f"\nParallel Group {group_id}:")
        for step in steps:
            print(f"  - {step.agent.name}: {', '.join(step.mcp_tools)}")


# ============================================================================
# Example 5: Architecture Task with Research MCPs
# ============================================================================

def example_5_architecture_with_research():
    """
    Example 5: Architecture task activating Context7 and Tavily

    Demonstrates:
    - Research-focused MCP activation
    - Context7 for documentation queries
    - Tavily for web search
    """
    print("\n" + "=" * 80)
    print("Example 5: Architecture Task with Research MCPs")
    print("=" * 80)

    router = AgentRouter()

    # Architecture/research task
    task = "调研并设计微服务架构，选择合适的技术栈"

    workflow = router.route(task, mode="single")

    print(f"\nTask: {task}")

    for step in workflow.steps:
        print(f"\nAgent: {step.agent.name}")
        print(f"MCP Tools: {', '.join(step.mcp_tools)}")

        if "context7" in step.mcp_tools:
            print("  ✅ Context7 activated (documentation queries)")
        if "tavily" in step.mcp_tools:
            print("  ✅ Tavily activated (web search)")


# ============================================================================
# Example 6: Framework-Specific Debug Task
# ============================================================================

def example_6_framework_debug():
    """
    Example 6: Debug task with framework-specific Context7 activation

    Demonstrates:
    - Conditional Context7 activation for framework references
    - How framework keywords trigger documentation lookup
    """
    print("\n" + "=" * 80)
    print("Example 6: Framework-Specific Debug Task")
    print("=" * 80)

    router = AgentRouter()

    # Debug task with framework reference
    framework_task = "调试React组件渲染性能问题"
    generic_task = "调试代码逻辑错误"

    print("\nTask 1 (with framework):", framework_task)
    workflow1 = router.route(framework_task, mode="single")
    for step in workflow1.steps:
        print(f"Agent: {step.agent.name}")
        print(f"MCP Tools: {', '.join(step.mcp_tools)}")
        if "context7" in step.mcp_tools:
            print("  ✅ Context7 activated (React framework detected)")

    print("\nTask 2 (generic):", generic_task)
    workflow2 = router.route(generic_task, mode="single")
    for step in workflow2.steps:
        print(f"Agent: {step.agent.name}")
        print(f"MCP Tools: {', '.join(step.mcp_tools)}")
        if "context7" not in step.mcp_tools:
            print("  ❌ Context7 not activated (no framework keywords)")


# ============================================================================
# Example 7: Direct MCPSelector Usage
# ============================================================================

def example_7_direct_mcp_selector():
    """
    Example 7: Using MCPSelector directly (advanced)

    Demonstrates:
    - Low-level MCPSelector API
    - Manual agent and task creation
    - Cache behavior
    """
    print("\n" + "=" * 80)
    print("Example 7: Direct MCPSelector Usage")
    print("=" * 80)

    selector = MCPSelector()

    # Create custom agent
    code_agent = Agent(
        name="code-agent",
        role="Implementation Engineer",
        expertise=["代码实现"],
        activation_keywords=["实现", "代码"],
        mcp_integrations=[
            {"name": "serena", "usage": "代码理解", "activation_condition": "always"},
            {"name": "magic", "usage": "UI生成", "activation_condition": "conditional",
             "keywords": ["ui", "界面", "组件"]},
            {"name": "sequential-thinking", "usage": "推理", "activation_condition": "always"}
        ]
    )

    # Test different tasks
    tasks = [
        "实现用户界面登录页面",
        "实现数据库查询逻辑",
        "实现API接口"
    ]

    for task_desc in tasks:
        task = Task(description=task_desc)
        tools = selector.select_tools(code_agent, task)

        print(f"\nTask: {task_desc}")
        print(f"Selected MCP Tools: {', '.join(tools)}")

        # Check for conditional tools
        if "magic" in tools:
            print("  → Magic activated (UI keywords found)")
        else:
            print("  → Magic not activated (no UI keywords)")


# ============================================================================
# Example 8: Performance Comparison with Caching
# ============================================================================

def example_8_performance_with_caching():
    """
    Example 8: Demonstrating caching performance benefits

    Demonstrates:
    - Selection caching mechanism
    - Performance improvement with repeated tasks
    """
    print("\n" + "=" * 80)
    print("Example 8: Performance with Caching")
    print("=" * 80)

    import time

    selector = MCPSelector()
    agent = Agent(
        name="test-agent",
        role="Test",
        expertise=[],
        activation_keywords=[],
        mcp_integrations=[
            {"name": "serena", "usage": "test", "activation_condition": "always"}
        ]
    )

    task = Task(description="测试缓存性能")

    # First call (no cache)
    start = time.time()
    tools1 = selector.select_tools(agent, task)
    time1 = time.time() - start

    # Second call (cached)
    start = time.time()
    tools2 = selector.select_tools(agent, task)
    time2 = time.time() - start

    print(f"\nFirst call (no cache): {time1 * 1000:.2f}ms")
    print(f"Second call (cached): {time2 * 1000:.2f}ms")
    print(f"Speedup: {time1 / time2:.1f}x" if time2 > 0 else "Instant (cached)")
    print(f"Selected tools: {', '.join(tools1)}")


# ============================================================================
# Example 9: Hierarchical Workflow with Complex Dependencies
# ============================================================================

def example_9_hierarchical_workflow():
    """
    Example 9: Hierarchical workflow for complex multi-layer tasks

    Demonstrates:
    - Multi-layer agent coordination
    - Complex dependency management
    - MCP tool selection at all hierarchy levels
    """
    print("\n" + "=" * 80)
    print("Example 9: Hierarchical Workflow")
    print("=" * 80)

    router = AgentRouter()

    # Very complex task requiring hierarchical breakdown
    task = "设计并实现完整的电商系统，包含用户界面、后端API、数据库和支付集成"

    workflow = router.route(task, mode="hierarchical")

    print(f"\nTask: {task}")
    print(f"Coordination Mode: {workflow.mode}")
    print(f"Total Steps: {len(workflow.steps)}")

    # Display hierarchy
    for i, step in enumerate(workflow.steps, 1):
        indent = "  " * (step.parallel_group or 0)
        print(f"\n{indent}Step {i}: {step.agent.name}")
        print(f"{indent}  Role: {step.role}")
        print(f"{indent}  MCP Tools: {', '.join(step.mcp_tools)}")


# ============================================================================
# Example 10: Custom Agent with Custom MCP Configuration
# ============================================================================

def example_10_custom_agent_mcp():
    """
    Example 10: Creating custom agent with specific MCP needs

    Demonstrates:
    - Custom agent creation
    - Custom MCP integration definition
    - Integration into routing system
    """
    print("\n" + "=" * 80)
    print("Example 10: Custom Agent with Custom MCP Configuration")
    print("=" * 80)

    # Create custom agent
    custom_agent = Agent(
        name="ml-specialist",
        role="Machine Learning Specialist",
        expertise=["机器学习", "模型训练", "数据分析"],
        activation_keywords=["机器学习", "模型", "训练", "预测"],
        mcp_integrations=[
            {"name": "serena", "usage": "代码理解", "activation_condition": "always"},
            {"name": "sequential-thinking", "usage": "复杂推理", "activation_condition": "always"},
            {"name": "context7", "usage": "ML框架文档", "activation_condition": "conditional",
             "keywords": ["tensorflow", "pytorch", "scikit-learn", "keras"]},
            {"name": "tavily", "usage": "最新ML研究", "activation_condition": "conditional",
             "keywords": ["研究", "论文", "sota", "benchmark"]}
        ]
    )

    # Create custom registry and router
    registry = AgentRegistry()
    registry.register(custom_agent)
    router = AgentRouter(registry=registry)

    # Test with ML task
    ml_task = "使用PyTorch实现图像分类模型"

    workflow = router.route(ml_task, mode="single")

    print(f"\nTask: {ml_task}")
    for step in workflow.steps:
        print(f"\nAgent: {step.agent.name}")
        print(f"Role: {step.role}")
        print(f"MCP Tools: {', '.join(step.mcp_tools)}")

        # Verify conditional activation
        if "context7" in step.mcp_tools:
            print("  ✅ Context7 activated (PyTorch keyword detected)")
        if "tavily" in step.mcp_tools:
            print("  ✅ Tavily activated (research keyword detected)")


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Run all examples"""
    examples = [
        example_1_basic_single_agent,
        example_2_ui_task_with_magic,
        example_3_sequential_workflow,
        example_4_parallel_workflow,
        example_5_architecture_with_research,
        example_6_framework_debug,
        example_7_direct_mcp_selector,
        example_8_performance_with_caching,
        example_9_hierarchical_workflow,
        example_10_custom_agent_mcp
    ]

    print("\n" + "=" * 80)
    print("Agent-MCP Coordination System - Usage Examples")
    print("=" * 80)
    print(f"\nTotal Examples: {len(examples)}")
    print("\nRunning all examples...\n")

    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n❌ Error in {example.__name__}: {str(e)}")

    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
