## Usage
`@wf_commit.md [message]`

## Purpose
Create git commits with integrated formatting, validation, and context updates:
- Validate changes against standards
- Auto-format code before commit
- Update TASK.md task completion status
- Auto-update CONTEXT.md with work summary
- **Auto-update README.md when important work completed**
- Identify and suggest KNOWLEDGE.md updates
- Maintain commit message conventions
- Ensure full traceability

## Process
1. **Pre-Commit Validation**:
   - Check git status for changes
   - Identify files for staging
   - Validate against PLANNING.md standards
   - Check related tasks in TASK.md

2. **Auto-Formatting & Time Sync**:
   - Apply language-specific formatting:
     * Python: black formatter
     * JavaScript/TypeScript: prettier
     * C++: clang-format
     * Go: gofmt
     * Other: project-specific formatters
   - Remove trailing whitespace and tabs
   - Ensure consistent line endings
   - **Auto-Update Maintenance Dates**:
     * Update "最后更新" fields to current date: `$(date +%Y-%m-%d)`
     * Update "Last Updated" fields to current date: `$(date +%Y-%m-%d)`
     * Preserve historical dates (创建日期、发布日期、决策日期)
     * Validate date format consistency across all .md files
     * Check for and flag any outdated year references

3. **Change Analysis**:
   - Group related changes
   - Identify completed tasks
   - Check for excluded files
   - Validate code formatting applied
   - **README Update Assessment**: Check if changes trigger README update:
     * New core features (feat commits affecting main files)
     * PLANNING.md architecture changes
     * API/interface modifications
     * Dependency or installation requirement changes
     * Major version milestones
   - Analyze changes for knowledge extraction opportunities
   - **Time Point Validation**: Verify all dates are current and accurate

4. **README Update (If Triggered)**:
   - **Content Generation**: Generate updated README.md:
     * Project overview from PLANNING.md
     * Installation requirements from dependencies
     * Core usage examples from available commands
     * Feature list from completed TASK.md items
     * Architecture overview from PLANNING.md
     * Troubleshooting from KNOWLEDGE.md
   - **Quality Validation**: Ensure README meets standards:
     * No trailing whitespace
     * Valid markdown formatting
     * Working internal links
     * Current date references
   - **Integration**: Include updated README in commit

5. **Commit Preparation**:
   - Stage formatted files (including README if updated)
   - Generate semantic commit message
   - Link to TASK.md items
   - Add task references

6. **Context Update**:
   - Create/update CONTEXT.md with:
     * Work completed this session
     * Tasks finished and remaining
     * Key decisions made
     * Next priority items
   - Include progress summary

7. **Knowledge Extraction**:
   - Identify architectural decisions worthy of ADR documentation
   - Detect new problem-solution patterns
   - Recognize reusable code patterns or conventions
   - Suggest KNOWLEDGE.md updates if applicable

8. **Post-Commit Actions**:
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
3. **README Update Report** – README generation details (if triggered)
4. **Knowledge Extraction** – identified patterns and decisions
5. **Commit Message** – formatted message
6. **Task Updates** – TASK.md completions
7. **Context Update** – CONTEXT.md refresh
8. **Knowledge Updates** – KNOWLEDGE.md suggestions or updates
9. **Commit Result** – success confirmation
10. **Next Steps** – remaining work items

## Workflow Integration
- Validates against PLANNING.md standards
- Auto-formats code (integrates wf_format.md functionality)
- **Auto-updates README.md for important work completions**
- Updates completed tasks in TASK.md
- Auto-updates CONTEXT.md for session continuity
- Enhances KNOWLEDGE.md with accumulated wisdom
- Follows after `@wf_review.md` approval
- Triggers task status updates
- Maintains complete project history and context
- **Ensures README stays synchronized with project state**
- Enables seamless `@wf_prime.md` context loading with long-term memory