# WhatsApp delivery contract

## The one law

An HTTP success and returned WhatsApp message ID mean Meta accepted the send. Human delivery is a later asynchronous fact.

## Message ledger

Store one row per logical outbound operation:

- operation ID
- message purpose
- exact normalized recipient
- template and language, or service-window message type
- accepted message ID
- current status
- accepted, sent, delivered, read and failed timestamps
- Meta error code and reason
- retry generation

Status may advance but must not move backward. Duplicate or late webhook events are normal.

## Safe retry

- Never retry `accepted`, `sent`, `delivered` or `read` blindly.
- Retry an explicit terminal failure only when the failure is retryable and the message is still timely.
- After an uncertain timeout, keep the operation claimed and reconcile provider/ledger evidence. A stable local operation ID does not make Meta deduplicate repeated HTTP sends; do not blindly retry.
- A send guard matches recipient plus message purpose plus operation ID, not an arbitrary time window.

## Recipient truth

One person may have several CRM or booking rows. Resolve the recipient to one exact normalized phone identity before acting. Never send based on loose name matching.

