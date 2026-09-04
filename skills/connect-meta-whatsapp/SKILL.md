---
name: connect-meta-whatsapp
description: Connect, audit, test and operate the official Meta WhatsApp Business Platform Cloud API. Use when the user asks to integrate WhatsApp, connect a WABA or phone number, create or inspect templates, receive webhook messages, track delivery, route leads into a CRM, or diagnose why a WhatsApp message was not received. Default to read-only preflight and dry runs. Real test sends, customer messages, template submissions and production webhook changes require explicit approval.
---

# Connect Meta Whatsapp

Use the official WhatsApp Cloud API. Do not silently replace it with WhatsApp Web automation, QR-linked gateways or unofficial providers.

## Entry checks

1. Read `BUSINESS-TRUTH.md` and `META-TRUTH.md` when present.
2. Identify the exact business portfolio, WABA, phone-number ID, display number ending and CRM.
3. Confirm the customer-consent source, first-message purpose, operator owner and stable customer identity key.
4. Run `scripts/whatsapp_preflight.py` before any send or webhook change.
5. If the required asset or permission is unavailable, give the owner the smallest Meta setup step. A skill cannot bypass login, verification or authorization.

## Delivery truth

Read [references/delivery-contract.md](references/delivery-contract.md).

A successful send response proves only that Meta accepted the request. It does not prove `sent`, `delivered` or `read`. Store the returned WhatsApp message ID and update the message ledger from signed webhook statuses.

Use this state machine:

`prepared -> accepted -> sent -> delivered -> read`

Terminal failure is `failed`. Do not mark a lead as contacted, block a retry, or advance a workflow merely because the request was accepted.

## Webhook contract

Read [references/webhook-contract.md](references/webhook-contract.md).

- Verify GET subscription challenges with a secret verify token.
- Verify every POST using `X-Hub-Signature-256` over the exact raw request bytes.
- Reject invalid signatures before parsing or storing data.
- Deduplicate inbound messages and status events by their immutable Meta IDs.
- Acknowledge valid webhooks quickly and perform slow work after acknowledgement.
- Keep customer messages, delivery statuses and operator actions as separate records.

Use `scripts/verify_webhook_signature.py` to test a captured payload without exposing the app secret.

## Templates and service window

- List the live templates and read their category, language and status.
- Match an outbound message to its real business purpose.
- Do not disguise marketing as utility.
- Outside an open customer-service window, use an approved template.
- Inside the service window, free-form replies may be eligible, but the CRM must still enforce consent, opt-out and message purpose.
- Template submission needs approval of the exact copy, language, variables, header, buttons and category.

## Controlled first test

Prepare a dry run with [assets/WHATSAPP-TEST-CONFIG.example.json](assets/WHATSAPP-TEST-CONFIG.example.json):

```bash
python3 scripts/send_test_template.py --config WHATSAPP-TEST-CONFIG.json --out META-WHATSAPP-TEST-RECEIPT.json
```

Ask for explicit approval before a real test. The script requires both `--apply` and the literal confirmation `TEST_RECIPIENT_ONLY`. The recipient must be an owned or explicitly authorized test number, not a lead.

After acceptance, wait for signed webhook status and update the receipt. If no status arrives, report `accepted, delivery unknown`.

## CRM integration

At minimum, persist:

- normalized customer identity;
- consent source and timestamp;
- inbound Meta message ID;
- outbound operation ID and message purpose;
- returned WhatsApp message ID;
- current delivery status and status timestamps;
- template name and language when used;
- failure code and reason;
- opt-out state;
- operator owner and next action.

Every send needs an idempotency key. An uncertain result must be retried only with the same logical operation ID and only after the delivery ledger is checked.

## Completion standard

Report:

- exact WABA and phone-number assets, redacted where appropriate;
- permissions and profile status;
- live template inventory;
- webhook signature result;
- test recipient ending and template used;
- acceptance ID plus webhook-derived delivery state;
- CRM persistence and deduplication result;
- and the remaining owner or Meta approval step.
