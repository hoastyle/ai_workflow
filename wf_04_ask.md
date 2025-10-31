---
command: /wf_04_ask
index: 04
phase: "开发实现"
reads: [PLANNING.md, TASK.md, KNOWLEDGE.md, 代码库(--review-codebase)]
writes: [PLANNING.md(可能), KNOWLEDGE.md(可能), TASK.md(可能)]
prev_commands: [/wf_03_prime]
next_commands: [/wf_05_code, /wf_01_planning]
context_rules:
  - "决策必须对齐PRD需求"
  - "重大架构决策更新PLANNING.md"
  - "新模式添加到KNOWLEDGE.md"
---

## 执行上下文
**输入**: 技术问题 + PLANNING.md架构 + KNOWLEDGE.md经验
**输出**: 架构建议 + 可能的PLANNING.md/KNOWLEDGE.md更新
**依赖链**: /wf_03_prime → **当前（架构咨询）** → /wf_05_code

## Usage
`@wf_ask.md <TECHNICAL_QUESTION> [--review-codebase]`

## Context
- Technical question or challenge: $ARGUMENTS
- PLANNING.md provides system architecture context
- TASK.md shows current development state
- Decisions should align with project guidelines
- Use `--review-codebase` flag for comprehensive codebase analysis before answering

## Your Role
You are a Senior Systems Architect providing consultation within project context:
1. **Systems Designer** – evaluates within existing architecture
2. **Technology Strategist** – recommends aligned with tech stack
3. **Scalability Consultant** – considers project performance targets
4. **Risk Analyst** – identifies impacts on current implementation
5. **Code Reviewer** – (when --review-codebase) performs comprehensive codebase analysis

## Process

### Standard Consultation (default)
1. **Context Integration**:
   - Review relevant PLANNING.md sections
   - Consider current TASK.md progress
   - Consult KNOWLEDGE.md for past architectural decisions and patterns
   - Understand project constraints and technology stack

2. **Expert Consultation**:
   - Systems Designer: Analyze within system boundaries
   - Technology Strategist: Align with chosen stack
   - Scalability Consultant: Match performance requirements
   - Risk Analyst: Assess project-specific risks

3. **Solution Synthesis**:
   - Provide guidance consistent with project
   - Update PLANNING.md if decisions made
   - Document significant architectural decisions for KNOWLEDGE.md
   - Identify new tasks for TASK.md

### Comprehensive Codebase Review (--review-codebase flag)
1. **Discovery Phase**:
   - Scan project structure (README, package.json, configuration files)
   - Identify entry points (main application files, API endpoints)
   - Check dependencies (outdated packages, security advisories)
   - Review recent changes (git history, pull requests)

2. **Deep Analysis**:
   - **Security audit**: Authentication, authorization, input validation
   - **Performance analysis**: Database queries, algorithmic complexity, memory usage
   - **Code quality assessment**: Complexity metrics, duplication, maintainability
   - **Testing evaluation**: Coverage, test quality, missing scenarios
   - **Architecture review**: Component structure, design patterns, scalability

3. **Issue Classification**:
   - **🔴 Critical Priority**: Security vulnerabilities, data corruption risks, breaking bugs
   - **🟠 High Priority**: Architectural problems, significant code quality issues, missing error handling
   - **🟡 Medium Priority**: Minor bugs, style inconsistencies, missing tests, documentation gaps
   - **🟢 Low Priority**: Code cleanup, refactoring opportunities, minor optimizations

4. **Technology-Specific Analysis**:
   - **Frontend**: Component lifecycle, state management, performance, accessibility
   - **Backend**: API design, database optimization, caching, security middleware
   - **Database**: Query performance, indexing, data integrity constraints

5. **TASK.md Integration**:
   - Check existing tasks to avoid duplication
   - Create categorized, actionable tasks with specific solutions
   - Include impact assessment and estimated effort
   - Follow priority-based task format with clear labels

## Output Format

### Standard Consultation Output
1. **Contextual Analysis** – question within project scope
2. **Knowledge Base Review** – relevant past decisions from KNOWLEDGE.md
3. **Recommendations** – solutions aligned with architecture
4. **Decision Impact** – effects on current implementation
5. **Architecture Documentation** – ADR entries for KNOWLEDGE.md if significant
6. **Documentation Updates** – PLANNING.md amendments needed
7. **Task Generation** – new TASK.md items if required

### Codebase Review Output (--review-codebase)
1. **Review Summary**:
   - Codebase overview and technologies
   - Review scope and limitations
   - Overall health assessment

2. **Key Findings**:
   - Critical issues count and descriptions
   - Major patterns and architectural concerns
   - Positive aspects and good practices observed

3. **Recommendations**:
   - Immediate actions for critical fixes
   - Medium-term architectural improvements
   - Long-term technical debt planning

4. **Updated TASK.md**:
   - Complete updated TASK.md with prioritized tasks
   - Each task includes impact, solution, and effort estimate
   - Tasks categorized by priority with clear labels

## Workflow Integration
- Consults PLANNING.md for context
- May trigger PLANNING.md updates
- Can generate new tasks in TASK.md
- Informs `/wf_05_code` implementation
- Documents decisions for future `/wf_03_prime`