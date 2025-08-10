## Usage
`@wf_prime.md`

## Purpose
Prime the AI assistant with comprehensive project context by reading PLANNING.md and TASK.md to understand:
- Current project state and architecture
- Completed work and remaining tasks
- Development guidelines and standards
- Active working context

## Process
1. **Read Core Documentation**:
   - Check for existence of PLANNING.md and TASK.md
   - Read CLAUDE.md for project-specific AI guidance
   - Identify any additional context files (README.md, etc.)

2. **Context Analysis**:
   - Parse project architecture and technology stack
   - Understand current development phase
   - Identify active tasks and priorities
   - Note any blockers or dependencies

3. **Working Memory Setup**:
   - Load relevant code patterns and conventions
   - Understand testing and deployment procedures
   - Note security considerations and constraints
   - Prepare for continuation of work

## Output Format
1. **Project Summary** - Brief overview of project purpose and current state
2. **Active Context** - Current working area and immediate tasks
3. **Key Information** - Critical details for continuing work
4. **Ready Status** - Confirmation of context loading and readiness to continue

## Integration Notes
- Run after `/clear` to restore working context
- Use before starting new related work sessions
- Ensures continuity across context boundaries
- Maintains development momentum without redundant information