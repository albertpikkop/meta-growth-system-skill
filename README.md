# Meta Growth System Skill

Build a measurable Meta Ads and WhatsApp Cloud API growth system from a business truth file.

This package contains three Codex and Claude-compatible skills:

- `meta-growth-system`: routes an end-to-end request and keeps one shared plan.
- `build-meta-ads`: audits Meta advertising assets, designs the funnel, stages paused campaigns, and reports performance.
- `connect-meta-whatsapp`: audits WhatsApp Cloud API, verifies webhooks and templates, and performs a controlled test send.

Version 1 is deliberately fail-closed. It can do read-only discovery without approval. It can prepare plans and dry runs. It never activates spend, changes a live campaign, or contacts a real customer without separate explicit approval.

## What it needs

1. A `BUSINESS-TRUTH.md` file, normally produced by the `noguess` skill.
2. A Meta business portfolio with the relevant assets.
3. API credentials supplied through environment variables, never pasted into a repository.
4. A clearly named business outcome such as qualified lead, booked appointment, attended appointment, or purchase.

Read [SETUP.md](SETUP.md) before the first live API check.

## Honest limit

The skill can complete most repeatable technical work. The account owner must still sign in, grant permissions, complete any verification Meta requires, connect payment details, and approve spend and customer communication.

