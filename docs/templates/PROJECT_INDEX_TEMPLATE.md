# Project Index: [Project Name]

**Generated**: YYYY-MM-DD
**Version**: X.Y.Z
**Description**: [One-line project description - what does this project do?]

---

## 📁 Project Structure

```
project-root/
├── src/                       # Main source code ([LOC] lines)
│   ├── core/                  # Core modules
│   ├── api/                   # API layer
│   └── utils/                 # Utilities
├── tests/                     # Test suite
├── docs/                      # Documentation
│   ├── management/            # Project management (PRD, PLANNING, TASK, CONTEXT, KNOWLEDGE)
│   ├── api/                   # API documentation
│   ├── architecture/          # Architecture decisions (ADRs)
│   └── guides/                # User/developer guides
├── scripts/                   # Build/deployment scripts
└── config/                    # Configuration files
```

---

## 🚀 Entry Points

### Main Application
- **Command/Script**: `[how to run the application]`
- **Source**: `[path/to/entry/point.ext:function_name]`
- **Purpose**: [What this entry point does]

### Additional Entry Points
- **[Name]**: `[path/to/file.ext]`
- **Purpose**: [What this does]

---

## 📦 Core Modules

### Module 1 ([path/to/module/])
[Brief description of what this module does]

#### Key Components
- **[ComponentName]** (`[filename.ext]`)
  - **Purpose**: [What it does]
  - **Key features**: [List 2-3 main features]

#### Key Components
- **[ComponentName]** (`[filename.ext]`)
  - **Purpose**: [What it does]
  - **Key features**: [List 2-3 main features]

### Module 2 ([path/to/module/])
[Brief description]

---

## 🔧 Configuration

### [Technology Stack]
- **File**: `[config-file-name]`
- **Key settings**: [List important configuration points]
- **Dependencies**: [Key dependencies with versions]

### Environment Variables
- **[VAR_NAME]**: [Description and default value]
- **[VAR_NAME]**: [Description and default value]

---

## 📚 Documentation

### Key Files
- **CLAUDE.md**: AI assistant integration instructions
- **README.md**: Project overview and quick start
- **PLANNING.md**: Technical architecture and standards
- **TASK.md**: Task tracking and progress
- **KNOWLEDGE.md**: Knowledge base and documentation index

### Management Documents (docs/management/)
- **PRD.md**: Product requirements (read-only)
- **PLANNING.md**: Technical planning and architecture
- **TASK.md**: Task tracking system
- **CONTEXT.md**: Session state (auto-managed)
- **KNOWLEDGE.md**: Knowledge base + document index

### Technical Documentation (docs/)
- **[Category]/**: [Description of document category]
- **[Category]/**: [Description of document category]

---

## 🧪 Test Coverage

### Structure
- **Unit tests**: [Number] files in `tests/[directory]/`
- **Test framework**: [Framework name and version]
- **Coverage tool**: [Tool name]

### Running Tests
```bash
# All tests
[command to run all tests]

# Specific category
[command to run specific tests]

# With coverage
[command to run tests with coverage]
```

---

## 🔗 Key Dependencies

### Core Dependencies
- **[Package name]** [version] - [Purpose]
- **[Package name]** [version] - [Purpose]

### Dev Dependencies
- **[Package name]** [version] - [Purpose]
- **[Package name]** [version] - [Purpose]

---

## 📝 Quick Start

### Installation
```bash
# Install dependencies
[installation command]

# Development setup
[dev setup command]
```

### Usage
```bash
# Basic usage
[basic command]

# Common operations
[command 1]
[command 2]
```

---

## 🌿 Git Workflow

**Branch structure**: `[main branch]` (production) ← `[dev branch]` (testing) ← `feature/*`, `fix/*`, `docs/*`

**Current branch**: `[current branch name]`

---

## 🎯 Token Efficiency

### Index Performance
- **Before**: [X] tokens (reading all files every session)
- **After**: [Y] tokens (reading this index)
- **Reduction**: [Z]% ([saved tokens] saved per session)

### Workflow Optimization
- **Smart context loading**: Reduced from ~10,000 to ~2,000 tokens (80% savings)
- **Confidence checks**: Prevent failed implementations (25-750x ROI)
- **Token budgets**: Efficient agent coordination (simple/medium/complex)

---

## 📊 Project Stats

- **Source code**: [X] lines of code
- **Test files**: [Y] files
- **Documentation**: [Z] files
- **Supported platforms**: [Platform list]
- **License**: [License type]
- **Contributors**: [Number or list]

---

## 🔌 Workflow Integration

This project uses the **ai_workflow** framework with 15 commands:

### Core Workflow
- `/wf_03_prime` - Load project context (use this index with `--quick` flag)
- `/wf_05_code` - Implement features with confidence check
- `/wf_07_test` - Test development and coverage
- `/wf_08_review` - Code review and quality gates
- `/wf_11_commit` - Git commits with auto-updates

### Full Command List
See `COMMANDS.md` for complete workflow command reference.

---

## 🎨 Project Principles

1. **[Principle 1]** - [Description]
2. **[Principle 2]** - [Description]
3. **[Principle 3]** - [Description]
4. **Token Efficiency** - Use PROJECT_INDEX for 80% token savings
5. **Evidence-Based** - Verify with official docs, don't hallucinate

---

**For detailed documentation**: See `docs/` directory or visit [project repository]

---

## 📋 Template Instructions

**To use this template**:

1. **Replace placeholders**: All text in `[brackets]` should be replaced with actual project information
2. **Remove unused sections**: Delete sections that don't apply to your project
3. **Keep it lightweight**: Target ~300 lines, ~2,000 tokens maximum
4. **Update regularly**: Regenerate when project structure changes significantly
5. **Test token savings**: Run `/wf_03_prime` with and without this index to measure improvement

**Generation command**:
```bash
# Use wf_14_doc to generate PROJECT_INDEX from codebase
/wf_14_doc --generate-index
```

**Token budget**: Aim for ~2,000-3,000 tokens (vs 10,000+ without index)
