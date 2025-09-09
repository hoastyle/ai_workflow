##                                                                                     Usage
`@wf_prime.md`

##                                                                                     Purpose
Prime the AI assistant with comprehensive project context by reading core project files to understand:
- Current project state and architecture
- Completed work and remaining tasks
- Development guidelines and standards
- Active working context
- Accumulated project knowledge and patterns

##                                                                                     Process
1. **Read Core Documentation**:
   - Check for existence of PRD.md, PLANNING.md, TASK.md, and KNOWLEDGE.md
   - Read PRD.md for project requirements (read-only, never modify)
   - Read CONTEXT.md for latest session state (if exists)
   - Read PLANNING.md for architecture aligned with PRD requirements
   - Read KNOWLEDGE.md for accumulated project knowledge and patterns
   - Read CLAUDE.md for project-specific AI guidance
   - Identify any additional context files (README.md, etc.)

2. **Context Analysis**:
   - Parse project architecture and technology stack from PLANNING.md
   - Load latest progress and decisions from CONTEXT.md
   - Extract architectural decisions and patterns from KNOWLEDGE.md
   - Understand current development phase from TASK.md
   - Identify active tasks and priorities
   - Note any blockers or dependencies
   - Review common issues and solutions from knowledge base

3. **Session State Recovery**:
   - Load work completed from previous sessions
   - Understand current development focus
   - Identify where work was left off
   - Restore development context and momentum

4. **Working Memory Setup**:
   - Load relevant code patterns and conventions from KNOWLEDGE.md
   - Apply accumulated solutions to current context
   - Understand testing and deployment procedures
   - Note security considerations and constraints
   - Reference architectural decisions for consistency
   - Prepare for continuation of work with enhanced context

##                                                                                     Output Format
1. **Requirements Overview** - Key requirements from PRD.md (read-only reference)
2. **Project Summary** - Brief overview from PLANNING.md aligned with PRD
3. **Knowledge Base Summary** - Key patterns and decisions from KNOWLEDGE.md
4. **Session Recovery** - Latest progress from CONTEXT.md
5. **Active Context** - Current working area and immediate tasks from TASK.md
6. **Applicable Solutions** - Relevant past solutions and patterns for current context
7. **Ready Status** - Confirmation of context loading and readiness to continue

##                                                                                     Integration Notes
- Run after `/clear` to restore working context
- Use before starting new related work sessions
- Loads CONTEXT.md for session continuity (updated by wf_commit.md)
- Integrates KNOWLEDGE.md for accumulated project wisdom
- Ensures continuity across context boundaries
- Maintains development momentum without redundant information
- Provides intelligent context enhancement through past decisions
- Core component of the closed-loop workflow system with long-term memory