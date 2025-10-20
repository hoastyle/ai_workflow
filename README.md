# Claude Code Workflow Commands (wf_*) - v2.3 Enhanced

A streamlined closed-loop workflow system for Claude Code that integrates project planning, task management, and development best practices.

## 🎯 Purpose

This command suite provides a structured workflow that:
- Maintains context across sessions using PLANNING.md, TASK.md, and CONTEXT.md
- Enables work continuity through `/clear` boundaries
- Tracks progress automatically throughout development
- Enforces consistent patterns and quality standards
- Creates a complete development loop from planning to deployment
- **New in v2.3**: Enhanced with automatic README updates and improved closed-loop workflow
- **Optimized**: Reduced complexity by 28% (18→13 commands) with integrated functionality

## 🚀 Quick Start

1. **Initialize a Project**
   ```bash
   /wf_01_planning "MyProject"
   /wf_02_task create
   ```

2. **Start a Work Session**
   ```bash
   /wf_03_prime  # Load project context
   ```

3. **Develop Features**
   ```bash
   /wf_05_code "implement user authentication"  # Auto-formatted
   /wf_07_test "authentication module"          # With coverage analysis
   /wf_11_commit "feat: add user authentication"  # Auto-updates context
   ```

4. **Continue After Break**
   ```bash
   /clear  # Clear context when it gets large
   /wf_03_prime  # Reload and continue seamlessly
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
| `wf_11_commit.md` | Commit with complete automation | **Auto README updates + formatting + CONTEXT.md updates** |
| `wf_12_deploy_check.md` | Validate deployment readiness | PRD criteria verification |

### 📚 Help (1) - Always Available
| Command | Purpose | Integrations |
|---------|---------|-------------|
| `wf_99_help.md` | Complete help system | **Merged wf_guide.md + wf_quick.md** |

## 🔄 Workflow Examples

### Complete Feature Development
```bash
# 1. Architecture consultation
/wf_04_ask "How should I structure the authentication system?"

# 2. Implementation (auto-formatted)
/wf_05_code "Implement JWT-based authentication"

# 3. Testing (with coverage analysis)
/wf_07_test "authentication endpoints"

# 4. Review
/wf_08_review

# 5. Commit (auto-updates context)
/wf_11_commit "feat: add JWT authentication"

# 6. Update tasks (auto-updated by commit)
/wf_02_task update
```

### Bug Fix Workflow
```bash
# 1. Debug and fix (unified command)
/wf_06_debug "Users getting 500 error on login"

# 2. Test fix
/wf_07_test "concurrent login scenarios"

# 3. Commit (auto-updated context)
/wf_11_commit "fix: resolve login race condition"
```

### Session Management
```bash
# Start of day
/wf_03_prime              # Loads all context from project files
/wf_02_task review

# ... work on features ...

# Before break
/wf_11_commit "save progress"              # Auto-updates CONTEXT.md

# After break (new session)
/clear
/wf_03_prime              # Seamlessly resumes from CONTEXT.md
# Continue where you left off
```

## 📋 Key Files (Closed Loop)

**Location**: All project management files are stored in the project root directory (`.claude/`), separate from the `commands/` directory which contains only workflow command definitions.

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

### CONTEXT.md ⭐ (Session State Manager)
The automatic session continuity file containing:
- Work completed in recent sessions
- Key decisions made (with PRD alignment notes)
- Current focus areas
- Next priority items
- **Auto-updated by `/wf_11_commit`**

### KNOWLEDGE.md
The accumulated knowledge repository containing:
- Architecture Decision Records (ADR)
- Common problem-solution patterns
- Reusable code patterns and conventions
- Project-specific best practices
- Technical research and findings

## 🏗️ Setup

1. **Directory structure is automatically created by Claude Code:**
   ```
   .claude/
   ├── PRD.md            # Project requirements
   ├── PLANNING.md       # Technical architecture
   ├── TASK.md           # Task tracking
   ├── CONTEXT.md        # Session state (auto-updated)
   ├── KNOWLEDGE.md      # Knowledge base
   └── commands/         # Workflow command definitions
       ├── wf_01_planning.md
       ├── wf_02_task.md
       ├── ... (other wf_XX commands)
       └── CLAUDE.md     # AI instruction document
   ```

2. **Initialize your project:**
   ```bash
   /wf_01_planning "YourProjectName"
   /wf_02_task create
   ```

3. **Start developing!**

## 💡 Best Practices

1. **Always prime after clearing context** - Run `/wf_03_prime` after `/clear`
2. **Let automation work for you** - `/wf_11_commit` handles formatting and context updates
3. **Use unified commands** - `/wf_06_debug` for both debugging and fixing
4. **Test with coverage** - `/wf_07_test --coverage` for coverage analysis
5. **Get help easily** - `/wf_99_help` for comprehensive command reference
6. **Respect file permissions** - PRD.md is read-only; use PLANNING.md for technical decisions
7. **Leverage KNOWLEDGE.md** - Document architecture decisions and patterns for future reference

## 🔍 Latest Updates (v2.4)

### Recent Improvements
- 🎯 **Data File Migration**: Moved project management files (PRD.md, PLANNING.md, KNOWLEDGE.md, CONTEXT.md) from `commands/` to project root for cleaner separation of concerns
- 🤖 **AI Execution Rules**: Added comprehensive AI behavior guidelines and file permission matrix
- 📁 **File Structure Clarity**: `commands/` directory now contains only workflow definitions
- 🔧 **Format Optimization**: Unified all command invocations to slash command format (`/wf_XX`)
- 📚 **Documentation Enhancement**: Updated CLAUDE.md with AI-specific execution rules and file management guidelines

### v2.0 Optimization Summary

#### Eliminated Commands (5)
- ❌ `wf_fix.md` → Merged into `wf_06_debug.md`
- ❌ `wf_format.md` → Integrated into `wf_11_commit.md`
- ❌ `wf_coverage.md` → Merged into `wf_07_test.md`
- ❌ `wf_guide.md` → Merged into `wf_99_help.md`
- ❌ `wf_quick.md` → Merged into `wf_99_help.md`

#### Enhanced Commands
- ✅ **wf_11_commit.md**: Auto-formatting + CONTEXT.md updates
- ✅ **wf_03_prime.md**: Reads CONTEXT.md for session continuity
- ✅ **wf_06_debug.md**: Unified debugging and fixing
- ✅ **wf_07_test.md**: Integrated coverage analysis with `--coverage` flag
- ✅ **wf_99_help.md**: Complete help system

#### New Features
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
/wf_03_prime  # Reload everything from all core files
```

### Unclear Requirements?
```bash
/wf_04_ask "your question"
```

### Need Quality Check?
```bash
/wf_08_review
/wf_07_test --coverage
```

### Ready to Deploy?
```bash
/wf_12_deploy_check
```

### Get Help?
```bash
/wf_99_help           # Main help menu
/wf_99_help quick     # Command reference
/wf_99_help guide     # Workflow scenarios
```

## 📈 Continuous Improvement

The system evolves through:
- Regular PLANNING.md updates with architecture decisions
- Task pattern analysis via TASK.md
- Command refinements based on usage patterns
- Workflow optimization driven by KNOWLEDGE.md insights
- User feedback integration

## 📖 Related Documentation

- **CLAUDE.md** - Comprehensive AI instruction document with execution rules
- **PLANNING.md** - Technical architecture and development standards
- **KNOWLEDGE.md** - Architecture Decision Records (ADR) and accumulated project knowledge
- **README_CN.md** - Chinese language documentation

## 🔮 What's Next

Future improvements may include:
- Further automation enhancements
- Additional language support for formatting
- Enhanced context analysis capabilities
- Performance optimizations for large projects
- Extended multi-language testing support

---

**Architecture**: Clear separation between command definitions (`commands/`) and project data (project root)

**File Management**: All project management documents stored in project root with read/write permissions matrix defined in CLAUDE.md

**Command Format**: All commands use slash command format (`/wf_XX`) for consistency and clarity

**Last Updated**: 2025-10-21
**Current Version**: v2.4 (AI Execution Rules + Data File Migration)
