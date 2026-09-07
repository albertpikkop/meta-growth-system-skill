# Meta Growth System Skill

Build a measurable Meta Ads and WhatsApp Cloud API growth system from a business truth file.

Repository: <https://github.com/albertpikkop/meta-growth-system-skill>

This package contains three Codex and Claude-compatible skills:

- `meta-growth-system`: routes an end-to-end request and keeps one shared plan.
- `build-meta-ads`: audits Meta advertising assets, designs the funnel, stages paused campaigns, and reports performance.
- `connect-meta-whatsapp`: audits WhatsApp Cloud API, verifies webhooks/templates, and guides the student CRM sales-automation build from enquiry to human handover.

The API helpers are deliberately fail-closed. It can do read-only discovery without approval. It can prepare plans and dry runs. It never activates spend, changes a live campaign, or contacts a real customer without separate explicit approval.

## What it needs

1. A `BUSINESS-TRUTH.md` file, normally produced by the `noguess` skill.
2. A Meta business portfolio with the relevant assets for live integration; local synthetic builds can start before connection. No ad account is needed for WhatsApp-only work.
3. API credentials supplied through environment variables, never pasted into a repository.
4. A clearly named business outcome such as qualified lead, booked appointment, attended appointment, or purchase.

Read [SETUP.md](SETUP.md) before the first live API check.

## Honest limit

The skill can complete most repeatable technical work. The account owner must still sign in, grant permissions, complete any verification Meta requires, connect payment details, and approve spend and customer communication.

## Student CRM automation

Keep the [first CRM](https://github.com/albertpikkop/first-crm-skill) and its existing Supabase
project/login/Resend sender. Ask:

> Use meta-growth-system to extend the CRM in this folder with WhatsApp confirmation, email,
> a human call task, qualification and permissions, nurture only when not ready, real booking
> when ready, and human sales handover. Read BUSINESS-TRUTH.md first. Build and test locally
> before asking for remaining account or live-send authorization.

The [implementation guide](skills/connect-meta-whatsapp/references/student-sales-automation.md)
covers the branch, consent, durable jobs, booking and scenario tests. The
[callback guide](skills/connect-meta-whatsapp/references/supabase-webhook-setup.md) explains
Meta IDs and the Supabase HTTPS endpoint. Start with the
[API access guide](skills/connect-meta-whatsapp/references/meta-api-access.md) for owner login,
system-user asset assignment, scopes and token storage. The coding agent builds the app; hosted functions
and scheduled jobs run it. No separate dedicated server, automation builder or runtime AI
model is inherently needed for fixed rules.

These additions are instructions for the agent to build and verify the system. This package
is not a prebuilt CRM or a one-command automation installer. Existing helpers remain preflight,
paused-ad staging, signature checking and an owned-recipient test. Installing it neither
deploys nor activates customer communication. See [EXERCISE.md](EXERCISE.md).
