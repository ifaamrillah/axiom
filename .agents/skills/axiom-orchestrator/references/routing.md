# Routing

| Request | Starting point |
|---|---|
| Unknown or poorly documented repository | `workflows/codebase-onboarding/WORKFLOW.md` |
| Vague idea or "build me X" without acceptance criteria | `product-discovery` (elicitation), then Feature Development |
| New user-visible or technical capability | `workflows/feature-development/WORKFLOW.md` |
| Defect with understood scope | `debugging`, then `tdd` for the regression test, then review gates (`workflows/bug-fix/WORKFLOW.md`) |
| Structural change preserving behavior | `workflows/refactoring/WORKFLOW.md` with blast-radius analysis |
| Risk review | `security-audit` (guidance mode by default) or `code-review`, scoped to the request |
| Spec, plan, and tasks exist; check consistency or remaining work | `spec-analysis` |
| Missing or eroding quality bar | `quality-constraints` |
| Release preparation | `release-management` and `workflows/release/WORKFLOW.md` |
| Single focused question or change | Relevant specialist skill; apply the [kernel](kernel.md) and skip workflow ceremony |
| Any completion claim | `verification-before-completion` |

Ask for clarification only when ambiguity materially changes the solution or risk. Keep assumptions explicit and reversible when possible.

## Scope sizing

| Signal | Process |
|---|---|
| One file, obvious correctness, low risk | Kernel only; focused check |
| Isolated bug or small feature | Bug-fix or lightweight plan (checklist with `step → verify`) |
| Multi-file, user-visible, or cross-module | Full workflow with a state file |
| Security-sensitive, data migration, public API | Full workflow plus security review and adversarial review of key claims |
