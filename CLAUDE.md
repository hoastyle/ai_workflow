# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a closed-loop workflow command system for Claude Code that integrates project planning, task management, and development workflows. The system uses PLANNING.md and TASK.md as central coordination documents to maintain context across sessions and enable efficient development with minimal context overhead.

## Core Philosophy

The workflow system is designed to:
1. **Maintain Context** - Use PLANNING.md and TASK.md as persistent context stores
2. **Enable Continuity** - Allow work to continue across `/clear` boundaries via `@wf_prime.md`
3. **Track Progress** - Automatically update task status throughout development
4. **Enforce Standards** - Apply consistent patterns and quality gates
5. **Close the Loop** - Each command integrates with others for complete workflows

## Command Architecture

All commands follow the `wf_` prefix (workflow) to distinguish from other command systems.

### Core Workflow Commands
- `wf_prime.md` - Load project context from PLANNING.md and TASK.md
- `wf_planning.md` - Create/update project planning documentation
- `wf_task.md` - Manage task tracking and progress

### Development Commands
- `wf_code.md` - Implement features with architecture alignment
- `wf_ask.md` - Architecture consultation within project context
- `wf_debug.md` - Systematic debugging with documentation
- `wf_refactor.md` - Code improvement maintaining standards

### Quality Commands
- `wf_test.md` - Test development and execution
- `wf_review.md` - Code review against standards
- `wf_optimize.md` - Performance optimization
- `wf_coverage.md` - Coverage analysis and improvement

### Operations Commands
- `wf_deploy_check.md` - Deployment readiness validation
- `wf_commit.md` - Git commits with task tracking
- `wf_format.md` - Code formatting per standards
- `wf_fix.md` - Error resolution with documentation

## Workflow Patterns

### Session Management
```
1. Start: @wf_prime.md (load context)
2. Work: @wf_code.md, @wf_test.md, etc.
3. Save: @wf_task.md update, @wf_commit.md
4. Clear: /clear (when context gets large)
5. Resume: @wf_prime.md (reload and continue)
```

### Feature Development
```
1. @wf_ask.md - Architecture consultation
2. @wf_code.md - Implementation
3. @wf_test.md - Test creation
4. @wf_review.md - Code review
5. @wf_commit.md - Save progress
6. @wf_task.md update - Track completion
```

### Bug Fixing
```
1. @wf_debug.md or @wf_fix.md - Analyze issue
2. @wf_code.md - Implement fix
3. @wf_test.md - Verify fix
4. @wf_commit.md - Commit solution
```

### Refactoring
```
1. @wf_review.md - Identify issues
2. @wf_refactor.md - Improve code
3. @wf_test.md - Ensure no regression
4. @wf_optimize.md - Performance tuning
5. @wf_commit.md - Save improvements
```

## Key Files

### PLANNING.md
Central architecture and standards document containing:
- Project overview and goals
- System architecture and design
- Technology stack and tools
- Development standards and patterns
- Testing and deployment strategies

### TASK.md
Dynamic task tracking document containing:
- Categorized task lists
- Task status and progress
- Dependencies and blockers
- Completion history

## Command Integration Rules

1. **Context Loading**: Commands should read PLANNING.md for standards and TASK.md for status
2. **Progress Updates**: Commands that complete work should update TASK.md
3. **Standard Enforcement**: All code generation follows PLANNING.md guidelines
4. **Documentation**: Significant decisions update PLANNING.md
5. **Task Generation**: Issues and improvements create TASK.md entries

## Development Standards

### Code Quality
- Follow patterns established in existing code
- Maintain test coverage requirements
- Apply formatting before commits
- Document significant changes

### Git Workflow
- Semantic commit messages
- Task references in commits
- Format code before committing
- Update tasks after commits

### Testing
- Write tests for new features
- Maintain coverage targets
- Test before deployment
- Document test strategy

## Best Practices

1. **Start Sessions with Prime**: Always run `@wf_prime.md` after `/clear`
2. **Update Tasks Regularly**: Keep TASK.md current with progress
3. **Document Decisions**: Update PLANNING.md with architectural changes
4. **Test Continuously**: Run tests after significant changes
5. **Review Before Commit**: Use `@wf_review.md` for quality checks
6. **Format Consistently**: Run `@wf_format.md` before commits

## Troubleshooting

### Lost Context
- Run `@wf_prime.md` to reload
- Check PLANNING.md for architecture
- Review TASK.md for current state

### Unclear Requirements
- Use `@wf_ask.md` for consultation
- Update PLANNING.md with decisions
- Create tasks in TASK.md

### Quality Issues
- Run `@wf_review.md` for assessment
- Apply `@wf_refactor.md` for improvements
- Verify with `@wf_test.md`

## Continuous Improvement

The workflow system evolves through:
- Regular PLANNING.md updates
- Task pattern analysis
- Command refinements
- Process optimization

This system ensures development continuity, quality maintenance, and efficient progress tracking across all project phases.