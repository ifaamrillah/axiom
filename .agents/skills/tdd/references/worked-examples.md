# Worked Red-Green-Refactor Examples

Open this when you need a concrete model of one full cycle in Python, TypeScript, or Go, or of a bug-fix cycle. Each example shows the test, the expected red output, the minimal green code, and the refactor.

## What a valid red looks like

| Red output | Valid? | Why |
|---|---|---|
| `AssertionError: assert 0 == 15` | Yes | The behavior is missing; the assertion caught it |
| `expected 'tag:"urgent"', received ''` | Yes | Same |
| `NameError: name 'apply_discount' is not defined` | Not yet | Create the empty function or stub, then rerun until the assertion fails |
| `SyntaxError`, `cannot find module`, `undefined: Foo` | No | The test never ran its assertion |
| Test passes on first run | No | Either the behavior already exists (use a characterization check) or the test asserts nothing useful |
| Fails with a different message than the one you predicted | Investigate | You may be testing something other than you think |

Predict the failure message before you run the test. A surprise is information.

## Python (pytest): cart discount

Behavior: orders of 100.00 or more get 10 percent off; smaller orders pay full price.

**Red 1**

```python
# tests/test_pricing.py
from decimal import Decimal
from shop.pricing import order_total

def test_orders_of_100_or_more_get_ten_percent_off():
    assert order_total([Decimal("60.00"), Decimal("40.00")]) == Decimal("90.00")
```

```sh
pytest tests/test_pricing.py -q
# ImportError: cannot import name 'order_total'   -> not a valid red yet
```

Add a stub `def order_total(prices): return Decimal("0")` and rerun:

```
E  AssertionError: assert Decimal('0') == Decimal('90.00')   -> valid red
```

**Green 1:** the smallest code that passes.

```python
# shop/pricing.py
from decimal import Decimal

def order_total(prices):
    return sum(prices, Decimal("0")) * Decimal("0.9")
```

**Red 2:** the next test forces the threshold.

```python
def test_orders_under_100_pay_full_price():
    assert order_total([Decimal("99.99")]) == Decimal("99.99")
# E  AssertionError: assert Decimal('89.991') == Decimal('99.99')
```

**Green 2**

```python
THRESHOLD = Decimal("100.00")

def order_total(prices):
    subtotal = sum(prices, Decimal("0"))
    if subtotal >= THRESHOLD:
        return (subtotal * Decimal("0.9")).quantize(Decimal("0.01"))
    return subtotal
```

**Red 3:** the boundary. `Decimal("100.00")` must give `Decimal("90.00")`. Add it as a parametrized case with literal expectations:

```python
import pytest

@pytest.mark.parametrize("prices, expected", [
    ([Decimal("100.00")], Decimal("90.00")),   # exact threshold
    ([Decimal("99.99")], Decimal("99.99")),    # just below
    ([], Decimal("0")),                        # empty cart
])
def test_order_total_boundaries(prices, expected):
    assert order_total(prices) == expected
```

If this passes immediately, mutate `>=` to `>` and confirm the exact-threshold case fails. Restore it.

**Refactor:** extract `DISCOUNT_RATE`, rename `prices` to `line_amounts` if clearer. Run `pytest tests/test_pricing.py -q` after each step.

## TypeScript (Vitest or Jest): slug generator

Behavior: `slugify("Hello, World!")` returns `"hello-world"`.

**Red**

```ts
// src/slug.test.ts
import { describe, it, expect } from "vitest"; // Jest: globals, no import
import { slugify } from "./slug";

describe("slugify", () => {
  it("lowercases and joins words with single hyphens", () => {
    expect(slugify("Hello, World!")).toBe("hello-world");
  });
});
```

Stub `export const slugify = (s: string) => "";` then run `npx vitest run src/slug.test.ts`:

```
AssertionError: expected '' to be 'hello-world'
```

**Green**

```ts
export function slugify(input: string): string {
  return input.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}
```

**Next reds**, one at a time, each with a literal expectation:

```ts
it("collapses repeated separators", () => {
  expect(slugify("a  --  b")).toBe("a-b");
});
it("returns an empty string for input with no letters or digits", () => {
  expect(slugify("!!!")).toBe("");
});
it("strips accents", () => {
  expect(slugify("Crème Brûlée")).toBe("creme-brulee");
});
```

The accent test fails (`"cr-me-br-l-e"`). Green it with `input.normalize("NFKD").replace(/[̀-ͯ]/g, "")` before lowercasing.

**Refactor:** name the regexes (`NON_ALNUM`, `EDGE_HYPHENS`). Rerun the file.

## Go (testing package): table-driven parser

Behavior: `ParseDuration("1h30m")` returns 90 minutes; invalid input returns an error.

**Red**

```go
// duration_test.go
package clock

import (
	"testing"
	"time"
)

func TestParseDuration(t *testing.T) {
	tests := []struct {
		name    string
		in      string
		want    time.Duration
		wantErr bool
	}{
		{"hours and minutes", "1h30m", 90 * time.Minute, false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ParseDuration(tt.in)
			if (err != nil) != tt.wantErr {
				t.Fatalf("ParseDuration(%q) err = %v, wantErr %v", tt.in, err, tt.wantErr)
			}
			if got != tt.want {
				t.Errorf("ParseDuration(%q) = %v, want %v", tt.in, got, tt.want)
			}
		})
	}
}
```

Stub `func ParseDuration(s string) (time.Duration, error) { return 0, nil }`, then:

```sh
go test ./clock -run TestParseDuration -v
# duration_test.go:25: ParseDuration("1h30m") = 0s, want 1h30m0s
```

**Green**

```go
func ParseDuration(s string) (time.Duration, error) {
	return time.ParseDuration(s)
}
```

**Next reds:** add rows, not new functions.

```go
{"empty is an error", "", 0, true},
{"days are supported", "2d", 48 * time.Hour, false},
{"negative is rejected", "-5m", 0, true},
```

`"2d"` fails because the standard library has no day unit. `"-5m"` fails because the standard library accepts negatives. Green each with the smallest branch, then refactor the day handling into a helper. Run with `-race` when the code touches goroutines.

## Bug-fix cycle (any language)

Report: "Splitting `a,,b` returns `['a', 'b']`; it should keep the empty field."

1. Write the test with the reported input and the expected output from the report: `split("a,,b") == ["a", "", "b"]`.
2. Run it. The red must show the reported symptom: `expected ['a', '', 'b'], got ['a', 'b']`. If it passes, you have not reproduced the bug. Stop and investigate before fixing.
3. Fix at the cause (for example, a `filter(Boolean)` that drops empty strings), not at the symptom.
4. Run the test green, then the module's suite. Keep the test, named for the behavior (`keeps empty fields between consecutive separators`), not the ticket number alone.

## Cycle log template

Record each cycle briefly in your handoff:

```
Behavior: orders >= 100.00 get 10% off
Red:   pytest tests/test_pricing.py::test_orders_of_100_or_more... -> AssertionError 0 == 90.00
Green: same command -> 1 passed
Suite: pytest -q -> 48 passed
```

Sources: adapted from obra/superpowers (MIT) skills/test-driven-development/SKILL.md, addyosmani/agent-skills (MIT) skills/test-driven-development/SKILL.md, and general practice.
