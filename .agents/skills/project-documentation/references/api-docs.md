# API Documentation

API docs describe a contract: inputs, outputs, errors, and guarantees. Generate the reference from the source of truth when possible and write prose only for what generation cannot express (concepts, auth flow, examples, migration notes).

## Source of truth by API kind

| API kind | Source of truth | Generated reference |
|---|---|---|
| REST/HTTP | OpenAPI file, or annotations that produce it | Swagger UI, Redoc |
| GraphQL | Schema SDL with descriptions | GraphiQL, introspection docs |
| gRPC | `.proto` with comments | protoc-gen-doc |
| TypeScript library | Exported types + TSDoc | TypeDoc, API Extractor |
| Python library | Type hints + docstrings | Sphinx autodoc, mkdocstrings |
| Go | Exported identifiers + doc comments | `go doc`, pkg.go.dev |
| Java/Kotlin | Javadoc / KDoc | javadoc, Dokka |
| PHP | PHPDoc + types | phpDocumentor |
| CLI | `--help` output | Generated man page or README table |
| Events/messages | Schema registry, AsyncAPI, JSON Schema | AsyncAPI HTML |

If the project already publishes one of these, update the source, not a hand-written copy.

## What every operation needs

- Purpose in one sentence.
- Auth requirement and scopes.
- Inputs with type, required/optional, default, constraints (length, range, format).
- Output shape with an example.
- Every error the caller can act on: status or exception type, condition, what to do.
- Side effects and idempotency (is a retry safe?).
- Limits: rate limits, pagination, max payload size.
- Version or "since" note when the API is versioned.

## Examples

TypeScript:

```typescript
/**
 * Creates a refund for a captured payment.
 *
 * @param paymentId - ID of a captured payment (`pay_...`).
 * @param amountCents - Amount in minor units; at most the remaining captured amount.
 * @returns The refund, status `pending` until the provider confirms.
 * @throws {NotFoundError} If the payment does not exist.
 * @throws {RefundLimitError} If amountCents exceeds the refundable balance.
 * @remarks Idempotent per (paymentId, idempotencyKey). Safe to retry.
 * @example
 * const r = await createRefund('pay_123', 500, { idempotencyKey: orderId });
 */
```

Python:

```python
def create_refund(payment_id: str, amount_cents: int, *, idempotency_key: str) -> Refund:
    """Create a refund for a captured payment.

    Args:
        payment_id: ID of a captured payment ("pay_...").
        amount_cents: Minor units; at most the refundable balance.
        idempotency_key: Reusing a key returns the original refund.

    Returns:
        The refund, status "pending" until the provider confirms.

    Raises:
        NotFoundError: The payment does not exist.
        RefundLimitError: amount_cents exceeds the refundable balance.
    """
```

OpenAPI:

```yaml
/payments/{id}/refunds:
  post:
    summary: Refund a captured payment
    security: [{ bearerAuth: [payments:write] }]
    parameters:
      - { name: Idempotency-Key, in: header, required: true, schema: { type: string } }
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [amount_cents]
            properties:
              amount_cents: { type: integer, minimum: 1 }
    responses:
      '201': { description: Refund created, content: { application/json: { schema: { $ref: '#/components/schemas/Refund' } } } }
      '404': { description: Payment not found }
      '409': { description: Same Idempotency-Key with a different body }
      '422': { description: Amount exceeds refundable balance }
```

## Changing an API

- Update the reference in the same change as the code.
- Mark breaking changes clearly and add a migration note with before/after examples.
- Deprecate before removing: state the replacement and the removal version or date.
- Check examples still run (doc tests, `--help` snapshot, a contract test against the OpenAPI file).

## Verification

| Check | Command (examples) |
|---|---|
| OpenAPI is valid | `npx @redocly/cli lint openapi.yaml` |
| Spec matches implementation | contract tests, or compare generated spec with committed spec in CI |
| Docstring examples run | `python -m doctest`, `go test` (Example functions), `cargo test --doc` |
| Reference builds | `npx typedoc`, `mkdocs build --strict`, `./gradlew dokkaHtml` |

Run what the project already uses. Report anything you could not run.

Sources: adapted from addyosmani/agent-skills (MIT) documentation-and-adrs, and general practice.
