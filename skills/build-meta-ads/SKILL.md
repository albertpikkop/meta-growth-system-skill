---
name: build-meta-ads
description: Audit, plan, stage and measure Meta advertising through the Marketing API. Use when the user asks to connect an ad account, automate Meta ads, create a campaign, choose an objective or conversion event, diagnose delivery or funnel performance, compare creatives, or create reporting. Default to read-only inspection and dry runs. New campaign objects are paused first, and live spend or changes to running objects require separate explicit approval.
---

# Build Meta Ads

Build from business outcomes backward. Do not begin with campaign settings.

## Entry checks

1. Read `BUSINESS-TRUTH.md` and `META-TRUTH.md` when present.
2. Confirm the business, ad account, currency, timezone, destination, customer value and person responsible for leads.
3. Confirm the deepest outcome the business records reliably. Use that as the scoreboard. Choose an earlier optimization event only when the deeper event lacks sufficient clean volume.
4. Run `scripts/meta_preflight.py` before planning a write.
5. Record missing permissions or assets as blockers. Do not invent IDs or silently select the first account returned by an API.

## Design the campaign

Read [references/campaign-contract.md](references/campaign-contract.md). Produce one configuration based on [assets/META-CAMPAIGN-CONFIG.example.json](assets/META-CAMPAIGN-CONFIG.example.json).

Keep these concepts separate:

- Campaign: objective and container.
- Ad set: budget, optimization, audience, schedule and placements.
- Ad: creative and destination.
- Business outcome: verified CRM or payment result used to judge the system.

One advertising use case should have one primary action and one primary optimization event. Do not add several unproven creatives to a proven ad set merely because Meta permits it. Testing needs a written control, challenger, budget, horizon and decision rule.

## Stage safely

The staging script defaults to dry-run:

```bash
python3 scripts/build_paused_campaign.py --config META-CAMPAIGN-CONFIG.json --out META-PAUSED-BUILD-RECEIPT.json
```

Creating paused objects is still an external write. Ask for approval naming the account and proposed budget before using `--apply`. The script then requires the literal confirmation `I_APPROVE_PAUSED_META_BUILD`.

Version 1 may create:

- one paused campaign;
- one paused ad set;
- and optionally one paused ad that uses an existing creative ID.

It does not upload new creative, activate delivery, alter running objects, increase budget, or delete anything.

## Measure the real funnel

Read [references/measurement-contract.md](references/measurement-contract.md). Run `scripts/funnel_report.py` on a normalized funnel JSON file.

Always distinguish:

- account status from actual spend and impressions;
- clicks from landing-page arrivals;
- leads from qualified leads or bookings;
- bookings from attendance;
- attributed conversions from verified CRM outcomes;
- missing attribution from organic traffic.

Use the account timezone for Meta-day comparisons. Compare equal windows. Allow for the business's real sales delay. A newest-day or incomplete-day read cannot support a structural verdict.

## Diagnose before changing

Check in order:

1. Billing and account restrictions.
2. Campaign, ad-set and ad effective status.
3. Actual spend and impressions.
4. Link click rate and cost.
5. Landing-page arrival rate and speed.
6. Form or CRM persistence.
7. Lead response and contact capacity.
8. Qualified, attended and paid outcomes.

Only recommend a creative, audience, budget or optimization change when the evidence isolates that stage.

## Completion receipt

Report:

- account and asset identities, without secrets;
- read-only checks performed;
- exact planned or created object IDs;
- configured budget and currency;
- paused or live state;
- funnel result and unknowns;
- and the smallest next approval required.
