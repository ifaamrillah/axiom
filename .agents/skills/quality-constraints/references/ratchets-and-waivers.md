# Ratchets and Waivers

Two tools for a bar the codebase cannot meet today. A **ratchet** holds the current value and only lets it improve. A **waiver** is a written, time-boxed exception to one rule for one scope. Use this when proposing a number the project fails, when a change needs an exception, or when reviewing a change to `.axiom/CONSTRAINTS.md`.

## Ratchets

Setting 80% coverage on a codebase at 62% produces a permanently red build, and a team that learns to ignore red builds. A ratchet asks for no target: record today's value and refuse to get worse.

### Procedure

1. **Measure** on the main branch with the real command. Record the value, the commit, and the date.
2. **Record** it in the "Measured, not yet enforced" table (or as a ratchet row) with a direction and a tolerance.
3. **Compare** every change against the recorded value, not against an aspiration.
4. **Tighten** when the value improves: update the recorded number in the same change that improved it, or in a scheduled follow-up. Tightening needs no approval.
5. **Never loosen silently.** Lowering the recorded value is a constraint change: separate change, owner approval, reason recorded.
6. **Graduate** to an enforced threshold once the value has passed the target for two weeks.

### Recording format

```markdown
## Ratchets

| Metric | Value | Direction | Tolerance | Measured | Command |
|---|---|---|---|---|---|
| Project line coverage | 62.4% | must not fall | 0.5 pt | 2026-11-16 @ a1b2c3d | `pytest --cov=app --cov-report=term` |
| ESLint warnings | 214 | must not rise | 0 | 2026-11-16 @ a1b2c3d | `eslint . -f json \| jq '[.[].warningCount] \| add'` |
| PHPStan baseline entries | 1,038 | must not rise | 0 | 2026-11-16 @ a1b2c3d | `grep -c "message:" phpstan-baseline.neon` |
| Main bundle (gzip) | 184 KB | must not grow | 2 KB | 2026-11-16 @ a1b2c3d | `npx size-limit --json` |
| `any` count in src/ | 97 | must not rise | 0 | 2026-11-16 @ a1b2c3d | `grep -rEo ':\s*any\b\|as any\b' src \| wc -l` |
```

### What makes a good ratchet metric

- Deterministic: the same commit gives the same number. Line coverage and lint counts qualify; latency on shared CI runners does not.
- Cheap to compute in CI.
- Moved by the change itself, not by unrelated files. Prefer changed-line or changed-file metrics; use a tolerance for project-wide ones.

### Ratchet check (shell sketch)

```bash
# Fails if project coverage fell more than the tolerance below the recorded value.
recorded=62.4; tolerance=0.5
current=$(pytest --cov=app --cov-report=term | awk '/^TOTAL/ {gsub("%","",$NF); print $NF}')
awk -v c="$current" -v r="$recorded" -v t="$tolerance" 'BEGIN { exit (c + t < r) ? 1 : 0 }' \
  || { echo "coverage $current% < recorded $recorded% (tolerance $tolerance)"; exit 1; }
```

Tool-native ratchets exist and are preferable when present: Jest `coverageThreshold`, `pytest --cov-fail-under`, PHPStan and detekt baselines, ESLint bulk suppressions, `diff-cover --fail-under` for changed lines.

## Waivers

A waiver unblocks one change without deleting the rule for everyone. Deleting or loosening the constraint unblocks every future change forever; a waiver expires.

### Rules

- One rule, one scope (paths, endpoint, or package), one reason.
- An owner who can be asked about it, and an approver who is not the author of the change that needs it.
- An expiry date, 90 days by default, never more than a year.
- A tracking issue for the real fix.
- Recorded where review sees it (the Exceptions table in `.axiom/CONSTRAINTS.md`), and referenced at the suppression site.
- Added in a visible way: its own commit or a called-out line in the PR description. An unannounced new waiver row is a bar-lowering finding.
- Expired waivers fail the check, or are renewed with a new approval.

### Template

```markdown
## Exceptions

| ID | Rule | Scope | Reason | Owner | Approved by | Expires | Tracking |
|---|---|---|---|---|---|---|---|
| W<n> | <constraint row or lint rule id> | <paths or component> | <why the rule cannot be met now, and the risk accepted> | <name> | <name, date> | <YYYY-MM-DD> | <issue link or id> |
```

At the code site, point back at the waiver:

```ts
// eslint-disable-next-line @typescript-eslint/no-explicit-any -- W3: vendor SDK has no types, see ENG-512
```

### Worked example

A team must ship a payment provider integration. The provider's SDK has no TypeScript types, and the project bans `any` (`@typescript-eslint/no-explicit-any: error`). Writing full types for the SDK would take a week.

**Wrong:** change the rule to `warn` in `eslint.config.js` in the same PR. That loosens the bar for the whole codebase, permanently, without review noticing.

**Right:**

1. Confine the untyped surface to one adapter file, `src/payments/provider-adapter.ts`. Everything outside it uses a typed interface the team owns.
2. Add the waiver row:

   | ID | Rule | Scope | Reason | Owner | Approved by | Expires | Tracking |
   |---|---|---|---|---|---|---|---|
   | W3 | `@typescript-eslint/no-explicit-any` | `src/payments/provider-adapter.ts` | Provider SDK ships no types; adapter isolates `any` behind `PaymentGateway` interface. Risk: SDK shape changes go undetected in this file. | Rina | Dimas, 2026-11-16 | 2027-02-14 | PAY-218 |

3. Mark each suppression with `-- W3` and the issue id.
4. Add a contract test that calls the real sandbox and checks the fields the adapter reads, to cover the risk the types would have caught.
5. In review, the reviewer confirms that suppressions appear only in the waived file and that each cites W3.
6. On 2027-02-14 the check fails if W3 is still present. The team either types the SDK (and deletes W3) or renews it with a new approval and reason.

### Waiver check (shell sketch)

```bash
# Fails on any Exceptions row whose expiry date is in the past.
today=$(date +%F)
awk -F'|' -v d="$today" '/^\| *W[0-9]+ *\|/ { gsub(/ /,"",$8); if ($8 < d) { print "expired waiver:" $2; bad=1 } } END { exit bad }' .axiom/CONSTRAINTS.md
```

Adjust the column index to the table you use (here `Expires` is the 7th column, so field 8 after the leading `|`).

## Reviewing a constraint change

| Change | Treatment |
|---|---|
| Threshold raised, rule added, baseline shrunk | Accept; no approval needed |
| Recorded ratchet value updated upward | Accept if the command output supports it |
| Threshold lowered, rule removed or set to warn, stage made non-blocking | Separate change, owner approval, reason recorded |
| New waiver | Approver is not the author; expiry and tracking present |
| Any loosening in the same change as the code that needed it | Blocking finding |

Tightening should be quiet. Loosening should be loud.

Sources: adapted from addyosmani/agent-skills (MIT) (`skills/constraint-driven-development/SKILL.md`) and general practice.
