# Webhook contract

## Verification request

For a GET verification request, compare `hub.verify_token` to a secret value stored server-side. If equal, return `hub.challenge` exactly. Otherwise return 403.

## Event request

1. Read the exact raw request bytes.
2. Compute HMAC SHA-256 using the Meta app secret.
3. Compare `sha256=<hex digest>` to `X-Hub-Signature-256` using constant-time comparison.
4. Reject invalid or missing signatures.
5. Parse JSON only after signature verification.
6. Claim each immutable event ID in a database uniqueness constraint.
7. Return 200 quickly for valid duplicates and already processed events.
8. Process CRM and reply work asynchronously where the hosting platform permits it.

## Events to capture

- inbound customer message ID, sender, timestamp and message type
- button or list reply ID
- delivery status message ID, status, timestamp and error
- template and pricing metadata where supplied

Do not log app secrets, tokens, full webhook headers or unrelated personal payload fields.

