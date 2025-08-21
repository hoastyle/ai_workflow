# Claude Code Workflow Commands (wf_*) - v2.0 Optimized

A streamlined closed-loop workflow system for Claude Code that integrates project planning, task management, and development best practices.

## 🎯 Purpose

This command suite provides a structured workflow that:
- Maintains context across sessions using PLANNING.md, TASK.md, and CONTEXT.md
- Enables work continuity through `/clear` boundaries
- Tracks progress automatically throughout development
- Enforces consistent patterns and quality standards
- Creates a complete development loop from planning to deployment
- **New in v2.0**: Reduced complexity by 28% (18→13 commands) with integrated functionality

## 🚀 Quick Start

1. **Initialize a Project**
   ```bash
   @wf_01_planning.md MyProject
   @wf_02_task.md create
   ```

2. **Start a Work Session**
   ```bash
   @wf_03_prime.md  # Load project context
   ```

3. **Develop Features**
   ```bash
   @wf_05_code.md implement user authentication  # Auto-formatted
   @wf_07_test.md authentication module          # With coverage analysis
   @wf_11_commit.md                              # Auto-updates context
   ```

4. **Continue After Break**
   ```bash
   /clear  # Clear context when it gets large
   @wf_03_prime.md  # Reload and continue seamlessly
   ```

## 📁 Optimized Command Architecture (13 Commands)

### 🔄 Core Workflow (3) - Ordered by Usage
| Command | Purpose | New Features |
|---------|---------|-------------|
| `wf_01_planning.md` | Create/update project architecture | PRD.md alignment, enhanced documentation |
| `wf_02_task.md` | Manage task tracking and progress | PRD requirement mapping, improved automation |
| `wf_03_prime.md` | Load project context | Reads PRD.md + CONTEXT.md for session state |

### 💻 Development (4) - Ordered by Usage
| Command | Purpose | Integrations |
|---------|---------|-------------|
| `wf_04_ask.md` | Get architecture consultation within PRD context | Enhanced multi-agent |
| `wf_05_code.md` | Implement features aligned with PRD requirements | Auto-formatting built-in |
| `wf_06_debug.md` | Debug and fix issues systematically | **Merged wf_fix.md** |
| `wf_09_refactor.md` | Improve code structure maintaining PRD compliance | Enhanced |

### ✅ Quality Assurance (3) - Ordered by Usage
| Command | Purpose | Integrations |
|---------|---------|-------------|
| `wf_07_test.md` | Create and run tests | **Merged wf_coverage.md**, PRD criteria validation |
| `wf_08_review.md` | Review code against standards | Format validation, PRD compliance |
| `wf_10_optimize.md` | Optimize performance | PRD performance requirements |

### 🔧 Operations (2) - Ordered by Usage
| Command | Purpose | Integrations |
|---------|---------|-------------|
| `wf_11_commit.md` | Commit with complete automation | **Merged wf_format.md + auto CONTEXT.md updates** |
| `wf_12_deploy_check.md` | Validate deployment readiness | PRD criteria verification |

### 📚 Help (1) - Always Available
| Command | Purpose | Integrations |
|---------|---------|-------------|
| `wf_99_help.md` | Complete help system | **Merged wf_guide.md + wf_quick.md** |

## 🔄 Workflow Examples

### Complete Feature Development
```bash
# 1. Architecture consultation
@wf_04_ask.md How should I structure the authentication system?

# 2. Implementation (auto-formatted)
@wf_05_code.md Implement JWT-based authentication

# 3. Testing (with coverage analysis)
@wf_07_test.md authentication endpoints

# 4. Review
@wf_08_review.md authentication module

# 5. Commit (auto-formats, updates context)
@wf_11_commit.md feat: add JWT authentication

# 6. Update tasks (auto-updated by commit)
@wf_02_task.md update
```

### Bug Fix Workflow
```bash
# 1. Debug and fix (unified command)
@wf_06_debug.md Users getting 500 error on login

# 2. Test fix
@wf_07_test.md concurrent login scenarios

# 3. Commit (auto-formatted, context updated)
@wf_11_commit.md fix: resolve login race condition
```

### Session Management
```bash
# Start of day
@wf_03_prime.md              # Loads all context including CONTEXT.md
@wf_02_task.md review

# ... work on features ...

# Before break
@wf_11_commit.md              # Auto-updates CONTEXT.md

# After break (new session)
/clear
@wf_03_prime.md              # Seamlessly resumes from CONTEXT.md
# Continue where you left off
```

## 📋 Key Files (Closed Loop)

### PRD.md
The requirements source document containing:
- Official project requirements and specifications
- Business objectives and success criteria
- Stakeholder requirements and constraints
- **CRITICAL**: Read-only, never automatically modified

### PLANNING.md
The technical architecture document containing:
- Project overview and goals (derived from PRD.md)
- System architecture (meeting PRD requirements)
- Technology decisions (supporting PRD objectives)
- Development standards and patterns
- Testing strategies

### TASK.md
The dynamic progress tracker containing:
- Categorized task lists (mapped to PRD requirements)
- Current status and progress
- Dependencies and blockers
- Completion history
- PRD requirement traceability

### CONTEXT.md ⭐ (New in v2.0)
The session state manager containing:
- Work completed in recent sessions
- Key decisions made (with PRD alignment notes)
- Current focus areas
- Next priority items
- **Auto-updated by wf_11_commit.md**

## 🏗️ Setup

1. **Create the command directory in your project:**
   ```bash
   mkdir -p .claude/commands
   ```

2. **Copy all wf_*.md files to the commands directory**

3. **Initialize your project:**
   ```bash
   @wf_01_planning.md YourProjectName
   @wf_02_task.md create
   ```

4. **Start developing!**

## 💡 Best Practices

1. **Always prime after clearing context** - Run `@wf_03_prime.md` after `/clear`
2. **Let automation work for you** - `@wf_11_commit.md` handles formatting and context updates
3. **Use unified commands** - `@wf_06_debug.md` for both debugging and fixing
4. **Test with coverage** - `@wf_07_test.md --coverage` for coverage analysis
5. **Get help easily** - `@wf_99_help.md quick` for command reference

## 🔍 v2.0 Optimization Summary

### Eliminated Commands (5)
- ❌ `wf_fix.md` → Merged into `wf_06_debug.md`
- ❌ `wf_format.md` → Integrated into `wf_11_commit.md`
- ❌ `wf_coverage.md` → Merged into `wf_07_test.md`
- ❌ `wf_guide.md` → Merged into `wf_99_help.md`
- ❌ `wf_quick.md` → Merged into `wf_99_help.md`

### Enhanced Commands
- ✅ **wf_11_commit.md**: Auto-formatting + CONTEXT.md updates
- ✅ **wf_03_prime.md**: Reads CONTEXT.md for session continuity
- ✅ **wf_06_debug.md**: Unified debugging and fixing with `--quick` mode
- ✅ **wf_07_test.md**: Integrated coverage analysis with `--coverage` flag
- ✅ **wf_99_help.md**: Complete help system with quick/guide modes

### New Features
- 🆕 **CONTEXT.md**: Automatic session state management
- 🆕 **Auto-formatting**: Multi-language formatting in commit workflow
- 🆕 **Seamless sessions**: Perfect continuity across `/clear` boundaries
- 🆕 **Unified operations**: Less cognitive overhead, more focus on development

## 📊 Workflow Benefits

- **Context Preservation**: Work continues smoothly across sessions via CONTEXT.md
- **Progress Tracking**: Always know what's done and what's next
- **Quality Enforcement**: Consistent standards automatically applied
- **Reduced Overhead**: 28% fewer commands, integrated functionality
- **Complete Loop**: From planning to deployment in one streamlined system

## 🛠️ Troubleshooting

### Lost Context?
```bash
@wf_03_prime.md  # Reload everything from all core files
```

### Unclear Requirements?
```bash
@wf_04_ask.md [your question]
```

### Need Quality Check?
```bash
@wf_08_review.md [scope]
@wf_07_test.md --coverage
```

### Ready to Deploy?
```bash
@wf_12_deploy_check.md production
```

### Get Help?
```bash
@wf_99_help.md           # Main help menu
@wf_99_help.md quick     # Command reference
@wf_99_help.md guide     # Workflow scenarios
```

## 📈 Continuous Improvement

The system evolves through:
- Regular PLANNING.md updates
- Task pattern analysis
- Command refinements
- Workflow optimization
- User feedback integration

## 🔮 What's Next

Future improvements may include:
- Further automation enhancements
- Additional language support for formatting
- Enhanced context analysis
- Performance optimizations

---

**Note**: All commands use the `wf_` prefix to distinguish them from other command systems. This ensures clear namespace separation and easy identification of workflow commands.

**Migration from v1.0**: Existing projects will work seamlessly - deleted commands will show helpful error messages directing to their replacement commands.