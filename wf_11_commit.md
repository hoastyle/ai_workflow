## Usage
`@wf_commit.md [message]`

## Purpose
Create git commits with integrated formatting, validation, and context updates:
- Validate changes against standards
- Auto-format code before commit
- Update TASK.md task completion status
- Auto-update CONTEXT.md with work summary
- Identify and suggest KNOWLEDGE.md updates
- Maintain commit message conventions
- Ensure full traceability

## Process
1. **Pre-Commit Validation**:
   - Check git status for changes
   - Identify files for staging
   - Validate against PLANNING.md standards
   - Check related tasks in TASK.md

2. **Auto-Formatting**:
   - Apply language-specific formatting:
     * Python: black formatter
     * JavaScript/TypeScript: prettier
     * C++: clang-format
     * Go: gofmt
     * Other: project-specific formatters
   - Remove trailing whitespace and tabs
   - Ensure consistent line endings

3. **Change Analysis**:
   - Group related changes
   - Identify completed tasks
   - Check for excluded files
   - Validate code formatting applied
   - Analyze changes for knowledge extraction opportunities

4. **Commit Preparation**:
   - Stage formatted files
   - Generate semantic commit message
   - Link to TASK.md items
   - Add task references

5. **Context Update**:
   - Create/update CONTEXT.md with:
     * Work completed this session
     * Tasks finished and remaining
     * Key decisions made
     * Next priority items
   - Include progress summary

6. **Knowledge Extraction**:
   - Identify architectural decisions worthy of ADR documentation
   - Detect new problem-solution patterns
   - Recognize reusable code patterns or conventions
   - Suggest KNOWLEDGE.md updates if applicable

7. **Post-Commit Actions**:
   - Update TASK.md with completions
   - Document significant changes
   - Update KNOWLEDGE.md if new patterns or decisions identified
   - Prepare for next work cycle

## Commit Message Format
```
[<type>][(<scope>)] <subject>

<body>

Tasks: #task-id-1, #task-id-2
Refs: PLANNING.md updates, TASK.md completions
```

Types:
- feat: New feature implementation
- fix: Bug fix
- refactor: Code restructuring
- test: Test additions/changes
- docs: Documentation updates
- perf: Performance improvements
- chore: Maintenance tasks

## Output Format
1. **Formatting Report** – auto-formatting applied
2. **Change Summary** – files and modifications
3. **Knowledge Extraction** – identified patterns and decisions
4. **Commit Message** – formatted message
5. **Task Updates** – TASK.md completions
6. **Context Update** – CONTEXT.md refresh
7. **Knowledge Updates** – KNOWLEDGE.md suggestions or updates
8. **Commit Result** – success confirmation
9. **Next Steps** – remaining work items

## Workflow Integration
- Validates against PLANNING.md standards
- Auto-formats code (integrates wf_format.md functionality)
- Updates completed tasks in TASK.md
- Auto-updates CONTEXT.md for session continuity
- Enhances KNOWLEDGE.md with accumulated wisdom
- Follows after `@wf_review.md` approval
- Triggers task status updates
- Maintains complete project history and context
- Enables seamless `@wf_prime.md` context loading with long-term memory