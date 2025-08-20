# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an optimized closed-loop workflow command system for Claude Code that integrates project planning, task management, and development workflows. The system uses PLANNING.md, TASK.md, and CONTEXT.md as central coordination documents to maintain context across sessions and enable efficient development with minimal context overhead.

**Recent Optimization**: Streamlined from 18 to 13 commands by eliminating redundancies and integrating related functions.

## Core Philosophy

The workflow system is designed to:
1. **Maintain Context** - Use PLANNING.md, TASK.md, and CONTEXT.md as persistent context stores
2. **Enable Continuity** - Allow work to continue across `/clear` boundaries via `@wf_prime.md`
3. **Track Progress** - Automatically update task status throughout development
4. **Enforce Standards** - Apply consistent patterns and quality gates
5. **Close the Loop** - Each command integrates with others for complete workflows
6. **Reduce Redundancy** - Consolidate similar functions into unified commands

## Command Architecture

All commands follow the `wf_` prefix (workflow) to distinguish from other command systems.

### Command Usage Pattern

Commands follow the format `wf_<number>_<name>.md <ARGUMENTS>` where:
- Command files define specialized workflows and agent roles
- Arguments specify the target scope (feature, component, error, etc.)
- Multi-agent coordination patterns are used for complex tasks
- Progressive development with validation at each step
- Numbered prefixes indicate typical usage order in workflows

### Core Workflow Commands (3) - Ordered by Usage
- `wf_01_planning.md` - Create/update project planning documentation (aligned with PRD.md)
- `wf_02_task.md` - Manage task tracking and progress (mapped to PRD requirements)
- `wf_03_prime.md` - Load project context from PRD.md, PLANNING.md, TASK.md, and CONTEXT.md

### Development Commands (4) - Ordered by Usage
- `wf_04_ask.md` - Architecture consultation within PRD and project context (includes comprehensive codebase review capabilities)
- `wf_05_code.md` - Implement features aligned with PRD requirements (auto-formatting integrated)
- `wf_06_debug.md` - Enhanced systematic debugging and fixing (integrated with advanced error analysis protocol)
- `wf_09_refactor.md` - Code improvement maintaining PRD compliance

### Quality Commands (3) - Ordered by Usage
- `wf_07_test.md` - Test development and execution (coverage analysis integrated, PRD criteria validation)
- `wf_08_review.md` - Code review against standards and PRD compliance
- `wf_10_optimize.md` - Performance optimization (meeting PRD performance requirements)

### Operations Commands (2) - Ordered by Usage
- `wf_11_commit.md` - Git commits with formatting and context updates (integrates wf_format.md)
- `wf_12_deploy_check.md` - Deployment readiness validation (PRD criteria verification)

### User Guidance Commands (1) - Always Available
- `wf_99_help.md` - Complete help system (integrates guide, quick reference, and command help)

## Workflow Patterns

### Session Management
```
1. Start: wf_03_prime.md (load context from all core files)
2. Work: wf_05_code.md, wf_07_test.md, etc.
3. Save: wf_02_task.md update, wf_11_commit.md (auto-updates CONTEXT.md)
4. Clear: /clear (when context gets large)
5. Resume: wf_03_prime.md (reload and continue seamlessly)
```

### Feature Development
```
1. wf_04_ask.md - Architecture consultation
2. wf_05_code.md - Implementation (auto-formatted)
3. wf_07_test.md - Test creation (with coverage analysis)
4. wf_08_review.md - Code review
5. wf_11_commit.md - Save progress (auto-updates context)
6. wf_02_task.md update - Track completion
```

### Bug Fixing
```
1. wf_06_debug.md - Analyze and fix issue (unified debug/fix)
2. wf_07_test.md - Verify fix
3. wf_11_commit.md - Commit solution (auto-formatted)
```

### Refactoring
```
1. wf_08_review.md - Identify issues
2. wf_09_refactor.md - Improve code
3. wf_07_test.md - Ensure no regression (with coverage check)
4. wf_10_optimize.md - Performance tuning
5. wf_11_commit.md - Save improvements
```

## Key Files (Closed Loop)

### PRD.md (Requirements Source)
Project Requirements Document - read-only reference containing:
- Official project requirements and specifications
- Business objectives and success criteria
- Stakeholder requirements and constraints
- **CRITICAL**: Never automatically modified by commands
- **ROLE**: Source of truth for all project decisions

### PLANNING.md
Technical architecture document aligned with PRD.md containing:
- Project overview and goals (derived from PRD.md)
- System architecture and design (meeting PRD requirements)
- Technology stack and tools (supporting PRD objectives)
- Development standards and patterns
- Testing and deployment strategies
- PRD compliance checklist

### TASK.md
Dynamic task tracking document containing:
- Categorized task lists (mapped to PRD requirements)
- Task status and progress
- Dependencies and blockers
- Completion history
- PRD requirement traceability

### CONTEXT.md (New)
Session state and progress summary containing:
- Work completed in recent sessions
- Key decisions made (with PRD alignment notes)
- Current focus areas
- Next priority items
- Auto-updated by wf_11_commit.md for seamless session continuity

## Command Integration Rules

1. **PRD Compliance**: All commands must reference and align with PRD.md requirements (read-only, never modify)
2. **Context Loading**: Commands should read PRD.md for requirements, PLANNING.md for standards, TASK.md for status, and CONTEXT.md for session state
3. **Progress Updates**: Commands that complete work should update TASK.md with PRD requirement traceability
4. **Standard Enforcement**: All code generation follows PLANNING.md guidelines aligned with PRD requirements
5. **Documentation**: Significant decisions update PLANNING.md with PRD alignment justification
6. **Task Generation**: Issues and improvements create TASK.md entries mapped to PRD requirements
7. **Session Continuity**: wf_11_commit.md auto-updates CONTEXT.md for seamless wf_03_prime.md loading
8. **Integrated Operations**: Formatting, coverage analysis, and fixing are integrated into main commands

## Multi-Agent Coordination

The cc_commands workflow system uses a multi-agent approach with specialized roles:

- **Architect Agent** - High-level design and structure analysis
- **Implementation Engineer** - Core functionality development following standards
- **Integration Specialist** - System compatibility and dependency management
- **Code Reviewer** - Quality validation and standards compliance
- **Test Specialists** - Various testing strategies (unit, integration, coverage)
- **Structure Analyst** - Code architecture evaluation and improvement
- **Design Pattern Expert** - Pattern application for maintainability
- **Debug Coordinator** - Systematic error analysis and resolution
- **Performance Optimizer** - System performance analysis and tuning

Each command orchestrates relevant specialists to ensure comprehensive coverage of development tasks while maintaining consistency with project standards and PRD requirements.

## Development Standards

### Code Quality
- Follow patterns established in existing code
- Maintain test coverage requirements
- Auto-formatting applied by wf_11_commit.md (Python: black, JS/TS: prettier, C++: clang-format, Go: gofmt)
- Document significant changes

### Git Workflow
- Semantic commit messages ([feat], [fix], [docs], [refactor])
- Task references in commits
- Auto-formatting integrated into wf_11_commit.md
- Auto-update TASK.md and CONTEXT.md after commits
- Consider splitting logically separate changes into different commits

### Testing
- Write tests for new features
- Maintain coverage targets using wf_07_test.md --coverage
- Test before deployment
- Document test strategy in PLANNING.md

### Error Debugging Process
Follow the systematic approach in `wf_06_debug.md`:
1. Analyze complete error output with detailed classification
2. Research using available tools (context7 MCP, brave-search MCP)
3. Implement targeted fixes addressing root causes
4. Verify fixes by re-running original commands
5. Iterate if new errors appear
6. Document solutions for future reference

## Best Practices

1. **Start Sessions with Prime**: Always run `wf_03_prime.md` after `/clear`
2. **Update Tasks Regularly**: Keep TASK.md current with progress
3. **Document Decisions**: Update PLANNING.md with architectural changes
4. **Test Continuously**: Run tests after significant changes
5. **Review Before Commit**: Use `wf_08_review.md` for quality checks
6. **Let Commit Handle Formatting**: wf_11_commit.md auto-formats, no need for manual formatting

## Troubleshooting

### Lost Context
- Run `wf_03_prime.md` to reload from all core files
- Check CONTEXT.md for latest session state
- Review PLANNING.md for architecture
- Review TASK.md for current state

### Unclear Requirements
- Use `wf_04_ask.md` for consultation
- Update PLANNING.md with decisions
- Create tasks in TASK.md

### Quality Issues
- Run `wf_08_review.md` for assessment
- Apply `wf_09_refactor.md` for improvements
- Verify with `wf_07_test.md --coverage`

## Optimization History

**v2.1 (Current)**:
- Enhanced debugging with comprehensive 6-step error analysis protocol
- Integrated codebase review capabilities into architecture consultation
- Added MCP tool integration (context7, brave-search) for better research
- Improved error classification and systematic investigation methods
- Enhanced TASK.md integration with priority-based issue tracking

**v2.0**:
- Reduced from 18 to 13 commands (-28% complexity)
- Integrated formatting into commit workflow
- Added CONTEXT.md for session continuity
- Merged redundant commands:
  - `wf_debug.md` absorbed `wf_fix.md`
  - `wf_help.md` absorbed `wf_guide.md` and `wf_quick.md`
  - `wf_test.md` absorbed `wf_coverage.md`
  - `wf_commit.md` absorbed `wf_format.md`
- Enhanced closed-loop automation

## Continuous Improvement

The workflow system evolves through:
- Regular PLANNING.md updates
- Task pattern analysis
- Command refinements
- Process optimization
- User feedback integration

This system ensures development continuity, quality maintenance, and efficient progress tracking across all project phases while maintaining simplicity and avoiding redundancy.