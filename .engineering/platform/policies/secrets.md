# Secrets Policy

## Purpose

Prevent credentials and sensitive authentication material from being exposed through source code, logs, documentation or AI-assisted workflows.

## Secrets Include

Examples include:

- passwords
- API keys
- access tokens
- refresh tokens
- private keys
- connection credentials
- signing keys
- client secrets
- privileged certificates

## 1. Source Control

Secrets must not be committed to source control.

This applies to:

- application code
- configuration
- test files
- examples
- documentation
- scripts

Use placeholders in examples.

## 2. Secret Storage

Production secrets must use an approved secret-management mechanism.

Examples may include:

- managed secret stores
- workload identity
- platform-managed credentials

Prefer identity-based access over long-lived static credentials where practical.

## 3. Environment Variables

Environment variables may be used to expose secrets to processes where appropriate.

They are not themselves a secret-management system.

Underlying secret values must still be stored securely.

## 4. Logs

Secrets must never be intentionally logged.

Logging mechanisms should avoid automatically serialising objects that may contain credentials.

## 5. AI Systems

Do not intentionally provide production secrets to AI models or coding agents unless:

- the organisation explicitly permits the system
- the tool requires the credential to perform an authorised operation
- appropriate security controls exist

Prefer agents operating through secured tool integrations rather than receiving raw secret values.

## 6. Testing

Tests must use:

- fake credentials
- ephemeral credentials
- isolated development credentials

Production credentials must not be embedded in tests.

## 7. Secret Detection

Repositories should enable automated secret scanning where practical.

Detected secrets must be treated as potentially compromised.

Deleting the secret from a later commit is not sufficient remediation.

## 8. Compromise Response

If a secret is exposed:

1. revoke or rotate it promptly
2. assess exposure
3. remove it from active configuration
4. remediate repository exposure where necessary
5. document material incidents according to organisational procedures

## 9. Least Privilege

Credentials should grant only required permissions and should be scoped to the smallest practical environment and resource set.
