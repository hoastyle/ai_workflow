---
command: /wf_07_test
index: 07
phase: "质量保证"
reads: [PLANNING.md(测试策略), TASK.md(测试任务), 代码文件]
writes: [测试文件, TASK.md(测试状态), 覆盖率报告]
prev_commands: [/wf_05_code, /wf_06_debug, /wf_09_refactor]
next_commands: [/wf_08_review, /wf_09_refactor, /wf_11_commit]
context_rules:
  - "遵循PLANNING.md测试策略"
  - "满足PRD覆盖率要求"
  - "--coverage模式分析测试覆盖率"
---

## 执行上下文
**输入**: PLANNING.md测试策略 + 代码实现
**输出**: 测试代码 + 覆盖率报告 + TASK.md更新
**依赖链**: /wf_05_code → **当前（测试开发）** → /wf_08_review → /wf_11_commit

## Usage
`/wf_07_test <COMPONENT_OR_FEATURE> [--coverage]`

## Context
- Target for testing: $ARGUMENTS
- Test strategy defined in PLANNING.md
- Test tasks tracked in TASK.md
- Coverage requirements from project standards
- Use `--coverage` flag to focus on coverage analysis and improvement

## Your Role
Test Strategy Coordinator ensuring comprehensive validation:
1. **Test Architect** – designs tests per PLANNING.md strategy
2. **Unit Test Specialist** – creates tests following project patterns
3. **Integration Engineer** – validates system interactions
4. **Quality Validator** – ensures coverage meets requirements

## Process

### Standard Testing (default)
1. **Test Planning**:
   - Review testing strategy in PLANNING.md
   - Check TASK.md for test requirements
   - Identify coverage gaps

2. **Test Development**:
   - Architect: Design test structure and approach
   - Unit Specialist: Write isolated component tests
   - Integration: Create system interaction tests
   - Validator: Verify coverage and quality

3. **Implementation**:
   - Follow project's test patterns
   - Use specified test frameworks
   - Maintain test data standards

4. **Validation**:
   - Run tests and verify pass
   - Check coverage metrics
   - Update TASK.md status

### Coverage Analysis Mode (--coverage flag)
1. **Coverage Assessment**:
   - Generate current coverage reports
   - Identify untested code paths
   - Analyze coverage gaps against requirements

2. **Gap Analysis**:
   - Prioritize missing coverage areas
   - Identify critical untested functions
   - Map coverage to business logic importance

3. **Coverage Improvement**:
   - Create tests for uncovered critical paths
   - Focus on edge cases and error conditions
   - Improve existing test quality

4. **Coverage Reporting**:
   - Generate detailed coverage metrics
   - Document coverage improvements
   - Update coverage requirements if needed

## Output Format

### Standard Testing Output
1. **Test Strategy** – approach aligned with project
2. **Test Implementation** – concrete test code
3. **Coverage Report** – basic metrics against requirements
4. **Task Updates** – TASK.md test completions
5. **Next Steps** – remaining test work

### Coverage Analysis Output (--coverage flag)
1. **Coverage Summary** – current coverage statistics
2. **Gap Analysis** – detailed uncovered areas
3. **Priority Recommendations** – critical missing tests
4. **Improvement Plan** – tests to add for better coverage
5. **Coverage Trends** – comparison with previous runs

## Workflow Integration
- Follows PLANNING.md test strategy
- Updates test tasks in TASK.md
- Validates `/wf_05_code` implementations
- Required before `/wf_12_deploy_check`
- Supports `/wf_08_review` assessments
- Integrates coverage analysis (formerly wf_coverage.md functionality)
- Coverage reports inform `/wf_09_refactor` decisions