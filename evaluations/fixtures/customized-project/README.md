# Fixture: customized-project

The `discount-bug` defect (`apply_discount(1000, 10)` returns `0`, should be `900`) in a project that customizes Axiom under `.axiom/`. Used to check that customization layers are applied, reported, and never allowed to loosen a rule.

- `.axiom/overrides/debugging.md`: a valid override that tightens the skill (a `Root cause:` line and a verbose test run before the final report).
- `.axiom/overrides/verification-before-completion.md`: an invalid override that tries to skip running tests. It must be quoted and not applied.
- `.axiom/workflows/overlays/bug-fix.md`: an overlay whose `after:` names a stage that does not exist. It must be reported, not silently ignored.
- `.axiom/config.md`: a mandatory stage hook before the Repair stage (valid).

Run the tests with `python3 -m unittest discover -s tests -t .` from this directory.
