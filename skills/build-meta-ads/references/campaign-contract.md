# Campaign contract

## Required business inputs

- One offer and one customer action.
- Geography and any legally required restrictions.
- Customer value or acceptable acquisition cost.
- Daily lead-handling capacity.
- Destination that has been tested on a phone.
- A stable CRM identity and a verified outcome.

## Required account truth

- Exact ad account ID, name, currency and timezone.
- Page and Instagram identity used by the ad.
- Dataset or Pixel and the event selected for optimization.
- Permissions needed by the operation.
- Billing and restriction status.

## Safe first structure

- One campaign for one objective.
- One ad set for one audience and optimization event.
- One reviewed creative for the first controlled run.
- New objects start paused.
- Tracking names are deterministic and include a unique use-case slug.
- UTM content identifies the creative exactly. Avoid overlapping substring names.

## Testing contract

Before starting a test, write:

- control;
- challenger;
- only variable intentionally changed;
- budget per arm;
- expected sample rate;
- fixed duration or sample threshold;
- kill condition;
- promotion condition;
- final business metric;
- and attribution delay.

Do not call a winner from an incomplete day, a different audience, a different optimization event, or a metric that is not connected to the business result.

