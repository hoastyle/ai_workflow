## Usage
`@wf_fix.md <ERROR_OUTPUT>`

## Purpose
Systematic error resolution with documentation and task tracking:
- Analyze and fix errors methodically
- Update TASK.md with fixes
- Document solutions for future reference
- Maintain project stability

## Process
1. **Error Analysis**:
   - Parse complete error output
   - Identify error type and location
   - Check for known issues in TASK.md
   - Review related code sections

2. **Research and Investigation**:
   - Search for similar issues
   - Check project documentation
   - Review dependency versions
   - Analyze stack traces

3. **Solution Implementation**:
   - Address root cause
   - Apply minimal changes
   - Follow project patterns
   - Test fix thoroughly

4. **Verification**:
   - Re-run failing command
   - Verify error resolved
   - Check for regressions
   - Update documentation

5. **Documentation**:
   - Add fix to TASK.md
   - Update PLANNING.md if needed
   - Document for future reference

## Error Categories
- **Syntax**: Code formatting issues
- **Runtime**: Execution failures
- **Dependency**: Package/library issues
- **Configuration**: Setup problems
- **Build**: Compilation errors
- **Test**: Test failures
- **Deployment**: Deploy issues

## Output Format
1. **Error Analysis** – root cause identification
2. **Solution Applied** – fix implementation
3. **Verification Results** – confirmation of fix
4. **Task Updates** – TASK.md entries
5. **Prevention Notes** – future avoidance

## Workflow Integration
- Creates fix tasks in TASK.md
- May update PLANNING.md guidelines
- Triggers `@wf_test.md` validation
- Documents in commit messages
- Builds knowledge base