---
command: /wf_12_deploy_check
index: 12
phase: "运维部署"
reads: [PLANNING.md(部署要求), TASK.md(任务完成度), 测试报告]
writes: [部署报告, TASK.md(部署任务)]
prev_commands: [/wf_07_test, /wf_08_review, /wf_11_commit]
next_commands: [实际部署操作]
context_rules:
  - "验证PRD所有需求"
  - "确认PLANNING.md部署标准"
  - "要求/wf_07_test通过"
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

## Workflow Integration
- Validates against PLANNING.md requirements
- Checks TASK.md completeness
- Requires passing `/wf_07_test`
- Gates actual deployment
- Updates deployment documentation