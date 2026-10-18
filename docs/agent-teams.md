# Agent team spawn prompts

Paste-in prompts for Claude Code agent teams. Adjust the folder names and the model per teammate.

## Full project team (frontend, backend, database, tests)

```
Create an agent team with these specialists:

1. Frontend Engineer: Own all files in frontend/ and src/components/.
   Focus on React/TypeScript. Use Sonnet to manage costs.

2. Backend Engineer: Own all files in backend/, api/, and services/.
   Focus on the API work. Use Opus.

3. Database Engineer: Own all migration and schema files.
   Focus on PostgreSQL. Use Sonnet.

4. Security/QA Engineer: Review all changes, own all test files.
   Run test suites before and after. Use Sonnet.

Require plan approval from all teammates before they modify any shared interfaces or configs.
I will operate in delegate mode as the coordinator.
```

## Lightweight feature team (2 agents)

```
Create an agent team:

1. Implementer: Own the feature files. Build the feature per the task description. Use Sonnet.
2. Reviewer: Review all changes for security, correctness, and test coverage. Use Sonnet.

Wait for the implementer to finish before the reviewer starts their review.
```

## Debugging team (competing hypotheses)

```
Create an agent team to investigate [describe the bug]:

Spawn 3 teammates, each investigating a different hypothesis:
1. Hypothesis A: [describe theory]
2. Hypothesis B: [describe theory]
3. Hypothesis C: [describe theory]

Have them talk to each other to challenge and disprove each other's theories.
Converge on the most likely root cause before proposing a fix.
```

## Code review team (3 perspectives)

```
Create an agent team to review [PR/changeset]:

1. Security Reviewer: Focus on auth, input validation, secrets, OWASP top 10.
2. Performance Reviewer: Focus on query efficiency, rendering, memory, bundle size.
3. Test Reviewer: Focus on coverage gaps, edge cases, missing assertions.

Each reviewer works independently, then share findings with the group.
Synthesize a final review summary.
```

## AI agent system team

```
Create an agent team for AI system work:

1. AI/ML Engineer: Own agent code, prompts, and protocol files. Use Opus.
2. Backend Engineer: Own API routes and WebSocket handlers that connect to agents. Use Sonnet.
3. Security/QA Engineer: Review all prompt injection vectors, validate agent boundaries. Use Sonnet.

The AI/ML Engineer must get plan approval before modifying any agent communication patterns.
```

## Tips

- Each teammate is billed separately. Sonnet for routine work, Opus for reasoning.
- Never let two teammates edit the same file. Assign clear boundaries.
- Delegate mode (`Shift+Tab`) keeps the lead coordination-only.
- Add "Require plan approval" for risky changes.
- Start with 2 or 3 teammates. Scale up only if needed.
