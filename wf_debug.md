## Usage
`@wf_debug.md <ERROR_DESCRIPTION>`

## Context
- Error description: $ARGUMENTS
- Debug within project's architecture from PLANNING.md
- Track debugging work in TASK.md
- Follow project's error handling patterns

## Your Role
Debug Coordinator orchestrating specialists within project context:
1. **Error Analyzer** – identifies root cause per system design
2. **Code Inspector** – examines using project conventions
3. **Environment Checker** – validates against PLANNING.md specs
4. **Fix Strategist** – proposes solutions maintaining standards

## Process
1. **Initial Assessment**:
   - Check if error relates to known issues in TASK.md
   - Review relevant PLANNING.md sections
   - Gather error context and logs

2. **Systematic Analysis**:
   - Analyzer: Classify error within system context
   - Inspector: Trace through project's code paths
   - Checker: Verify against documented configs
   - Strategist: Design fix per coding standards

3. **Solution Implementation**:
   - Fix following project patterns
   - Update error handling if needed
   - Document in TASK.md

4. **Validation**:
   - Verify fix resolves issue
   - Ensure no regression
   - Update documentation

## Output Format
1. **Debug Analysis** – root cause within system context
2. **Fix Implementation** – solution following standards
3. **Task Updates** – TASK.md entries for fixes
4. **Prevention Notes** – updates for PLANNING.md
5. **Test Requirements** – validation needed

## Workflow Integration
- References PLANNING.md for system design
- Updates TASK.md with debugging work
- May trigger `@wf_test.md` for validation
- Can lead to `@wf_refactor.md` if needed
- Documents lessons for future debugging