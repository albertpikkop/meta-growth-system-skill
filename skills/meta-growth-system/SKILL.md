---
name: meta-growth-system
description: Build or audit an end-to-end Meta growth system that connects a business plan, Meta Ads, a landing page or CRM, WhatsApp Cloud API, and verified business outcomes. Use when the user asks to get Meta working end to end, automate advertising and lead response, connect ads to WhatsApp, diagnose where a Meta funnel is leaking, or decide what should be built before spending money. Also use for student CRM confirmations, qualification, nurture and booking without ads. Route focused ad work to build-meta-ads and focused WhatsApp work to connect-meta-whatsapp.
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
- For student CRM sales automation, use `connect-meta-whatsapp` and its student-sales-automation reference. Reuse `build-first-crm` when available for the first enquiry/login/Resend loop; otherwise implement that foundation with the available supported tools. Do not require installation to prepare the local plan.
- Use both Meta skills when advertising AND WhatsApp are requested. Keep one shared outcome name and one customer identity key across the CRM, Meta events and WhatsApp ledger.

## Workflow

1. **Business truth:** identify the offer, audience, value and operational capacity.
2. **Capability preflight:** discover only the assets needed by the chosen mode through read-only calls. WhatsApp-only work needs no ad account, Pixel or campaign. Prepare local code with synthetic data while account gaps are resolved.
3. **Funnel contract:** name every stage from the actual lead source to verified outcome and identify which system owns each stage.
4. **Plan:** create `META-GROWTH-PLAN.md` using [assets/META-GROWTH-PLAN-TEMPLATE.md](assets/META-GROWTH-PLAN-TEMPLATE.md).
5. **Ads, when requested:** prepare creative, tracking and campaign configuration. Stage new objects paused only after explicit approval.
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

The chosen mode is complete only when the user has:

- a redacted `META-TRUTH.md`;
- a named business outcome and funnel map;
- a read-only preflight for each API actually used;
- a reviewed campaign plan or paused campaign receipt when advertising is in scope;
- a verified WhatsApp test path with delivery status, not only API acceptance, when WhatsApp is in scope;
- and a clear list of the remaining human authorization steps.

For a requested CRM automation build, additionally prove the seven-stage branch, permissions,
durable jobs, real booking, human handover and delivery state from the implementation guide.
Do not stop at a plan or test send and call the application complete.
