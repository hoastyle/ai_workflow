## Usage
`@wf_coverage.md [component]`

## Purpose
Analyze and improve test coverage per project requirements:
- Measure coverage against PLANNING.md targets
- Identify untested code paths
- Generate coverage reports
- Track coverage improvements

## Process
1. **Coverage Analysis**:
   - Run coverage tools
   - Compare to requirements
   - Identify gaps
   - Prioritize areas

2. **Gap Assessment**:
   - Critical path coverage
   - Edge case handling
   - Error path testing
   - Integration coverage

3. **Improvement Planning**:
   - Create test tasks
   - Prioritize by risk
   - Estimate effort
   - Update TASK.md

4. **Reporting**:
   - Generate coverage report
   - Track trends
   - Document improvements
   - Update metrics

## Coverage Metrics
- **Line Coverage**: Percentage of lines executed
- **Branch Coverage**: Conditional paths tested
- **Function Coverage**: Functions with tests
- **Integration Coverage**: API/interface testing

## Output Format
1. **Coverage Report** – current metrics vs. targets
2. **Gap Analysis** – untested areas
3. **Priority List** – critical gaps to address
4. **Task Generation** – new test tasks for TASK.md
5. **Improvement Plan** – coverage enhancement strategy

## Workflow Integration
- Compares to PLANNING.md requirements
- Generates tasks in TASK.md
- Follows `@wf_test.md` execution
- Informs `@wf_review.md` assessments
- Tracks progress over time