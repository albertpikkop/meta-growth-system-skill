# Approval matrix

| Action | Default | Required unlock |
|---|---|---|
| Read account, assets, permissions and insights | Allowed | None |
| Produce use case, funnel, copy, creative brief or dry run | Allowed | None |
| Create a new campaign, ad set or ad in paused state | Blocked | Explicit approval naming the account and expected budget |
| Activate delivery | Blocked | Separate explicit approval naming campaign and daily or lifetime budget |
| Change budget, targeting, optimization, placement or creative on a running object | Blocked | Separate explicit approval describing the change and expected cost |
| Pause a live object | Blocked | Explicit approval, except a documented emergency budget kill switch already authorized by the owner |
| Delete an object | Blocked | Explicit approval after exact-ID read-back; prefer pause |
| Submit a WhatsApp template for review | Blocked | Explicit approval of the exact copy, language and category |
| Send to one owned test number | Blocked | Explicit test-only approval and exact recipient confirmation |
| Send to a lead or customer | Blocked | Explicit approval for the exact audience, purpose and copy |
| Replace a production webhook | Blocked | Explicit deployment approval and rollback plan |
| Send conversion events | Blocked for live data | Explicit approval plus event-source and identity verification |

Every write produces a receipt with account or asset ID, operation, timestamp, inputs excluding secrets, returned object ID, and verification result.

