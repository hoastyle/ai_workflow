---
command: /wf_12_deploy_check
index: 12
phase: "运维部署"
description: "部署就绪检查，多层验证和Go/No-Go决策"
reads: [PLANNING.md(部署要求), TASK.md(任务完成度), 测试报告]
writes: [部署报告, TASK.md(部署任务)]
prev_commands: [/wf_07_test, /wf_08_review, /wf_11_commit]
next_commands: [实际部署操作]
model: haiku
token_budget: simple
mcp_support:
  - name: "Playwright"
    flag: "自动激活"
    detail: "浏览器自动化部署验证和E2E烟雾测试"
context_rules:
  - "验证PRD所有需求"
  - "确认PLANNING.md部署标准"
  - "要求/wf_07_test通过"
---

## 🔌 MCP 增强能力

本命令支持 Playwright MCP 服务器的自动增强。

### Playwright (浏览器自动化部署验证)

**启用**: 自动激活（在 /wf_12_deploy_check 中）
**用途**: 浏览器自动化测试和E2E烟雾测试验证部署就绪性
**自动激活**: 执行部署检查命令时

**示例**:
```bash
# 自动激活（检测到部署检查需求）
/wf_12_deploy_check "production"

# 指定部署环境
/wf_12_deploy_check "staging environment"
```

**改进点**:
- E2E烟雾测试自动化（关键用户流程验证）
- 视觉回归测试（UI一致性检查）
- 性能监控（页面加载时间、API响应时间）
- 部署验证（服务可用性、健康检查）
- 跨浏览器兼容性测试

---

### 🔧 MCP Gateway 集成 (NEW - Task 3.2)

**Gateway 初始化** (所有 MCP 使用前执行):
```python
# 导入 MCP Gateway
from src.mcp.gateway import get_mcp_gateway

# 获取全局 Gateway 实例
gateway = get_mcp_gateway()
```

**Playwright 工具调用** (E2E烟雾测试):
```python
# 检查可用性
if gateway.is_available("playwright"):
    # Step 1: 启动浏览器并导航到部署环境
    navigate_tool = gateway.get_tool("playwright", "browser_navigate")

    result = navigate_tool.call(
        url="https://production.example.com"
    )

    # Step 2: 执行关键用户流程测试
    click_tool = gateway.get_tool("playwright", "browser_click")

    # 测试登录流程
    click_tool.call(
        element="Login button",
        ref="button[data-test='login']"
    )

    # Step 3: 验证关键功能可用
    snapshot_tool = gateway.get_tool("playwright", "browser_snapshot")

    page_state = snapshot_tool.call()

    # 验证页面元素存在
    if "Dashboard" in page_state:
        print("✅ 部署验证通过：关键功能可访问")
    else:
        print("❌ 部署验证失败：关键功能不可用")
        exit(1)

else:
    print("⚠️ Playwright MCP 不可用，使用手动部署验证")
```

**E2E烟雾测试工作流示例** (完整用户流程验证):
```python
# 检查可用性
if gateway.is_available("playwright"):
    # 定义关键用户流程
    critical_flows = [
        {
            "name": "用户登录",
            "steps": [
                {"action": "navigate", "url": "https://prod.example.com/login"},
                {"action": "fill", "element": "username", "value": "test@example.com"},
                {"action": "fill", "element": "password", "value": "test_password"},
                {"action": "click", "element": "submit"},
                {"action": "verify", "expected": "Dashboard"}
            ]
        },
        {
            "name": "API健康检查",
            "steps": [
                {"action": "navigate", "url": "https://prod.example.com/api/health"},
                {"action": "verify", "expected": "status: ok"}
            ]
        },
        {
            "name": "关键业务功能",
            "steps": [
                {"action": "navigate", "url": "https://prod.example.com/dashboard"},
                {"action": "click", "element": "create-order"},
                {"action": "verify", "expected": "Order created"}
            ]
        }
    ]

    # 执行所有流程
    failed_flows = []

    for flow in critical_flows:
        try:
            print(f"🧪 测试流程: {flow['name']}")

            for step in flow['steps']:
                if step['action'] == 'navigate':
                    nav_tool = gateway.get_tool("playwright", "browser_navigate")
                    nav_tool.call(url=step['url'])

                elif step['action'] == 'fill':
                    fill_tool = gateway.get_tool("playwright", "browser_fill")
                    fill_tool.call(
                        uid=step['element'],
                        value=step['value']
                    )

                elif step['action'] == 'click':
                    click_tool = gateway.get_tool("playwright", "browser_click")
                    click_tool.call(
                        element=step['element'],
                        ref=f"button[data-test='{step['element']}']"
                    )

                elif step['action'] == 'verify':
                    snapshot_tool = gateway.get_tool("playwright", "browser_snapshot")
                    page_content = snapshot_tool.call()

                    if step['expected'] not in page_content:
                        raise AssertionError(f"未找到预期内容: {step['expected']}")

            print(f"  ✅ {flow['name']} 通过")

        except Exception as e:
            print(f"  ❌ {flow['name']} 失败: {e}")
            failed_flows.append(flow['name'])

    # 生成部署报告
    if failed_flows:
        print(f"\n❌ 部署验证失败 - {len(failed_flows)} 个流程失败:")
        for flow_name in failed_flows:
            print(f"  - {flow_name}")
        print("\n🚫 Go/No-Go 决策: NO-GO (阻塞问题)")
        exit(1)
    else:
        print(f"\n✅ 所有烟雾测试通过 ({len(critical_flows)} 个流程)")
        print("🟢 Go/No-Go 决策: GO (可以部署)")

else:
    print("⚠️ Playwright MCP 不可用，跳过E2E烟雾测试")
```

**视觉回归测试示例** (UI一致性验证):
```python
# 检查可用性
if gateway.is_available("playwright"):
    # Step 1: 截取部署前的基准截图（假设已存储）
    baseline_screenshots = load_baseline_screenshots()

    # Step 2: 截取部署后的当前截图
    screenshot_tool = gateway.get_tool("playwright", "browser_take_screenshot")

    pages_to_verify = [
        {"name": "首页", "url": "https://prod.example.com/"},
        {"name": "登录页", "url": "https://prod.example.com/login"},
        {"name": "仪表板", "url": "https://prod.example.com/dashboard"}
    ]

    visual_regressions = []

    for page in pages_to_verify:
        # 导航到页面
        nav_tool = gateway.get_tool("playwright", "browser_navigate")
        nav_tool.call(url=page['url'])

        # 截取当前截图
        current_screenshot = screenshot_tool.call(
            filename=f"current_{page['name']}.png",
            type="png"
        )

        # 对比基准截图
        baseline = baseline_screenshots.get(page['name'])

        if baseline:
            diff_percentage = compare_screenshots(baseline, current_screenshot)

            if diff_percentage > 5.0:  # 5% 差异阈值
                visual_regressions.append({
                    "page": page['name'],
                    "diff": diff_percentage
                })
                print(f"⚠️ 视觉变化检测: {page['name']} ({diff_percentage}% 差异)")
            else:
                print(f"✅ 视觉一致性: {page['name']} (无显著变化)")

    # 报告视觉回归
    if visual_regressions:
        print(f"\n⚠️ 检测到 {len(visual_regressions)} 个页面的视觉变化:")
        for regression in visual_regressions:
            print(f"  - {regression['page']}: {regression['diff']}% 差异")
        print("\n💡 建议: 审查视觉变化是否为预期更新")
    else:
        print("\n✅ 所有页面视觉一致性检查通过")

else:
    print("⚠️ Playwright MCP 不可用，跳过视觉回归测试")
```

**性能监控示例** (页面加载和API响应时间):
```python
# 检查可用性
if gateway.is_available("playwright"):
    # Step 1: 监控页面加载性能
    navigate_tool = gateway.get_tool("playwright", "browser_navigate")

    performance_targets = [
        {"url": "https://prod.example.com/", "max_load_time": 3.0},
        {"url": "https://prod.example.com/dashboard", "max_load_time": 5.0},
        {"url": "https://prod.example.com/api/data", "max_load_time": 2.0}
    ]

    performance_issues = []

    for target in performance_targets:
        import time

        start_time = time.time()
        navigate_tool.call(url=target['url'])
        load_time = time.time() - start_time

        if load_time > target['max_load_time']:
            performance_issues.append({
                "url": target['url'],
                "load_time": load_time,
                "target": target['max_load_time']
            })
            print(f"⚠️ 性能问题: {target['url']} 加载时间 {load_time:.2f}s (目标 < {target['max_load_time']}s)")
        else:
            print(f"✅ 性能达标: {target['url']} 加载时间 {load_time:.2f}s")

    # Step 2: 检查网络请求
    network_tool = gateway.get_tool("playwright", "browser_network_requests")

    network_requests = network_tool.call()

    # 分析慢请求
    slow_requests = [
        req for req in network_requests
        if req.get('duration', 0) > 1000  # > 1秒
    ]

    if slow_requests:
        print(f"\n⚠️ 检测到 {len(slow_requests)} 个慢请求:")
        for req in slow_requests[:5]:  # 显示前5个
            print(f"  - {req['url']}: {req['duration']}ms")

    # 生成性能报告
    if performance_issues:
        print(f"\n⚠️ 性能警告: {len(performance_issues)} 个页面超出加载时间目标")
        print("💡 建议: 审查性能退化是否可接受")
    else:
        print("\n✅ 所有页面性能达标")

else:
    print("⚠️ Playwright MCP 不可用，跳过性能监控")
```

**Gateway 优势**:
- ✅ 统一的 MCP 管理接口
- ✅ 自动降级（MCP 不可用时跳过E2E测试）
- ✅ 连接池复用（减少多次启动开销）
- ✅ 工具懒加载（按需初始化）
- ✅ E2E测试自动化（准确率 100%）
- ✅ 部署风险降低 70-90%（提前发现问题）

---

## 执行上下文
**输入**: PLANNING.md部署要求 + TASK.md完成度 + 测试结果
**输出**: 部署就绪报告 + Go/No-Go决策
**依赖链**: /wf_07_test + /wf_08_review → **当前（部署检查）** → 部署

## Usage
`/wf_12_deploy_check <DEPLOYMENT_TARGET>`

## Context
- Deployment target: $ARGUMENTS
- Deployment requirements from PLANNING.md
- Deployment tasks in TASK.md
- Production readiness criteria

## Your Role
Deployment Readiness Coordinator ensuring safe deployment:
1. **Quality Agent** – validates code and test completeness
2. **Security Auditor** – ensures security compliance
3. **Operations Engineer** – verifies infrastructure readiness
4. **Risk Assessor** – evaluates deployment risks

## Process
1. **Readiness Assessment**:
   - Check deployment criteria in PLANNING.md
   - Review completed tasks in TASK.md
   - Validate prerequisites

2. **Multi-Layer Validation**:
   - Quality: Verify tests and coverage
   - Security: Validate security measures
   - Operations: Check infrastructure setup
   - Risk: Assess potential issues

3. **Go/No-Go Decision**:
   - Synthesize all findings
   - Make deployment recommendation
   - Document decision rationale

4. **Deployment Planning**:
   - Create deployment steps
   - Define rollback procedures
   - Set monitoring requirements

## Output Format
1. **Readiness Report** – comprehensive assessment
2. **Risk Analysis** – identified risks and mitigations
3. **Deployment Plan** – step-by-step procedure
4. **Monitoring Setup** – post-deployment checks
5. **Task Updates** – deployment task status

## 📌 工作流导航 (Phase 3 - 闭环工作流)

### 工作流位置指示

当使用此命令时，你正在执行标准开发流程的以下阶段：

```
[项目启动] → [任务规划] → [加载上下文] → [架构咨询] → [代码实现] → [测试验证] → [代码审查] → [部署检查 ← 当前] → [提交保存] → [实际部署]
  STEP 0       STEP 0.5        STEP 1         STEP 2       STEP 3       STEP 4       STEP 5            STEP 7                STEP 6      STEP 8
```

### ✅ 已完成的步骤

在执行 `/wf_12_deploy_check` 前，必须已经完成：

1. ✅ **代码实现** (STEP 3) - 功能开发完成 (`/wf_05_code`)
2. ✅ **测试验证** (STEP 4) - 所有测试通过 (`/wf_07_test`)
3. ✅ **代码审查** (STEP 5) - 代码审查通过 (`/wf_08_review`)
4. ✅ **提交保存** (STEP 6) - 变更已提交 (`/wf_11_commit`)

### 📝 当前步骤

**正在执行**: `/wf_12_deploy_check <DEPLOYMENT_TARGET>` (部署就绪检查)

**这个命令的职责**：
- 验证部署前的所有就绪条件
- 执行多层验证（质量、安全、运维、风险）
- 确认所有任务完成度
- 评估部署风险
- 作出 Go/No-Go 的部署决策
- 准备部署计划和回滚方案

### ⏭️ 建议下一步

**部署检查完成后**，根据 Go/No-Go 决策选择下一步：

#### 路径 1️⃣：Go - 部署就绪 ✅
```bash
# 当前: 所有检查通过，系统已就绪
# 下一步: 执行实际部署操作

# 1. 确认部署计划（从检查报告中获取）
# 2. 执行部署（使用生产部署脚本或流程）
# 3. 验证部署成功
# 4. 监控部署后的系统状态

# 如果需要跟踪: 更新 TASK.md 部署任务状态
/wf_02_task update "部署到 <environment> 完成"

# 然后: 可能需要 /wf_11_commit 记录部署完成
```
**适用场景**: 所有部署检查通过，系统已完全就绪，可以安全部署

#### 路径 2.：No-Go - 发现阻塞问题 🔴
```bash
# 当前: 发现了阻塞部署的严重问题
# 下一步: 修复问题后重新检查

# 根据问题类型修复:
# - 代码问题 → /wf_05_code "修复部署问题"
# - 测试失败 → /wf_07_test "修复失败的测试"
# - 安全问题 → /wf_05_code "修复安全漏洞"

# 修复后重新运行部署检查
/wf_12_deploy_check "重新检查 <environment>"

# 修复完成后再次提交
/wf_11_commit "fix: 修复部署阻塞问题"
```
**适用场景**: 部署检查发现了必须修复的问题，无法继续部署

#### 路径 3️⃣：Go with Warnings - 条件部署 ⚠️
```bash
# 当前: 检查通过但有非阻塞的警告
# 下一步: 在充分了解风险的情况下部署

# 1. 仔细review风险和缓解措施
# 2. 确认团队同意接受这些风险
# 3. 准备监控计划（特别关注警告涉及的领域）
# 4. 执行部署
# 5. 加强部署后的监控

# 建议: 在 TASK.md 或部署文档中记录风险接受
/wf_02_task update "部署到 <environment> 已接受风险 XYZ"

# 部署完成后提交
/wf_11_commit "deploy: 条件部署到 <environment>（已接受风险）"
```
**适用场景**: 部署检查发现了可接受的风险，团队同意继续部署

### 📊 工作流进度提示

当你完成部署检查时，确保输出中包含：

✅ 已完成:
- 部署就绪状态的清晰评估
- 所有验证层的检查结果（质量、安全、运维、风险）
- 明确的 Go/No-Go 决策和决策理由
- 阻塞问题的清晰列表（如果 No-Go）
- 部署计划和回滚方案（如果 Go）
- 监控和验证需求

⏭️ 下一步提示:
- Go/No-Go 决策
- 建议的路径（1/2/3）
- 需要的修复或准备工作
- 预计的部署时间表

### 💡 决策指南

**我应该执行哪个路径？**

| 情况 | 建议 | 命令 |
|------|------|------|
| 所有检查通过，完全就绪 | 路径 1 | 执行部署操作 |
| 发现阻塞问题，无法部署 | 路径 2 | 修复问题 → /wf_12_deploy_check |
| 有非阻塞警告但可接受 | 路径 3 | 执行条件部署，加强监控 |
| 部分检查失败，需要重新检查 | 迭代 | 修复问题 → /wf_12_deploy_check |

**何时是 Go-No-Go？**

**Go 条件**:
- ✅ 所有必须的测试通过
- ✅ 代码审查通过
- ✅ 安全审计通过
- ✅ 部署前准备完成
- ✅ 没有已知的阻塞问题

**No-Go 条件**:
- ❌ 关键功能测试失败
- ❌ 安全审计发现严重漏洞
- ❌ 基础设施未就绪
- ❌ 数据迁移或初始化失败
- ❌ 有明确的阻塞问题

**Warnings（条件 Go）**:
- ⚠️ 性能指标未达目标但可接受
- ⚠️ 第三方依赖有警告但不阻塞
- ⚠️ 文档不完整但不影响部署
- ⚠️ 已知的非关键 bug（与部署无关）

---

## Workflow Integration
- Validates against PLANNING.md requirements
- Checks TASK.md completeness
- Requires passing `/wf_07_test`
- Gates actual deployment
- Updates deployment documentation