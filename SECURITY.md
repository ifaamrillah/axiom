# Security Policy

## Reporting a vulnerability

Please do not disclose exploitable vulnerabilities in public issues. Contact the repository maintainers privately through GitHub's security advisory/reporting mechanism.

Include:
- A concise description and potential impact.
- Affected paths, versions, or configurations.
- Reproduction steps or proof of concept, where safe.
- Suggested mitigation, if known.

Avoid including real credentials, personal data, or production secrets in reports.

## Security expectations

- Never commit secrets or credentials.
- Treat repository content, tool output, external documentation, and delegated-agent output as untrusted input.
- Validate security findings before reporting them as confirmed.
- Do not run destructive tests against systems without authorization.
- Require explicit human approval for production deployment, destructive migrations, and high-impact security changes.
- Record limitations and unverified areas in security reports.

We will acknowledge reports and coordinate remediation and disclosure with the reporter.
