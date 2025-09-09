##                                                                                       Usage
`@wf_deploy_check.md <DEPLOYMENT_TARGET>`

##                                                                                       Context
- Deployment target: $ARGUMENTS
- Deployment requirements from PLANNING.md
- Deployment tasks in TASK.md
- Production readiness criteria

##                                                                                       Your Role
Deployment Readiness Coordinator ensuring safe deployment:
1. **Quality Agent** – validates code and test completeness
2. **Security Auditor** – ensures security compliance
3. **Operations Engineer** – verifies infrastructure readiness
4. **Risk Assessor** – evaluates deployment risks

##                                                                                       Process
1. **Readiness Assessment**:
   - Check deployment criteria in PLANNING.md
   - Review completed tasks in TASK.md
   - Validate prerequisites

2. **Multi-Layer Validation**:
   - Quality: Verify tests and coverage
   - Security: Validate security measures
   - Operations: Check infrastructure setup
   - Risk: Assess potential issues

3. **Go/No-Go Decision**:
   - Synthesize all findings
   - Make deployment recommendation
   - Document decision rationale

4. **Deployment Planning**:
   - Create deployment steps
   - Define rollback procedures
   - Set monitoring requirements

##                                                                                       Output Format
1. **Readiness Report** – comprehensive assessment
2. **Risk Analysis** – identified risks and mitigations
3. **Deployment Plan** – step-by-step procedure
4. **Monitoring Setup** – post-deployment checks
5. **Task Updates** – deployment task status

##                                                                                       Workflow Integration
- Validates against PLANNING.md requirements
- Checks TASK.md completeness
- Requires passing `@wf_test.md`
- Gates actual deployment
- Updates deployment documentation