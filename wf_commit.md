## Usage
`@wf_commit.md [message]`

## Purpose
Create git commits with proper validation and TASK.md synchronization:
- Validate changes against standards
- Update task completion status
- Maintain commit message conventions
- Ensure traceability

## Process
1. **Pre-Commit Validation**:
   - Check git status for changes
   - Identify files for staging
   - Validate against PLANNING.md standards
   - Check related tasks in TASK.md

2. **Change Analysis**:
   - Group related changes
   - Identify completed tasks
   - Check for excluded files
   - Validate code formatting

3. **Commit Preparation**:
   - Stage appropriate files
   - Generate semantic commit message
   - Link to TASK.md items
   - Add task references

4. **Post-Commit Actions**:
   - Update TASK.md with completions
   - Document significant changes
   - Prepare for next work cycle

## Commit Message Format
```
<type>(<scope>): <subject>

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
1. **Change Summary** – files and modifications
2. **Commit Message** – formatted message
3. **Task Updates** – TASK.md completions
4. **Commit Result** – success confirmation
5. **Next Steps** – remaining work items

## Workflow Integration
- Validates against PLANNING.md standards
- Updates completed tasks in TASK.md
- Follows after `@wf_review.md` approval
- Triggers task status updates
- Maintains project history