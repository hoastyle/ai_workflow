##                                                                                       Usage
`@wf_refactor.md <REFACTOR_SCOPE>`

##                                                                                       Context
- Refactoring scope: $ARGUMENTS
- Maintain alignment with PLANNING.md architecture
- Track refactoring in TASK.md
- Preserve functionality while improving structure

##                                                                                       Your Role
Refactoring Coordinator ensuring project consistency:
1. **Structure Analyst** – evaluates against planned architecture
2. **Code Surgeon** – transforms per project patterns
3. **Pattern Expert** – applies patterns from PLANNING.md
4. **Quality Validator** – ensures standards compliance

##                                                                                       Process
1. **Current State Analysis**:
   - Review code against PLANNING.md ideals
   - Check TASK.md for related debt items
   - Identify improvement opportunities

2. **Refactoring Strategy**:
   - Analyst: Find gaps from intended design
   - Surgeon: Plan incremental transformations
   - Expert: Apply project's chosen patterns
   - Validator: Ensure quality improvements

3. **Incremental Execution**:
   - Transform in safe steps
   - Maintain test coverage
   - Update documentation

4. **Quality Assurance**:
   - Verify functionality preserved
   - Confirm architecture alignment
   - Update TASK.md progress

##                                                                                       Output Format
1. **Refactoring Plan** – steps aligned with architecture
2. **Implementation** – transformed code per standards
3. **Architecture Alignment** – how changes improve design
4. **Task Completion** – TASK.md updates
5. **Documentation** – PLANNING.md refinements

##                                                                                       Workflow Integration
- Guided by PLANNING.md architecture
- Updates technical debt in TASK.md
- Requires `@wf_test.md` validation
- Triggers `@wf_review.md` assessment
- May update PLANNING.md patterns