# Fixture: tenant-billing

A small multi-tenant billing service (standard library only) with several modules. It contains subtle seeded defects, some security issues and some correctness bugs, plus safe patterns that look risky. It is used to measure how much detail `security-audit` and `code-review` catch. Do not use this code.

Run the tests: `python3 -m unittest discover -s tests -t .`
