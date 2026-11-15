# Approval Policy

Require explicit user authorization before:
- Deploying to production or changing live production infrastructure.
- Destructive database migrations, data deletion, or irreversible operations.
- Rotating or revoking credentials with service impact.
- Publishing releases or packages under the user's identity when not already authorized.
- Making externally visible changes with material business, legal, or security impact.

Preparation, local validation, and non-destructive staging work may proceed within the task scope. An agent must state what approval is needed and why; it must not imply approval from silence.
