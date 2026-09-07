# Get the agent access to Meta, then prove it

Use for “how do I get the API?”, missing-token setup, or a student asking what is manual.
Scope: a single business using its own Meta assets. For onboarding many clients, explain that
Embedded Signup/appropriate app review is a separate integration; do not reuse one student's
token across businesses. Verify current official Meta docs and actual account UI before
prescribing a screen label or declaring an account eligible.

## There is no API to download

Meta hosts Graph API. The agent's backend calls a versioned HTTPS endpoint using an access
token. A valid token alone is insufficient: the app must have the needed permissions AND the
principal behind the token must have access to the correct business/WABA/phone assets.
An installed skill is instructions, not a Meta login or automatic account access.

## Owner, agent and Meta responsibilities

| Owner does or authorizes | Agent can prepare or perform with scoped access | Meta decides |
|---|---|---|
| Sign in; complete MFA, terms and ownership checks | Check existing assets read-only; explain each missing setup step | Account/access eligibility |
| Create/select own business portfolio and app; allow appropriate asset access | Map Business/App/WABA/Phone Number IDs; inspect profile and templates | Assigned IDs and required review |
| Receive phone OTP; approve registration/migration/coexistence choice | Execute supported registration steps after authorization | Number/display-name status |
| Create/authorize credential; accept actual billing terms | Store through approved secret path; validate permissions and target assets | Token/access restrictions, billing eligibility |
| Approve exact template copy, language/category | Submit/list templates via Graph API when authorized | Template approval/category |
| Authorize hosted callback and customer journey | Deploy handler, configure supported subscriptions, send eligible approved tests/jobs | Platform acceptance and delivery events |

Do not promise every setup step can be performed by Graph API, nor send the student through
manual dashboards for operations a supported connector/API can safely do. Prefer API/CLI for
repeatable work; the human owns account login/verification/consent. Do not request credentials
already available through an authorized connector or secret store.

## One-business bootstrap

1. Sign into Meta Developers and the student's Meta Business Suite. Create/select the business
   portfolio and developer app, associate them appropriately, and configure WhatsApp. Reuse
   existing correct assets instead of creating duplicates. Do not mandate a legacy app-type
   label; follow the current WhatsApp setup offered by Meta.
2. For a first sandbox test, use the app's WhatsApp API Setup/Getting Started test number,
   temporary token and an explicitly authorized test recipient added/verified as required.
   Record this as TEST, not the production sending number. A demo token can expire.
3. For ongoing access to the business's own assets, use the business settings System users
   area (usually Users -> System users): create/select a system user, assign the relevant app
   and WABA with the minimum access needed, then generate a token for that app. Check both
   the generated token's permissions and the system user's actual asset assignments.
4. Request `whatsapp_business_messaging` for message operations and
   `whatsapp_business_management` for WABA/template management. `business_management` is for
   applicable portfolio operations; do not add `ads_management` for a WhatsApp-only build.
   If a permission is unavailable, inspect app/access requirements rather than guessing or
   using another business's token. No “full control everywhere” default.
5. Record the expiry/revocation policy and credential owner. System-user tokens may offer
   longer-lived/non-expiring options depending on setup; “never expires” does not mean cannot
   be revoked. Verify the chosen token rather than promising permanence.
6. For the real sending number, the owner verifies control and authorizes registration. Inspect
   whether it is already used in WhatsApp/another integration; use only a supported migration
   or coexistence path. Never casually delete its existing account. Complete applicable phone
   registration/two-step verification, display-name, app access/review and payment requirements.
7. Store credentials using the approved environment/secret manager. For development use an
   ignored local environment file if needed; for runtime use Supabase Edge Function secrets.
   Do not paste token values into chat, screenshots, source, Markdown or a public form.
8. Run read-only checks. Only after identity/permissions are right, prepare a concrete hosted
   webhook and owned-recipient test. A successful asset read alone is not send readiness.

Screen names may move. [Meta's official collection](https://www.postman.com/meta/whatsapp-business-platform/documentation/wlk6lh4/whatsapp-cloud-api)
links the current access-token setup; use its current official links when guiding a student.

## Secret and identifier handoff

Existing helpers use these environment variable names:

| Variable | What goes there |
|---|---|
| META_ACCESS_TOKEN | Authorized Graph bearer credential; secret |
| META_GRAPH_VERSION | Current supported version explicitly verified at build time |
| META_WABA_ID | Correct WhatsApp Business Account ID |
| META_PHONE_NUMBER_ID | Correct registered sending-number ID |
| META_APP_SECRET | App secret for POST HMAC; secret |
| META_WEBHOOK_VERIFY_TOKEN | Random value chosen by you for GET challenge; secret |

Record Business ID and App ID in META-TRUTH.md, alongside asset mapping and secret references,
not values. Keep IDs distinct from credentials. RESEND_API_KEY is a separate email secret.
Supabase/project-host administration needs its own authorized connector/CLI/access token;
a Meta token cannot deploy functions or set Resend DNS. The website gets only permitted public
configuration. Backend privileged keys stay in secret storage.

## Read-only connection proof

Resolve the installed helper path relative to this SKILL.md, not the student's working folder.
Run its `--help`, then `whatsapp_preflight.py` with secrets from the environment. It checks
phone details and templates. Its legacy ready_for_controlled_test flag only means a display
number was returned; it does NOT verify every item below. Do not use it as the release gate.

Verify additionally through supported Graph reads, inspecting current endpoint documentation:

- token belongs to the intended app/principal, is valid and has needed permissions;
- WABA belongs to the intended business and includes the chosen Phone Number ID;
- current number registration/display-name/account status permits the intended test;
- exact template name/language/category is eligible, consent and recipient are correct;
- app/WABA and messages-field subscription are correct, callback is reachable and signed
  events persist, required billing/access is complete for this test.

Use the token in the Authorization header. Do not print debug-token responses or query URLs
containing secrets. A missing-asset error can mean wrong ID or missing asset assignment;
check both before regenerating credentials. Report permission gap, asset gap, expired token
or review requirement distinctly, with one next owner action. Never claim app-review success
from token generation.

## What Graph API can then do

Within the token's access and the user's authorization, supported calls can list account/phone
assets and templates, submit approved-by-owner template copy, subscribe an app to a WABA,
send approved test/customer messages and query available status/configuration. Template
submission is not Meta approval. Incoming messages and delivery/read/failure updates arrive
through the separately hosted webhook, not by asking the coding chat to stay running.

After code is deployed, the hosted backend uses its stored credentials. The coding agent does
not have to run forever. Keep an operator-visible error queue and token-expiry/revocation
recovery; suppress rather than lose/duplicate sends while access is broken.
