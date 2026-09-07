# Supabase-hosted Meta webhook

Read for a student callback setup, deployment or diagnosis. Inspect current Supabase function
and Meta documentation before copying commands; CLI/auth defaults can change.

Before connection, follow [meta-api-access.md](meta-api-access.md) for owner login, system-user
asset assignment, token scopes, safe secret storage and read-only proof.

## Assets and credentials

| Item | Owner or source | Purpose |
|---|---|---|
| Business portfolio / Business ID | Created/selected in Meta | Business ownership |
| Developer app / App ID | Meta app configured with WhatsApp | Integration |
| WhatsApp Business Account / WABA ID | Meta WhatsApp setup | Account/templates |
| Business number / Phone Number ID | Business controls and registers number; Meta assigns ID | Sending number |
| Access token | Generated through authorized Meta setup | Server Graph API requests |
| App Secret | Meta developer app | Verify incoming event signatures |
| Verify token | You choose; configure same value in handler and Meta | GET challenge only |
| Callback URL | Your deployed handler's hosting platform | Receive incoming messages/statuses |

Business Suite/Business Manager and WhatsApp Manager manage assets, not your app hosting.
Use appropriate token asset access and whatsapp_business_messaging / whatsapp_business_management
permissions; business_management applies to some portfolio operations. A temporary test token
is not a production credential strategy. Handle expiry/revocation. Complete account-required
registration, display name, verification and billing; do not claim test setup and multi-client
Embedded Signup have identical requirements. This skill's classroom workflow is one business.

## The URL comes from deployment

The agent writes `meta-webhook`; deploying the Edge Function provides an address like:

`https://<project-ref>.supabase.co/functions/v1/meta-webhook`

That is a pattern, not a ready endpoint. Paste the actual HTTPS URL into Meta's Callback URL
field with your chosen verify token. Subscribe the messages field and the app to the correct
WABA. Verify the actual subscription and a real owned-recipient event, not only the dashboard
challenge. Meta posts events to this address; it does not create your handler or callback URL.

Supabase can run it; no separate dedicated server is required. A server/function-capable web
host or a dedicated server is an alternative. A static-only host is not. A custom domain is
optional for the Supabase webhook; Resend needs an owned verified sending domain. Localhost
alone cannot receive Meta events; a temporary public HTTPS tunnel is for authorized testing,
not a durable production deployment.

Receive: Meta -> hosted webhook -> durable CRM/event state.
Send: job/operator -> server handler -> Meta Graph API -> customer.
Status: Meta -> webhook -> provider ledger. Acceptance is not handset delivery.

## Handler and hosting checks

- GET: require hub.mode=subscribe, compare hub.verify_token, return hub.challenge as plain
  text only on match; reject otherwise.
- POST: preserve raw bytes; authenticate X-Hub-Signature-256 with HMAC SHA-256 and App Secret
  before parsing. Verify object/field, expected WABA and Phone Number ID before routing.
- Meta sends no Supabase user JWT or project API key. For only this external webhook, bypass
  those gateway/SDK checks and enforce the Meta signature in the handler. Current docs use
  verify_jwt=false; with the withSupabase wrapper, auth:'none' plus your own signature check.
  Keep operator and sending endpoints authenticated. Public reachability is not permission
  to write the CRM without signature verification.
- Persist/deduplicate required events or enqueue durably BEFORE returning success. On storage
  failure return a retryable failure. Process slow work via durable jobs, not a detached promise.
- Distinguish inbound message IDs from status transitions. A WAMID alone is not a unique
  status event: delivered/read share it. Deduplicate status identity including status and
  provider timestamp, while handling replay/order safely.
- Store Meta, Resend and privileged Supabase credentials in backend secrets only. Apply RLS
  and least privilege to CRM tables. Never print values for troubleshooting.
- Validate GET mismatch, unsigned POST, wrong account, duplicate event, persistence failure,
  delayed status and one signed delivery receipt. Keep an isolated rollback path for deployment.

Official references:
[Supabase quickstart](https://supabase.com/docs/guides/functions/quickstart),
[external webhook auth](https://supabase.com/docs/guides/functions/auth),
[Meta-owned callback example](https://github.com/fbsamples/business-messaging-sample-tech-provider-app/blob/main/README.md),
[Meta Cloud API](https://www.postman.com/meta/whatsapp-business-platform/documentation/wlk6lh4/whatsapp-cloud-api).
