# GHL Estimates/Invoices Verification Report — Property Renovators Home Services

**Date:** August 2, 2026 (all times UTC)
**Location ID:** `w6brLF0sqjGJVPR5N4Pa`
**Verified by:** Claude Code, working directly against the live GHL API (REI Unlock connector) and Jay's inbox (jay@thejaymora.com). Every verdict below is backed by a first-hand API response or email pulled today — nothing is carried over from Olu's claims or the prior chat session.

**Environment limitation (affects items 1–3, 7):** this session's network policy blocks direct HTTPS to `link.fastpaydirect.com` and `email.mail.propertyrenovatorshomeservices.com` (proxy returns 403 CONNECT). I could not load estimate pages in a browser or run a TLS handshake. Where page rendering mattered, I relied on server-side evidence (GHL's own `lastVisitedAt` view tracking, acceptance notification emails) and I list the exact remaining clicks for Jay at the end — about 3 minutes of work.

---

## Scorecard

| # | Item | Verdict |
|---|------|---------|
| 1 | Estimate links resolve (was NOT_FOUND) | **CONFIRMED FIXED** (server-side evidence; 2 confirmation clicks left for Jay) |
| 2 | 33% deposit / exact 1/3 math | **PARTIALLY CONFIRMED** — decimal precision works (33.3333 stored); invoice generation needs one Accept click |
| 3 | Deposit-optional flow | **CONFIGURED CORRECTLY** — acceptance needs one click |
| 4 | Branding / email templates | **SPLIT**: sending domain FIXED; blank logo was OUR bug (now solved); notification templates still blank/unchanged |
| 5 | Variants / multi-select line items | **CONFIRMED NOT DONE** |
| 6 | Deposit-paid → Opportunity automation | **CONFIRMED NOT DONE** (still draft, unpublished) |
| 7 | SSL cert on email tracking domain | **UNABLE TO TEST** here — and it matters more than we thought (see below) |
| 8 | Estimate void/cancel capability | **RESOLVED** — a working DELETE endpoint exists; full status enum mapped |
| — | Jay's real contact (data damage) | **REPAIRED** — `source` restored to "Send Us Your Photos" |
| — | Test data cleanup | **DONE** — 11 estimates deleted; opportunities were already gone |

---

## 1. Estimate links resolve — CONFIRMED FIXED

The NOT_FOUND bug is gone. Evidence, all from today:

- **Estimate #30** ("VERIFY TEST 2", $2, no deposit): GHL recorded `lastVisitedAt: 2026-08-02T21:11:18.659Z` — the estimate page loaded successfully ~30 seconds after sending. GHL only stamps this when the page actually loads and reports the view.
- **Estimate #24** ($900, Olu's test): the notification email in Jay's inbox at **20:26 UTC** — *"API Flow Test has accepted your estimate 24 for $900.00"* — proves the page not only rendered but the **Accept button worked end-to-end** at least once post-fix. (#24 was deleted afterward, presumably by Olu.)
- **Olu's sample #28** ($900 bathroom remodel): `lastVisitedAt: 2026-08-02T21:03:24Z`.
- **Fresh estimate created from scratch (#32)**: I created and sent a brand-new estimate via `POST /invoices/estimate` + send at 21:28–21:29 UTC. Status went to `sent`, and the email arrived in Jay's inbox at 21:29:04 — the full pipeline works for newly created estimates, not just Olu's samples.

**The products-catalog variable is eliminated.** The theory was that pre-existing estimates #4/#5 used real Products (`productId`/`priceId`) while all failing test estimates were ad-hoc. I checked: the list API *does* return `productId`/`priceId` when present (proven on #32 below), and **#4 and #5 contain no product references at all** — they were ad-hoc too. There was never a products-vs-ad-hoc difference. To cover the untested case anyway, **#32 is a true catalog-based estimate** — line item "Window Crank - Replacement (Casement Windows)", `productId: 6a59149492a3d6cc9df817db`, `priceId: 6a591494c5b1cfd2dea339d4` ($240 Flat Rate price). Created, stored, and sent without any issue.

**Remaining clicks for Jay** (I can't load pages from this environment):
- #29: https://link.fastpaydirect.com/l/ZChj2CmUq — *not yet visited by anyone; no `lastVisitedAt` on record*
- #30: https://link.fastpaydirect.com/l/HyN-L6UUS (already confirmed loading via `lastVisitedAt`)
- #32: https://link.fastpaydirect.com/l/9e2tc3QbI
(URLs decoded from the tracking wrappers in the actual emails.)

## 2. Deposit math — decimal precision CONFIRMED at the config layer

Tested on a throwaway draft (#31) with a **realistic $1,720 total**, then deleted:

- `paymentScheduleConfig.schedules[0].value: 33.33` → **accepted and stored exactly** (HTTP 201).
- Updated to `33.3333` → **accepted and stored exactly** (HTTP 200). Estimates carry `configuration.precision: 4`, consistent with 4-decimal support.

The math this enables on $1,720:
| Config | Deposit |
|---|---|
| 33 (flat, what #29 and Olu's samples use) | $567.60 |
| 33.33 | $573.28 |
| **33.3333** | **$573.33 — true 1/3 to the cent** |

**Recommendation: use `33.3333` on every deposit estimate going forward.** This solves the exact discrepancy Jay hit on the Housecall Pro estimate, with no dependency on Olu.

**Not yet confirmed:** that the auto-generated deposit *invoice* computes the amount correctly on acceptance. There is no public API to accept an estimate (acceptance is customer-side on the page), so this needs Jay to click **Accept on #29** ($3, 33% → expected $0.99 deposit invoice). Worth knowing: **no auto-generated invoice has ever appeared in this account** — the invoice list contains only 3 invoices, all manually created. Estimate #24's acceptance at 20:26 left no invoice behind, but #24 was deleted, so that's inconclusive rather than damning. The accept-#29 test is the real check.

## 3. Deposit-optional flow — configured correctly, one click from proven

#30 was created with no `autoInvoice` and no `paymentScheduleConfig`, and sent cleanly; the page loads (see item 1). Whether acceptance requests the full $2 with no deposit split needs Jay's Accept click on #30.

## 4. Branding / email templates — three separate facts

1. **Sending domain: CONFIRMED WORKING.** #29, #30, and #32 all arrived from `info@mail.propertyrenovatorshomeservices.com`. The July 31 tests had fallen back to `jay+thejaymora.com@mail.reiunlock.com`. This part of Olu's fix is real.
2. **The blank logo was our bug, not Olu's — and it's solved.** The #29/#30 emails literally contain `<img alt="Location logo" src="">` — empty. Cause: the API payloads omitted `businessDetails.logoUrl` (Olu's UI-built #28 has it; API-built estimates only get what you pass). I sent #32 **with** `logoUrl` set, and its email renders the logo image. **Rule for every future API-created estimate: always include `businessDetails.logoUrl`.** Jay should eyeball #32's email/page to confirm it's the correct teal/orange Home Services logo, not the wrong Handyman one (I can't render images here; the URL used is the same location photo as Olu's sample: `https://msgsndr-private.storage.googleapis.com/locationPhotos/5abc9048-419a-4e7f-b1ef-49a98914bc38.png`).
3. **Notification templates: CONFIRMED STILL UNTOUCHED.** `GET /invoices/settings` today shows every template (`customerSendEstimate`, `customerSendInvoice`, `customerPaymentSuccess`, `teamEstimateAccepted`, etc.) with `emailTemplate: ""` and `defaultEmailTemplateId: ""`, and the settings document's `updatedAt` is **2026-07-24T15:22:47Z** — before any fix work. GHL's system default template is what's rendering (it looks acceptable, per the emails), but if custom-branded templates were part of the scope, that work has not happened.

## 5. Variants / multi-select — CONFIRMED NOT DONE

`GET /proposals/templates` today: still **exactly one** template, "Property Renovators - Estimate", version 2, `updatedAt: 2026-07-11T20:34:44Z` — untouched since July 11, weeks before any of this. Zero proposal documents have ever been sent (`GET /proposals/document` → total 0). No Variants exist to test, so the check-any-combination vs pick-one-package question remains unanswerable. **This goes on Olu's list.**

## 6. Deposit-paid → Opportunity automation — CONFIRMED NOT DONE

`GET /workflows/` today shows 6 published workflows (Appointment Confirmation, HALT Opt-Out, New Job Request, Post-Job Reviews ×2, Site Visit Needed) — none deposit/booking related — and **two draft, auto-named workflows**:
- "New Workflow : 1785618174944" — draft, created Aug 1
- "New Workflow : 1785705746279" — **draft, created today 21:22 UTC** (minutes after Olu's fix-verification estimates), last edited 21:23

Someone (presumably Olu) is actively building this **but nothing is published**, so no automation will fire when a deposit is paid. The target exists and is ready: pipeline "Property Renovators Jobs" (`hT378d5OfgZIag9MIkMw`) with stage "Approved / Booked" (`d6e1cac0-610c-43f6-9223-a23ba0fb2266`). **This goes on Olu's list.**

## 7. SSL certificate — UNABLE TO TEST here, and higher-stakes than assumed

This environment's egress policy blocks TLS to the domain (proxy 403), so I could not reproduce or clear the `NET::ERR_CERT_COMMON_NAME_INVALID` error. DNS does resolve: `email.mail.propertyrenovatorshomeservices.com` → `34.102.239.211` (Google Cloud, consistent with GHL/LeadConnector infrastructure).

**Why this matters more than "a link in one of Olu's emails":** every link in every estimate email from the new sending domain — including the **View Estimate buttons** on #29/#30/#32 — is wrapped through `https://email.mail.propertyrenovatorshomeservices.com/c/...` for click tracking before redirecting to fastpaydirect. If that cert is still bad, **every customer who clicks an estimate gets a browser security warning first.** Jay can retest in 10 seconds by clicking any View Estimate button; if the warning still appears, this is a must-fix for Olu (SSL provisioning for the email tracking subdomain in GHL's domain settings).

## 8. Estimate void/cancel — RESOLVED, with definitive answers

- **A delete endpoint exists and works**: `DELETE /invoices/estimate/{estimateId}`. I used it 11 times today (my own test draft + the 10-estimate cleanup), each returning 200 with `deleted: true`. Whatever was true in the earlier session, deletion is available now — no more renaming things "SUPERSEDED".
- **Valid `estimateStatus` values** (probed against the API's own enum validation): `draft`, `sent`, `viewed`, `accepted`, `declined`, `invoiced`. Rejected as invalid: `void`, `cancelled`, `expired`. **There is no void status in GHL's model.**
- **Status cannot be set via the API at all**: `PUT /invoices/estimate/{id}` with `estimateStatus: "declined"` returns 200 but **silently ignores the field** (status stayed `draft`). Status only changes through real events (sending, customer viewing/accepting/declining). So: to kill a stale estimate, delete it; to decline one, the customer does it on the page.
- ⚠️ Same footgun class as the contacts API: `PUT /invoices/estimate` **wholesale-replaces** — when I omitted `termsNotes` on an update, it was nulled. Always send the full object.

---

## Data integrity: Jay's real contact — REPAIRED

`GET /contacts/sBNxkJ7k9a2Y1MFhOStp` this session confirmed the damage: `source` still read `"Internal Test - Estimate Flow QA"` (tags were empty; name, HVAC custom fields, and all 9 photos intact).

**Original value recovered with high confidence** (GHL has no public audit-log API, but the attribution trail is unambiguous): the contact's `lastAttributionSource.mediumId` is form `KNda9rEUYExpXdoWSIZd`, whose name is **"Send Us Your Photos"**, and the form-submissions API shows this exact contact submitted that form 13 times between July 26–28 (the HVAC photo uploads). GHL stamps the form name as contact source. I set `source` back to `"Send Us Your Photos"` at 21:31 UTC via a single-field update (nothing else touched — response verified). If Jay remembers it being something else, it's a one-line change.

Unknown and unrecoverable: whether the contact had **tags** before the overwrite (it has none now). Jay should glance at it once.

## Test data cleanup — DONE

- **Deleted today (11 estimates):** #8, #9, #10, #11, #12, #13, #14, #15, #16, #17 (the July 31 test/SUPERSEDED set) plus my own draft #31. Final list verified — only real records and the three live VERIFY estimates remain.
- **Test opportunities:** already gone before I started (spot-checked two IDs from the estimates' metadata → 404 OPPORTUNITY_NOT_FOUND).
- **Kept intentionally:** #29, #30, #32 (needed for Jay's Accept clicks — delete after), #4/#5 (Diane's SUPERSEDED drafts, pre-existing, not in the cleanup mandate), Olu's #27/#28 samples.
- **Two leftovers to decide on:**
  - Invoice **INV-000002** "TEST - Invoice Object Type Check" ($3, sent, unpaid) — ⚠️ it has **overdue-reminder emails scheduled for Aug 4, Aug 7, and Aug 15** that will fire to jay@thejaymora.com unless it's deleted/voided.
  - Invoice **INV-000005** "Deposit Invoice - Diane Christen" ($573, draft, never sent) — the manually-built deposit draft from July 31; keep if the Diane job is proceeding, else delete.

---

## What Jay does next (~3 minutes)

1. Click **#29** (https://link.fastpaydirect.com/l/ZChj2CmUq) — confirm it renders, check the logo/branding, then **Accept** it → then check whether a **$0.99 deposit invoice** auto-generates and arrives (this proves items 2 and the auto-invoice mechanism in one shot).
2. Click **#30** (https://link.fastpaydirect.com/l/HyN-L6UUS) → **Accept** → confirm it asks for the **full $2.00**, no deposit split (proves item 3).
3. Click **#32** (https://link.fastpaydirect.com/l/9e2tc3QbI) — confirm the **logo is the correct teal/orange one** and the catalog line item displays (closes out item 4's visual check and item 1's product-based variant).
4. During any of those clicks: if a **certificate warning** appears before the page loads, item 7 is still broken — screenshot it for Olu.
5. Glance at your own contact record — `source` is restored to "Send Us Your Photos"; re-add any tags you remember it having.
6. Delete #29/#30/#32 and invoice INV-000002 when done (or ask me to — it's one API call each now that delete works).

## The message to send Olu (once, complete)

**Still outstanding — please finish:**
1. **Variants on the estimate template** — the only proposal template hasn't been edited since July 11; no variants exist. Also answer definitively: can a client check any combination of line items, or only pick one package?
2. **Deposit-paid → "Approved / Booked" workflow** — both workflows are still unpublished drafts with auto-generated names. Please finish, name, and **publish** it (trigger: deposit invoice paid → move Opportunity in "Property Renovators Jobs" to "Approved / Booked"), and tell us so we can run a live test.
3. **SSL on `email.mail.propertyrenovatorshomeservices.com`** — [pending Jay's click-test] this domain wraps every link in every estimate email, so a bad cert puts a browser warning in front of every customer. Please confirm SSL is provisioned.
4. *(Optional, if custom branding was in scope)* the invoice/estimate **notification email templates** are all still blank (system default), unchanged since July 24.

**Confirmed fixed — no action needed:** estimate links resolve (NOT_FOUND gone, verified on multiple estimates including a brand-new API-created one), and the `info@mail.propertyrenovatorshomeservices.com` sending domain is live.

**Not Olu's problem (solved on our side):** the missing email logo (our API payloads now include `logoUrl`); exact 1/3 deposits (we'll send `33.3333`, which the API stores at 4-decimal precision); voiding stale estimates (the DELETE estimate endpoint works).
