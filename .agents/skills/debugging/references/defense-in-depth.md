# Defense in Depth

Fix the root cause first. Then decide whether other layers should also refuse the bad state, so the same class of bug cannot return through a different path.

A single check at the origin can be bypassed later: a new caller, a refactor, a mock in tests, a background job that skips the API. Extra layers turn "we fixed this occurrence" into "this state cannot get far".

## When to add layers

Add them when at least one is true:

- The bad state caused data loss, a security issue, or damage outside the process (files written in the wrong place, wrong account charged).
- More than one path reaches the dangerous operation.
- The bug was silent: it produced wrong output instead of an error.

Skip them when the fix is local, the value cannot arrive from elsewhere, and a guard would only duplicate a type the compiler already enforces.

## The layers

| Layer | Purpose | Example check |
|---|---|---|
| 1. Entry | Reject invalid input at the boundary (API, CLI, message consumer) | Schema validation; non-empty path that exists |
| 2. Domain | Refuse states that make no sense for this operation | `quantity > 0`; invoice currency matches account |
| 3. Environment guard | Block dangerous actions in the wrong context | In tests, refuse to write outside a temp dir; refuse prod DB URL in dev |
| 4. Instrumentation | Record enough context to find the next bypass fast | Log caller stack and inputs before the dangerous call |

The fix lives where the bad state originates. Layers 1–4 are guards, not the fix.

## Examples

TypeScript, a test wrote files into the repository because a temp path was empty:

```ts
// Layer 1: entry
export function createProject(name: string, dir: string) {
  if (!dir.trim()) throw new Error("createProject: dir is empty");
  if (!fs.statSync(dir, { throwIfNoEntry: false })?.isDirectory())
    throw new Error(`createProject: not a directory: ${dir}`);
  // ...
}

// Layer 3: environment guard
function assertSafeWrite(dir: string) {
  if (process.env.NODE_ENV === "test" && !path.resolve(dir).startsWith(os.tmpdir()))
    throw new Error(`refusing to write outside tmpdir during tests: ${dir}`);
}
```

Python, money must never be negative or mixed-currency:

```python
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str
    def __post_init__(self):                      # layer 2: domain invariant
        if self.amount < 0:
            raise ValueError(f"negative amount {self.amount}")
        if len(self.currency) != 3:
            raise ValueError(f"bad currency {self.currency!r}")
```

Go, refuse a destructive call against the wrong database:

```go
func (m *Migrator) DropAll(ctx context.Context) error {
    if m.env == "production" { // layer 3
        return errors.New("DropAll refused in production")
    }
    // ...
}
```

SQL, let the database enforce what code forgets:

```sql
ALTER TABLE invoices ADD CONSTRAINT invoices_total_nonneg CHECK (total >= 0);
ALTER TABLE users ALTER COLUMN email SET NOT NULL;
```

## Make invalid states unrepresentable

Often the strongest layer is a type, not a check:

- Parse once at the boundary into a validated type (`EmailAddress`, `NonEmptyPath`, `PositiveInt`) and pass that type inward.
- Use enums or sum types instead of free strings for states.
- Use constructors that validate and keep fields private.
- Use database constraints (`NOT NULL`, `CHECK`, foreign keys, unique indexes).

## Test each layer

1. Keep the regression test for the original bug (it exercises the fix).
2. For each guard, write a test that bypasses the layer above it and confirms this layer still refuses. For example, call the domain function directly with the bad value.
3. Do not let a guard hide the original failure in tests. A guard that throws is good. A guard that silently coerces (`?? 0`, `or ""`) is a new bug.

## Anti-patterns

| Pattern | Problem | Do instead |
|---|---|---|
| `if (x == null) return` scattered everywhere | Silently skips work; hides the producer | Fix the producer; throw with context at the boundary |
| `try { ... } catch {}` around the symptom | Swallows the evidence | Let it fail, or rethrow with context |
| Defaults that mask missing config | Wrong behavior in production | Fail fast at startup when required config is missing |
| Guards only in the UI | Other clients bypass them | Enforce in the service and the database |

Sources: adapted from obra/superpowers (MIT) `skills/systematic-debugging/defense-in-depth.md`, `root-cause-tracing.md`, and general practice.
