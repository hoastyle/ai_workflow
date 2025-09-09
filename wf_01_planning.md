##                                                                                      Usage
`@wf_planning.md <PROJECT_NAME>`

##                                                                                      Purpose
Create or update PLANNING.md to establish comprehensive project documentation that:
- Defines project architecture and technical decisions
- Documents development workflow and standards
- Provides context for AI assistants and developers
- Maintains project continuity across sessions

##                                                                                      Process
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
   - Technology decisions rationale

   ### Technology Stack
   - Programming languages and versions
   - Frameworks and libraries
   - Database and storage systems
   - Development and deployment tools
   - Third-party services

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

3. **Interactive Refinement**:
   - Mark sections as TBD initially
   - Collaborate with user to fill details
   - Validate technical decisions
   - Ensure completeness and accuracy

4. **Integration Setup**:
   - Link with TASK.md creation
   - Establish update procedures
   - Define review cycles

##                                                                                      Output Format
1. **PLANNING.md File** - Complete project planning document
2. **Summary Report** - Key decisions and action items
3. **Next Steps** - Immediate tasks based on planning
4. **Integration Guide** - How to use with other workflow commands

##                                                                                      Workflow Integration
- Creates foundation for `@wf_task.md`
- Referenced by `@wf_prime.md` for context loading
- Updated through `@wf_review.md` cycles
- Drives `@wf_code.md` implementation standards