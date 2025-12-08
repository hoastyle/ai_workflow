# Agent-MCP Coordination Examples

This directory contains usage examples and demonstrations of the Agent-MCP coordination system.

## Overview

The Agent-MCP coordination system automatically selects and activates appropriate MCP (Model Context Protocol) tools based on:
- **Agent role** (Architect, Code, Debug, etc.)
- **Task description** (keywords like "UI", "React", "调研")
- **Coordination mode** (single, sequential, parallel, hierarchical)

## Quick Start

### Running All Examples

```bash
cd /home/hao/Workspace/MM/utility/ai_workflow
python examples/agent_mcp_coordination_examples.py
```

### Running Individual Examples

```python
from examples.agent_mcp_coordination_examples import example_1_basic_single_agent

example_1_basic_single_agent()
```

## Example Categories

### Basic Usage (Examples 1-2)
- **Example 1**: Basic single agent workflow with automatic MCP selection
- **Example 2**: UI task with conditional Magic tool activation

### Multi-Agent Coordination (Examples 3-4)
- **Example 3**: Sequential workflow with multiple agents
- **Example 4**: Parallel workflow for independent tasks

### Specialized MCP Activation (Examples 5-6)
- **Example 5**: Architecture task activating Context7 and Tavily
- **Example 6**: Framework-specific debug task with conditional Context7

### Advanced Usage (Examples 7-10)
- **Example 7**: Direct MCPSelector API usage
- **Example 8**: Performance comparison with caching
- **Example 9**: Hierarchical workflow with complex dependencies
- **Example 10**: Custom agent with custom MCP configuration

## Key Concepts Demonstrated

### Three-Tier MCP Selection

**Tier 1 (Default - 100% Coverage)**
- Sequential-thinking: Always activated for all agents
- Provides structured multi-step reasoning

**Tier 2 (Role-Based - 90% Coverage)**
- Serena: Activated for all agents except research-agent
- Provides semantic code understanding

**Tier 3 (Task-Conditional)**
- Magic: Activated for UI-related tasks (keywords: ui, 界面, 组件, 按钮, 表单)
- Context7: Activated for framework references (keywords: react, vue, django, etc.)
- Tavily: Activated for research tasks (keywords: 研究, 调研, 评估)

### Activation Conditions

**Always Activation**
```yaml
mcp_integrations:
  - name: "serena"
    usage: "代码理解"
    activation_condition: "always"
```

**Conditional Activation**
```yaml
mcp_integrations:
  - name: "magic"
    usage: "UI生成"
    activation_condition: "conditional"
    keywords: ["ui", "界面", "组件", "按钮", "表单"]
```

### Coordination Modes

**Single Agent**
```python
workflow = router.route("实现用户登录", mode="single")
# → 1 agent, focused execution
```

**Sequential**
```python
workflow = router.route("设计并实现认证系统", mode="sequential")
# → Multiple agents, step-by-step execution
```

**Parallel**
```python
workflow = router.route("同时开发前端和后端", mode="parallel")
# → Multiple agents, concurrent execution
```

**Hierarchical**
```python
workflow = router.route("构建完整电商系统", mode="hierarchical")
# → Multi-layer agent coordination
```

## Example Outputs

### Example 1: Basic Single Agent
```
Task: 实现用户登录功能
Coordination Mode: SINGLE
Number of Steps: 1

Step 1:
  Agent: code-agent
  Role: Implementation Engineer
  MCP Tools: sequential-thinking, serena
```

### Example 2: UI Task with Magic
```
Task: 实现用户界面登录页面组件，包含按钮和表单

Agent: code-agent
MCP Tools: sequential-thinking, serena, magic
  ✅ Magic tool activated (UI task detected)
```

### Example 6: Framework Debug
```
Task 1 (with framework): 调试React组件渲染性能问题
Agent: debug-agent
MCP Tools: sequential-thinking, serena, context7
  ✅ Context7 activated (React framework detected)

Task 2 (generic): 调试代码逻辑错误
Agent: debug-agent
MCP Tools: sequential-thinking, serena
  ❌ Context7 not activated (no framework keywords)
```

## Performance Characteristics

### Caching Benefits (Example 8)
```
First call (no cache): 2.34ms
Second call (cached): 0.05ms
Speedup: 46.8x
```

### Typical Selection Times
- **Single agent selection**: < 5ms
- **Sequential workflow (3 agents)**: < 15ms
- **Parallel workflow (5 agents)**: < 20ms
- **Hierarchical workflow (10+ agents)**: < 50ms

## Testing

Run the integration tests to verify functionality:

```bash
# Test MCPSelector
python -m pytest tests/test_mcp_selector.py -v

# Test AgentRouter MCP integration
python -m pytest tests/test_agent_router_mcp.py -v

# Run all tests
python -m pytest tests/test_*mcp*.py -v
```

## Common Use Cases

### 1. UI Development Task
```python
router = AgentRouter()
workflow = router.route("实现登录界面组件", mode="single")
# → Activates: sequential-thinking, serena, magic
```

### 2. Framework Debugging
```python
workflow = router.route("调试React性能问题", mode="single")
# → Activates: sequential-thinking, serena, context7
```

### 3. Architecture Research
```python
workflow = router.route("调研微服务架构", mode="single")
# → Activates: sequential-thinking, context7, tavily
```

### 4. Complex Multi-Phase Development
```python
workflow = router.route(
    "设计、实现并测试用户认证系统",
    mode="sequential"
)
# → Multiple agents with appropriate MCP tools per phase
```

## Customization

### Creating Custom Agents

```python
from commands.lib.agent_registry import Agent

custom_agent = Agent(
    name="data-analyst",
    role="Data Analysis Specialist",
    expertise=["数据分析", "可视化"],
    activation_keywords=["分析", "数据", "图表"],
    mcp_integrations=[
        {
            "name": "serena",
            "usage": "代码理解",
            "activation_condition": "always"
        },
        {
            "name": "sequential-thinking",
            "usage": "复杂分析",
            "activation_condition": "always"
        },
        {
            "name": "context7",
            "usage": "数据科学库文档",
            "activation_condition": "conditional",
            "keywords": ["pandas", "numpy", "matplotlib"]
        }
    ]
)
```

### Extending MCP Selection Logic

To add custom MCP selection rules, extend the `MCPSelector` class:

```python
from commands.lib.mcp_selector import MCPSelector

class CustomMCPSelector(MCPSelector):
    def select_tools(self, agent, task):
        # Call parent selection
        tools = super().select_tools(agent, task)

        # Add custom logic
        if "机器学习" in task.description.lower():
            tools.add("ml-toolkit")

        return list(tools)
```

## Troubleshooting

### Issue: MCP tools not being selected
**Solution**: Check agent's `mcp_integrations` field has `activation_condition` set

### Issue: Conditional tools not activating
**Solution**: Verify task description contains keywords from `keywords` array

### Issue: Slow workflow generation
**Solution**: Check cache is enabled (`MCPSelector._cache_ttl > 0`)

## Related Documentation

- **Agent Definitions**: `/commands/agents/*.md`
- **MCPSelector Implementation**: `/commands/lib/mcp_selector.py`
- **AgentRouter Implementation**: `/commands/lib/agent_router.py`
- **MCP Optimizer**: `/commands/lib/mcp_optimizer.py`
- **Integration Tests**: `/tests/test_*mcp*.py`

## Contributing

When adding new examples:
1. Follow the numbering convention (`example_N_description`)
2. Include docstring explaining what is demonstrated
3. Add clear print statements showing results
4. Update this README with example description
5. Run tests to ensure compatibility

---

**Last Updated**: 2025-12-08
**Version**: 1.0
**Related Task**: TASK.md § Task 5.2 - Agent-MCP Coordination Mode
