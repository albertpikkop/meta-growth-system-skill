# Setup

## 1. Install the package

Install this repository as a plugin, or copy the three folders under `skills/` into the agent's skills directory.

## 2. Prepare the business truth

Run `noguess` first and keep `BUSINESS-TRUTH.md` in the business project. The Meta Growth System reads it instead of interviewing the owner again.

## 3. Provide credentials safely

Use environment variables. Never put access tokens or app secrets in Markdown, JSON committed to Git, browser code, screenshots, or chat.

Required for advertising reads:

```text
META_ACCESS_TOKEN
META_GRAPH_VERSION
META_AD_ACCOUNT_ID
```

Additional variables for WhatsApp Cloud API:

```text
META_WABA_ID
META_PHONE_NUMBER_ID
META_APP_SECRET
META_WEBHOOK_VERIFY_TOKEN
```

Optional asset identifiers:

```text
META_PAGE_ID
META_PIXEL_ID
```

`META_GRAPH_VERSION` must be set explicitly so an expired API version cannot be hidden by a stale default.

## 4. Start read-only

Run the preflight tools first. They write redacted reports and never print access-token values.

```bash
python3 skills/build-meta-ads/scripts/meta_preflight.py --out META-ADS-PREFLIGHT.json
python3 skills/connect-meta-whatsapp/scripts/whatsapp_preflight.py --out META-WHATSAPP-PREFLIGHT.json
```

## 5. Keep the first campaign paused

Create and review `META-CAMPAIGN-CONFIG.json`. The staging tool defaults to a dry run. Applying the plan requires both `--apply` and the exact approval phrase documented by the tool.

## 6. Test WhatsApp with one owned test number

The test sender defaults to a dry run. A real test requires the exact test-only approval phrase. A returned WhatsApp message ID proves acceptance only. Delivery must be verified from signed webhook status events.

