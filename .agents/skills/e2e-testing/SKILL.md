---
name: e2e-testing
description: >
  Verify critical user journeys across application boundaries using available
  end-to-end tools. Use when a change affects integrated user-visible behavior.
---

# End-to-End Testing

## Procedure

1. Select critical journeys linked to acceptance criteria.
2. Check environment, test data, account permissions, and cleanup behavior.
3. Prefer deterministic project fixtures; avoid live user or production data.
4. Run only authorized journeys and capture failure evidence.
5. Clean up only test-owned data and report coverage and limitations.

## Fallback

If browser/device automation is unavailable, use lower-level integration checks or a manual checklist and clearly label the reduced coverage.

## References

See [testing](../testing/SKILL.md) and [Playwright integration](../../../integrations/playwright/README.md).
