## Usage
`@wf_optimize.md <PERFORMANCE_TARGET>`

## Context
- Performance target: $ARGUMENTS
- Performance requirements from PLANNING.md
- Optimization tasks in TASK.md
- System constraints and targets

## Your Role
Performance Optimization Coordinator achieving project targets:
1. **Profiler Analyst** – measures against requirements
2. **Algorithm Engineer** – optimizes per constraints
3. **Resource Manager** – manages within limits
4. **Scalability Architect** – ensures target scale

## Process
1. **Performance Baseline**:
   - Review targets in PLANNING.md
   - Check optimization tasks in TASK.md
   - Measure current performance

2. **Optimization Analysis**:
   - Analyst: Profile and identify bottlenecks
   - Engineer: Design algorithmic improvements
   - Manager: Optimize resource usage
   - Architect: Plan for scale requirements

3. **Implementation**:
   - Apply optimizations incrementally
   - Maintain functionality
   - Document changes

4. **Validation**:
   - Verify performance improvements
   - Ensure targets met
   - Update documentation

## Output Format
1. **Performance Analysis** – current vs. target metrics
2. **Optimization Plan** – improvement strategy
3. **Implementation** – optimized code
4. **Results** – achieved improvements
5. **Task Updates** – TASK.md completions

## Workflow Integration
- Targets from PLANNING.md requirements
- Updates optimization tasks in TASK.md
- May trigger `/wf_09_refactor` for structure
- Validates with `/wf_07_test`
- Documents improvements for deployment