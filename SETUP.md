# Setup

## 1. Install the package

Install this repository as a plugin, or copy the three folders under `skills/` into the agent's skills directory.

## 2. Prepare the business truth

Run `noguess` first and keep `BUSINESS-TRUTH.md` in the business project. The Meta Growth System reads it instead of interviewing the owner again.

## 3. Get authorized API access

Follow [the owner/agent setup guide](skills/connect-meta-whatsapp/references/meta-api-access.md)
for Meta login, sandbox token, system user, app/WABA asset assignment, token scopes and
production number setup. Graph API is hosted by Meta; nothing needs downloading. Owner login,
MFA, OTP, permissions and any required review/billing are not bypassed by an agent.

## 4. Provide credentials safely

Use environment variables. Never put access tokens or app secrets in Markdown, JSON committed to Git, browser code, screenshots, or chat.

Shared Graph credentials:

```text
META_ACCESS_TOKEN
META_GRAPH_VERSION
```

WhatsApp preflight additionally needs META_WABA_ID and META_PHONE_NUMBER_ID. The receiver needs the two separate secrets listed below:

```text
META_WABA_ID
META_PHONE_NUMBER_ID
META_APP_SECRET
META_WEBHOOK_VERIFY_TOKEN
```

Advertising only (not required for a CRM/WhatsApp lesson):

```text
META_AD_ACCOUNT_ID
META_PAGE_ID
META_PIXEL_ID
```

`META_GRAPH_VERSION` must be set explicitly so an expired API version cannot be hidden by a stale default.

## 5. Start read-only

Run only the preflight tools for the selected mode. They write redacted reports and never print access-token values.

```bash
python3 skills/build-meta-ads/scripts/meta_preflight.py --out META-ADS-PREFLIGHT.json
python3 skills/connect-meta-whatsapp/scripts/whatsapp_preflight.py --out META-WHATSAPP-PREFLIGHT.json
```

## 6. Keep the first campaign paused (ads only)

Create and review `META-CAMPAIGN-CONFIG.json`. The staging tool defaults to a dry run. Applying the plan requires both `--apply` and the exact approval phrase documented by the tool.

## 7. Test WhatsApp with one owned test number

The test sender defaults to a dry run. A real test requires the exact test-only approval phrase. A returned WhatsApp message ID proves acceptance only. Delivery must be verified from signed webhook status events.


## CRM automation setup

For the student sales flow, follow the
[Supabase callback guide](skills/connect-meta-whatsapp/references/supabase-webhook-setup.md).
Use existing student-owned accounts and inspect their CRM before changing the schema. Supabase
can host the webhook; the domain used by Resend is a separate email requirement. Prepare
synthetic fixtures without live credentials. Add an ad account only for an advertising task.

The legacy WhatsApp preflight flag is not a complete release gate; follow the asset, permission,
subscription and signed-delivery checks in the API access guide.
