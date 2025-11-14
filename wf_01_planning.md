---
command: /wf_01_planning
index: 01
phase: "基础设施"
description: "创建/更新项目规划文档，建立架构和开发标准"
reads: [PRD.md, 现有PLANNING.md, 项目代码结构]
writes: [PLANNING.md]
prev_commands: []
next_commands: [/wf_02_task]
context_rules:
  - "PRD.md是只读的，绝不修改"
  - "PLANNING.md必须对齐PRD.md所有需求"
  - "这是项目架构的权威文档"
---

## 执行上下文
**输入**: PRD.md需求 + 现有项目结构分析
**输出**: PLANNING.md (项目架构和开发标准)
**依赖链**: **当前（项目启动）** → /wf_02_task (任务规划)

## Usage
`/wf_01_planning <PROJECT_NAME>`

## Purpose
Create or update PLANNING.md to establish comprehensive project documentation that:
- Defines project architecture and technical decisions
- Documents development workflow and standards
- Provides context for AI assistants and developers
- Maintains project continuity across sessions

## Process
1. **Requirements Analysis**:
   - Read PRD.md for official project requirements (read-only, never modify)
   - Check for existing PLANNING.md
   - Analyze project structure and codebase
   - Identify technology stack and frameworks
   - Review existing documentation
   - Ensure all PRD requirements are addressed in planning

2. **Document Structure Creation**:
   ### Project Overview
   - Purpose and goals (derived from PRD.md)
   - Target audience/users (per PRD requirements)
   - Key features and functionality (aligned with PRD)
   - Success criteria (mapped from PRD objectives)
   - PRD compliance checklist

   ### Architecture
   - System design and patterns
   - Core components and modules
   - Data models and storage
   - External integrations
   - Technology decisions (What, not Why)
     * 📋 List current technology choices
     * 🔗 Architecture decision rationale → See ADR
     * ❌ DO NOT duplicate decision background and trade-offs here

   ### Technology Stack
   - Programming languages and versions
   - Frameworks and libraries
   - Database and storage systems
   - Development and deployment tools
   - Third-party services

   **Architecture Decision Records (ADR)**:
   - Detailed "Why" → See KNOWLEDGE.md § ADR
   - Major technical choices → Create ADR: docs/adr/YYYY-MM-DD-title.md
   - PLANNING.md records "What it is", NOT "Why we chose it"
   - Example reference format:
     ```markdown
     ## Technology Stack
     - Frontend: React 18
     - Backend: Node.js + Express
     - Database: PostgreSQL

     **Architecture Decisions**: See following ADRs
     - [Why React?](docs/adr/2025-01-01-choose-react.md)
     - [Why PostgreSQL?](docs/adr/2025-01-02-choose-postgresql.md)
     ```

   ### Development Workflow
   - Setup instructions
   - Build commands
   - Test execution
   - Deployment process
   - Git workflow

   ### Code Standards
   - Naming conventions
   - File organization
   - Code style guidelines
   - Documentation requirements
   - Review process

   ### Testing Strategy
   - Unit test approach
   - Integration testing
   - E2E testing (if applicable)
   - Coverage requirements
   - Test data management

   ### Security Guidelines
   - Authentication approach
   - Authorization patterns
   - Data protection measures
   - Security best practices
   - Vulnerability management

   ### Performance Targets
   - Response time requirements
   - Throughput expectations
   - Resource constraints
   - Optimization priorities
   - Monitoring approach

   ### Documentation Architecture (NEW)
   - Four-layer documentation structure (Management/Technical/Working/Archive)
   - Document organization principles (see DOC_ARCHITECTURE.md)
   - AI context optimization strategy (on-demand loading)
   - Document lifecycle and maintenance schedule
   - KNOWLEDGE.md as documentation index center

3. **Documentation Architecture Setup**:
   - Create initial docs/ directory structure (architecture, api, database, deployment)
   - Initialize KNOWLEDGE.md with documentation index template
   - Explain four-layer architecture to user (refer to DOC_ARCHITECTURE.md)
   - Set up document organization rules in PLANNING.md

4. **Interactive Refinement**:
   - Mark sections as TBD initially
   - Collaborate with user to fill details
   - Validate technical decisions
   - Ensure completeness and accuracy

5. **Integration Setup**:
   - Link with TASK.md creation
   - Establish update procedures
   - Define review cycles
   - Initialize KNOWLEDGE.md documentation index

## Output Format
1. **PLANNING.md File** - Complete project planning document
2. **Summary Report** - Key decisions and action items
3. **Next Steps** - Immediate tasks based on planning
4. **Integration Guide** - How to use with other workflow commands

## Workflow Integration
- Creates foundation for `/wf_02_task`
- Referenced by `/wf_03_prime` for context loading
- Updated through `/wf_08_review` cycles
- Drives `/wf_05_code` implementation standards