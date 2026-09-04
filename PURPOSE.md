# Purpose

## Objective

Give GrowTricity students a safe, reusable way to complete most repeatable Meta Ads and WhatsApp Cloud API integration work without exposing GrowTricity's production credentials, IDs, customers or account-specific operating history.

## Version 1 current state

- One installable plugin containing three skills: router, Ads and WhatsApp.
- `BUSINESS-TRUTH.md` is the upstream source.
- `META-TRUTH.md` and `META-GROWTH-PLAN.md` are the durable outputs.
- Meta Ads and WhatsApp preflights are read-only.
- Campaign staging defaults to dry-run and can only create paused objects.
- WhatsApp testing defaults to dry-run and is limited to an explicitly owned test recipient.
- Webhook signature verification and full-funnel reporting are included.
- All skill and plugin validators pass; helper scripts compile and dry-run tests pass.
- Installed locally as `meta-growth-system@personal` for testing in a new Codex task.

## Deliberately excluded from Version 1

- Live campaign activation or automatic scaling.
- Editing running campaigns.
- Bulk or real-customer WhatsApp sends.
- WhatsApp template submission.
- Production webhook deployment.
- Unofficial WhatsApp gateways.
- Creative upload and creation through the Marketing API.
- Multi-client Embedded Signup and GrowTricity-owned SaaS authentication.

## Next evidence gate

Run the package against one fictional or sandbox business, then one founder-owned Meta test setup. Record every point where a person must leave Codex or make a Meta-side decision. Use that evidence to choose Version 2 rather than expanding by guesswork.

