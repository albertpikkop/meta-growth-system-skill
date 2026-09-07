# Build the student's lead-to-sale workflow

Use this reference when asked to build or extend a student's CRM with confirmations, a human
call, qualification, nurture and booking. It is an implementation guide, not a prebuilt CRM
or proof that an account is connected. Keep the student in one conversation and use their
existing project. This workflow can start from organic enquiries; an ad account is optional.

## Start from what already works

Read BUSINESS-TRUTH.md and its What exists now section, then META-TRUTH.md if present. Inspect
the actual form, schema, operator login and email hook. Ask only missing business choices:
qualification criteria, permission wording, follow-up timing, owner, booking availability and
what counts as conversion. Use existing facts and approvals. A plan is not permission to send.

If build-first-crm is installed, it owns the basic enquiry/login/Resend loop. Its released
version and a student's source can differ: inspect rather than assume helper commands or
schema columns. If unavailable, implement or repair that minimal loop here using the
student's supported tools. Do not install another skill silently or force a second interview.
Do not substitute a generic enquiry form for a requested booking system.

Keep BUSINESS-TRUTH.md as the business facts; put this implementation's stages and receipts in
META-GROWTH-PLAN.md, asset identity in META-TRUTH.md. No duplicate business truth, passwords,
real message bodies or customer lists in these files.

## Seven stages and the branch

| Stage | Build | Evidence |
|---|---|---|
| 1. New lead | Form, WhatsApp or operator intake with source and identity | One persisted enquiry, including retry handling |
| 2. Save CRM | Contact, owner and append-only conversation history | Signed-in operator sees the same lead |
| 3. First response | WhatsApp enquiry acknowledgement, Resend email, human call task | Each channel has its own receipt; person completes call |
| 4. Qualify + permissions | Need/readiness questions; update preferences and separate optional marketing choice | Answers, consent source/time/text version and decision stored |
| 5. Nurture when not ready | Scheduled eligible marketing; utility only for a specific request/transaction | Due job rechecks eligibility and suppression before send |
| 6. Book when ready | Real availability, reservation, calendar event/link, confirmation | One booking and a verified invite, not just a form row |
| 7. Human sales | Handover with history, pause bot sequence, record sales outcome | Operator action and actual won/lost/pending evidence |

READY at 4 goes directly to 6; NOT READY with marketing permission goes to 5. A reply from 5
returns to qualification; READY then goes to 6. No marketing permission means no marketing
queue. Opt-out stops the relevant communication. Booking, conversion or human takeover
suppresses obsolete nurture; relevant appointment utility reminders may remain eligible.
A human may take over earlier. Call task created is not call completed or automated calling.
Do not silently add an AI caller or promise a sale.

## Permission and template decisions

For a form lead, obtain the appropriate WhatsApp opt-in BEFORE initiating step 3. A form
submission does not open the WhatsApp service window. Step 4 records/refines preferences; it
cannot retroactively authorize the first message. An inbound WhatsApp enquiry allows an
eligible service reply, not blanket marketing consent. Missing phone/email permission or
address suppresses that channel while preserving the enquiry and human task.

Verify current official rules before implementation. Within 24 hours of the customer's last
WhatsApp message, service replies can be eligible; outside it, use an approved template.
Keep the exact template language, category and variables. Generic “still interested?” nurture
is marketing, not utility. Utility relates to a specific requested service or transaction,
such as a genuine booking update. Do not turn every enquiry confirmation into utility by
label alone. Template approval is not recipient consent.

Store separate channel/purpose preferences, opt-in time/source/text version and revocation.
Recheck them immediately before dispatch. Do not reset opt-out when a duplicate form arrives.

## Small deployable architecture

- Coding agent (for example Codex): writes and tests code. The deployed app runs afterwards.
- Student-owned Supabase: Postgres CRM, Auth and operator access with RLS. A database is not
  an operator UI; build the inbox, call-task action and qualification/booking controls.
- Supabase Edge Functions: signed Meta receiver and server-only send/booking handlers.
- Supabase Cron plus durable jobs/outbox: timed follow-ups, claimed atomically by a worker.
  No function sleeping overnight and no laptop-dependent schedule.
- Meta WhatsApp Cloud API: WhatsApp transport and inbound/status events.
- Resend: email using the student's verified sending domain and server-side API key.
- Existing web host: form and CRM screen. Static hosting alone cannot execute the webhook.
- Booking/calendar adapter: custom booking page or an existing scheduler with a reliable
  server-side booking event. Online meeting links are optional when meetings are in person.
- Optional runtime model API for AI-generated replies. Fixed rules do not require it.

Reuse the existing Resend sender and hook. Do not create a second confirmation path for the
same enquiry. If replacing a hook, map its outstanding jobs and verify only one active owner
before cutover. Never reuse a database-insert webhook secret as Meta's signature credential.

## State and storage contract

Map these entities to existing tables, adding migration-backed extensions only as needed:

- lead/contact and enquiries: stable lead ID, normalized channel identity, owner and source;
- consent events: channel, purpose, granted/revoked, time/source and wording version;
- inbound messages/status events: immutable provider identities and provider timestamps;
- outbound intents/jobs: unique logical operation key, purpose/template, due time, state,
  attempt/lease and suppression reason; provider attempts store WAMID or email ID separately;
- call tasks/qualification: owner, actual call outcome, answers and readiness;
- appointments: timezone, availability/resource, booking status and unique reservation;
- sales outcomes/operator actions: auditable handover, won/lost/pending, verified conversion.

Keep engagement, booking, sales and delivery as separate states. Customer initiated window
uses the last CUSTOMER message, not the last business response. Store UTC, display the
business timezone, and do not guess hours or nurture cadence.

Use database uniqueness and atomic claims, not browser flags. Duplicate inbound messages,
form submissions or scheduler callbacks must not create duplicate acknowledgements, tasks
or bookings. Distinguish a contact from a new legitimate enquiry by the same person.

A provider-accepted send remains claimed while awaiting status. Timeout after a send means
outcome unknown: reconcile, do not blindly resend even with the same operation key. Signed
status processing must not regress read to sent when callbacks arrive out of order.

Enforce booking capacity atomically. If the slot is taken, offer another. If calendar creation
fails after reservation, keep a recoverable pending state; no false confirmation. Booking
completion suppresses nurture even when an external scheduling webhook is delivered twice.
Server-side ownership checks guard actions; never trust a browser's lead ID by itself.

## Build in demonstrable increments

1. Inspect/preserve the working enquiry, login and email loop; map any extension migrations.
2. Build webhook + consent persistence + one acknowledgement + human call task. Verify it
   locally with synthetic events, then on an authorized isolated test setup.
3. Add qualification and the two readiness paths. Prove READY skips nurture.
4. Add booking with capacity checks and calendar confirmation, then durable nurture jobs.
5. Add human handover, suppression, outcome recording and operator-visible delivery errors.

Read [supabase-webhook-setup.md](supabase-webhook-setup.md) for the endpoint and credentials.
Show a runnable local build and test evidence before requesting remaining live authorization.
Preserve existing authorization: do not ask again for the same named action. Account login,
new costs, template submission, deployment and real-customer journey activation require the
applicable scope to be authorized; prepare everything independently possible first.

A classroom/test-recipient completion is not live-customer readiness. Live release needs the
actual project/account, audience, exact content/templates, schedule/caps, owner and kill switch
reviewed; never activate the whole list because one test arrived.

## Acceptance scenarios

Run against the built app and data/queue state, not just generated prose:

1. Form without marketing permission saves and creates a human task but never queues nurture;
   without WhatsApp opt-in it also sends no business-initiated WhatsApp acknowledgement.
2. READY lead reserves a real slot and queues no nurture; duplicate booking callback creates
   no second booking, invitation or confirmation.
3. NOT READY opted-in lead queues the chosen marketing message; unrelated utility is rejected.
4. Opt-out or human takeover between enqueue and dispatch suppresses the pending nurture job.
5. Customer window expires before dispatch: free text is rejected; only an eligible approved
   template can proceed. No invented fallback to another channel.
6. Invalid webhook signature produces no rows; valid duplicates cause no repeated effects;
   database/queue failure before persistence does not get a successful acknowledgement.
7. Two workers claim a due message: one send. Timeout/accepted-without-status produces no
   blind retry and no false delivered label. Delayed sent cannot overwrite read.
8. Two leads request the last slot: one reservation. Calendar failure does not produce a
   confirmed meeting. Human call completion is separate from task creation.
9. Existing email hook plus new journey produces one lead confirmation. Unauthorized operator
   access fails; browser bundle and logs expose no server secret.

Report build, local tests, hosted test and live activation separately as passed/pending/failed.
Save commands and redacted receipts in META-GROWTH-PLAN.md. Unrun tests remain pending.

## Official sources

Checked for the teaching design on 7 September 2026; recheck rules and SDK details when building.

- [Meta Cloud API assets and permissions](https://www.postman.com/meta/whatsapp-business-platform/documentation/wlk6lh4/whatsapp-cloud-api)
- [WhatsApp policy](https://business.whatsapp.com/policy)
- [Utility examples](https://whatsappbusiness.com/products/conversation-categories/utility/)
- [Supabase functions](https://supabase.com/docs/guides/functions/quickstart)
- [Supabase Cron](https://supabase.com/docs/guides/cron)
- [Resend domain setup](https://resend.com/docs/dashboard/domains/introduction)
