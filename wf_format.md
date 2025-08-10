## Usage
`@wf_format.md [file_pattern]`

## Purpose
Format code according to project standards before commits:
- Apply formatting rules from PLANNING.md
- Ensure consistency across codebase
- Prepare code for review
- Maintain code quality

## Process
1. **Configuration Check**:
   - Read formatting rules from PLANNING.md
   - Identify file types and patterns
   - Load formatter configurations

2. **Format Execution**:
   - Python: Apply `black` formatting
   - C++: Apply `clang-format`
   - JavaScript/TypeScript: Apply prettier
   - Other: Apply project-specific formatters

3. **Validation**:
   - Verify formatting success
   - Check for formatting errors
   - Report changes made

4. **Integration**:
   - Update formatted files
   - Prepare for commit
   - Document in workflow

## Formatting Rules
### Python
- Use black with project config
- Line length per PLANNING.md
- Import sorting with isort

### C++
- Use clang-format with project style
- Bracket style per standards
- Indentation per guidelines

### JavaScript/TypeScript
- Use prettier with config
- Semi-colons per standard
- Quote style per convention

## Output Format
1. **Files Formatted** – list of modified files
2. **Changes Made** – formatting adjustments
3. **Errors** – any formatting failures
4. **Ready Status** – commit readiness
5. **Next Actions** – review or commit

## Workflow Integration
- Uses standards from PLANNING.md
- Required before `@wf_commit.md`
- Part of `@wf_review.md` process
- Maintains code consistency
- Reduces review friction