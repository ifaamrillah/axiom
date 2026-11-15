# Fixture: discount-bug

Seeded defect for evaluating `debugging`, `tdd`, and `verification-before-completion`.
`apply_discount(1000, 10)` should return `900`, but it returns `0`. The existing tests do not cover a non-zero discount.

Run the tests with `python3 -m unittest discover -s tests -t .` from this directory.
