# Claude Code Workflow Commands (wf_*)

A comprehensive closed-loop workflow system for Claude Code that integrates project planning, task management, and development best practices.

## 🎯 Purpose

This command suite provides a structured workflow that:
- Maintains context across sessions using PLANNING.md and TASK.md
- Enables work continuity through `/clear` boundaries
- Tracks progress automatically throughout development
- Enforces consistent patterns and quality standards
- Creates a complete development loop from planning to deployment

## 🚀 Quick Start

1. **Initialize a Project**
   ```bash
   @wf_planning.md MyProject
   @wf_task.md create
   ```

2. **Start a Work Session**
   ```bash
   @wf_prime.md  # Load project context
   ```

3. **Develop Features**
   ```bash
   @wf_code.md implement user authentication
   @wf_test.md authentication module
   @wf_commit.md
   ```

4. **Continue After Break**
   ```bash
   /clear  # Clear context when it gets large
   @wf_prime.md  # Reload and continue
   ```

## 📁 Command Categories

### 🔄 Core Workflow
| Command | Purpose |
|---------|---------|
| `wf_prime.md` | Load project context from PLANNING.md and TASK.md |
| `wf_planning.md` | Create/update project architecture documentation |
| `wf_task.md` | Manage task tracking and progress |

### 💻 Development
| Command | Purpose |
|---------|---------|
| `wf_code.md` | Implement features aligned with architecture |
| `wf_ask.md` | Get architecture consultation within context |
| `wf_debug.md` | Debug issues systematically |
| `wf_refactor.md` | Improve code structure |

### ✅ Quality Assurance
| Command | Purpose |
|---------|---------|
| `wf_test.md` | Create and run tests |
| `wf_review.md` | Review code against standards |
| `wf_optimize.md` | Optimize performance |
| `wf_coverage.md` | Analyze test coverage |

### 🔧 Operations
| Command | Purpose |
|---------|---------|
| `wf_deploy_check.md` | Validate deployment readiness |
| `wf_commit.md` | Commit with task tracking |
| `wf_format.md` | Format code to standards |
| `wf_fix.md` | Fix errors with documentation |

## 🔄 Workflow Examples

### Complete Feature Development
```bash
# 1. Architecture consultation
@wf_ask.md How should I structure the authentication system?

# 2. Implementation
@wf_code.md Implement JWT-based authentication

# 3. Testing
@wf_test.md authentication endpoints

# 4. Review
@wf_review.md authentication module

# 5. Commit
@wf_format.md
@wf_commit.md feat: add JWT authentication

# 6. Update tasks
@wf_task.md update
```

### Bug Fix Workflow
```bash
# 1. Debug
@wf_debug.md Users getting 500 error on login

# 2. Fix
@wf_code.md Fix race condition in auth service

# 3. Test
@wf_test.md concurrent login scenarios

# 4. Commit
@wf_commit.md fix: resolve login race condition
```

### Session Management
```bash
# Start of day
@wf_prime.md
@wf_task.md review

# ... work on features ...

# Before break
@wf_task.md update
@wf_commit.md

# After break (new session)
/clear
@wf_prime.md
# Continue where you left off
```

## 📋 Key Files

### PLANNING.md
The architectural blueprint containing:
- Project overview and goals
- System architecture
- Technology decisions
- Development standards
- Testing strategies

### TASK.md
The dynamic progress tracker containing:
- Categorized task lists
- Current status
- Dependencies
- Completion history

## 🏗️ Setup

1. **Create the command directory in your project:**
   ```bash
   mkdir -p .claude/commands
   ```

2. **Copy all wf_*.md files to the commands directory**

3. **Initialize your project:**
   ```bash
   @wf_planning.md YourProjectName
   @wf_task.md create
   ```

4. **Start developing!**

## 💡 Best Practices

1. **Always prime after clearing context** - Run `@wf_prime.md` after `/clear`
2. **Keep tasks updated** - Update TASK.md regularly as you work
3. **Document decisions** - Update PLANNING.md with architectural changes
4. **Test continuously** - Run tests after changes
5. **Review before commit** - Use `@wf_review.md` for quality checks
6. **Format consistently** - Run `@wf_format.md` before commits

## 🔍 Command Integration

Each command integrates with others:
- Commands read context from PLANNING.md
- Work updates are tracked in TASK.md
- Standards are enforced consistently
- Progress flows through the workflow

## 📊 Workflow Benefits

- **Context Preservation**: Work continues smoothly across sessions
- **Progress Tracking**: Always know what's done and what's next
- **Quality Enforcement**: Consistent standards automatically applied
- **Reduced Overhead**: Minimal context repetition needed
- **Complete Loop**: From planning to deployment in one system

## 🛠️ Troubleshooting

### Lost Context?
```bash
@wf_prime.md  # Reload everything
```

### Unclear Requirements?
```bash
@wf_ask.md [your question]
```

### Need Quality Check?
```bash
@wf_review.md [scope]
@wf_coverage.md
```

### Ready to Deploy?
```bash
@wf_deploy_check.md production
```

## 📈 Continuous Improvement

The system evolves through:
- Regular PLANNING.md updates
- Task pattern analysis
- Command refinements
- Workflow optimization

---

**Note**: All commands use the `wf_` prefix to distinguish them from other command systems. This ensures clear namespace separation and easy identification of workflow commands.