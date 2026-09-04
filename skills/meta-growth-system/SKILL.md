---
name: meta-growth-system
description: Build or audit an end-to-end Meta growth system that connects a business plan, Meta Ads, a landing page or CRM, WhatsApp Cloud API, and verified business outcomes. Use when the user asks to get Meta working end to end, automate advertising and lead response, connect ads to WhatsApp, diagnose where a Meta funnel is leaking, or decide what should be built before spending money. Route focused ad work to build-meta-ads and focused WhatsApp work to connect-meta-whatsapp.
---

# Meta Growth System

Treat this as one growth system with two different Meta APIs. Do not pretend one token, permission set, success response, or metric covers both.

## Start with truth

1. Look for `BUSINESS-TRUTH.md` in the project.
2. If it exists, read it and do not ask again for facts it already contains.
3. If it does not exist, use the `noguess` skill first. Do not invent the offer, audience, location, price, capacity, conversion event, customer value, or lead-handling capacity.
4. Create or update `META-TRUTH.md` from [assets/META-TRUTH-TEMPLATE.md](assets/META-TRUTH-TEMPLATE.md). Never put tokens, app secrets, payment details, or personal customer data in it.

## Choose one use case

Name one concrete loop before touching an account. Examples:

- Local service: ad to landing page to WhatsApp confirmation to attended appointment to payment.
- B2B service: ad to qualified WhatsApp enquiry to sales call to won deal.
- Product: ad to product page to purchase.
- Event or course: ad to registration to attendance to enrolment.

The deepest verified business outcome is the scoreboard. A lead is not automatically a sale. A booking is not automatically attendance. Meta acceptance is not WhatsApp delivery.

## Route the work

- Use `build-meta-ads` for account discovery, campaign structure, creative briefs, paused staging, delivery checks and performance analysis.
- Use `connect-meta-whatsapp` for WABA and phone-number checks, templates, webhooks, consent, test messages and delivery truth.
- Use both when the request is end to end. Keep one shared outcome name and one customer identity key across the CRM, Meta events and WhatsApp ledger.

## Version 1 workflow

1. **Business truth:** identify the offer, audience, value and operational capacity.
2. **Capability preflight:** discover the ad account, Page, dataset or Pixel, WABA, phone number, permissions, currency and timezone through read-only API calls.
3. **Funnel contract:** name every stage from impression to verified outcome and identify which system owns each stage.
4. **Plan:** create `META-GROWTH-PLAN.md` using [assets/META-GROWTH-PLAN-TEMPLATE.md](assets/META-GROWTH-PLAN-TEMPLATE.md).
5. **Ads:** prepare creative, tracking and campaign configuration. Stage new objects paused only after explicit approval.
6. **WhatsApp:** verify the official Cloud API path, webhook signature, approved template and test recipient. Test only after explicit approval.
7. **Measurement:** verify the complete loop and report unknown attribution as unknown. Never silently label missing attribution as organic.
8. **Handoff:** state what is ready, what remains paused, what was verified, and the exact owner action needed next.

## Approval boundary

Read [references/approval-matrix.md](references/approval-matrix.md) before any external action.

Never infer approval for activation, spend, budget changes, live-campaign edits, template submission, production webhook replacement, customer messages, deletion or pausing. Approval for one action does not authorize the next one.

## Failure behaviour

- Stop when account identity, currency, timezone, Page, phone number or outcome is ambiguous.
- Do not switch to browser automation, an unofficial WhatsApp gateway, or another customer's account silently.
- Do not retry an uncertain write with a new idempotency key.
- Preserve partial receipts when an API sequence fails.
- Diagnose the funnel stage before blaming the creative or increasing budget.

## Completion standard

Version 1 is complete only when the user has:

- a redacted `META-TRUTH.md`;
- a named business outcome and funnel map;
- a read-only preflight for both APIs;
- a reviewed campaign plan or paused campaign receipt;
- a verified WhatsApp test path with delivery status, not only API acceptance;
- and a clear list of the remaining human authorization steps.
