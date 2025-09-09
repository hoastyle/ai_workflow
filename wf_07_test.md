##                                                                                   Usage
`@wf_test.md <COMPONENT_OR_FEATURE> [--coverage]`

##                                                                                   Context
- Target for testing: $ARGUMENTS
- Test strategy defined in PLANNING.md
- Test tasks tracked in TASK.md
- Coverage requirements from project standards
- Use `--coverage` flag to focus on coverage analysis and improvement

##                                                                                   Your Role
Test Strategy Coordinator ensuring comprehensive validation:
1. **Test Architect** – designs tests per PLANNING.md strategy
2. **Unit Test Specialist** – creates tests following project patterns
3. **Integration Engineer** – validates system interactions
4. **Quality Validator** – ensures coverage meets requirements

##                                                                                   Process

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

##                                                                                   Output Format

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

##                                                                                   Workflow Integration
- Follows PLANNING.md test strategy
- Updates test tasks in TASK.md
- Validates `@wf_code.md` implementations
- Required before `@wf_deploy_check.md`
- Supports `@wf_review.md` assessments
- Integrates coverage analysis (formerly wf_coverage.md functionality)
- Coverage reports inform `@wf_refactor.md` decisions