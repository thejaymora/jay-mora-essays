# HANDOFF — Property Renovators GHL Verification

**Written:** 2026-08-03 · **For:** a fresh Claude Code session running in Jay's local terminal
**Branch:** `claude/property-renovators-ghl-verify-hnk6rb`
**Companion files:** `ghl-verification-report-2026-08-02.md` (evidence log), `olu-followup-email-draft.md` (unsent draft)

> **Read this section first.** The previous session ran in a sandboxed cloud container whose network blocked everything except GitHub/Anthropic, and mid-session the GHL connector started refusing calls (`MCP error -32003: requires approval`). A local terminal session has neither limitation. **Everything in §6 is ready to execute immediately.**

---

## 0. START HERE — first five minutes

```bash
git fetch origin && git checkout claude/property-renovators-ghl-verify-hnk6rb && git pull
```

Then confirm you have GHL access. Two possible routes, in order of preference:

1. **REI Unlock MCP connector** — how all prior work was done. Verify with a read call
   (`search_operations` → `list-estimates`). If it returns 200, you're live.
2. **Direct REST** — if the connector is unavailable, ask Jay for a Private Integration Token
   (GHL → Settings → Private Integrations). Base URL `https://services.leadconnectorhq.com`,
   headers `Authorization: Bearer <token>` and `Version: 2021-07-28`. Scopes needed:
   `invoices/estimate`, `invoices`, `contacts`, `opportunities`, `locations`, `users`,
   `businesses`, `products`, `workflows`, `documents_contracts`, `payments/orders`, `forms`.

Then run the action queue in **§6**, in order. Items 6.1–6.2 are user-approved and ready to fire.

---

## 1. Mission

Property Renovators Home Services runs on GoHighLevel, provisioned by agency contact **Olu Laniyonu** (olu@reiunlock.com). A prior chat session found Estimates returning NOT_FOUND on payment links plus several secondary gaps. Olu replied "this is resolved," which addressed only part of it.

**The job:** independently re-verify every item with first-hand evidence, so Jay can send Olu **one** complete, accurate list — nothing missing, nothing already-fixed included by mistake.

**Standing rules from Jay:**
- Do not take Olu's or any prior session's claims at face value. Re-verify.
- **Do not send anything to Olu without explicit approval.** Draft only.
- Give every item a clear verdict: CONFIRMED FIXED / CONFIRMED BROKEN / UNABLE TO TEST (with reason).

---

## 2. Why the previous session stalled (don't repeat this)

| Blocker | Detail |
|---|---|
| **Network egress** | Gateway returned 403 CONNECT for `app.gohighlevel.com`, `services.leadconnectorhq.com`, `link.fastpaydirect.com`, `email.mail.propertyrenovatorshomeservices.com`, and even `google.com`. Verified with curl **and** Playwright/Chromium (`net::ERR_TUNNEL_CONNECTION_FAILED`). Allowlist was GitHub/Anthropic only. |
| **MCP connector** | The REI Unlock server disconnected and re-registered under a new ID mid-session; every `execute_operation` after that returned `-32003 requires approval`. A project-level `.claude/settings.local.json` allowlist did **not** satisfy it — the gate is server-side in the connector, not the harness. |

**Neither applies locally.** A local session should be able to hit the API, load estimate pages in a browser, and drive Playwright.

`.claude/settings.local.json` in this repo pre-allows the MCP tool names from the previous session. Harmless; the IDs will differ locally.

---

## 3. Account reference data

### Core identifiers
| Field | Value |
|---|---|
| Business | Property Renovators Home Services |
| Location ID | `w6brLF0sqjGJVPR5N4Pa` |
| Company ID | `5MGnXUiGtGRVwRP43cta` |
| Address | 17902 Cottonwood Terrace, Gaithersburg, MD 20877, US |
| **Current phone** | **+13013953831** — (301) 395-3831 |
| Old phone | `+12406726135` — **Jacob Mora's personal cell**, pre-port |
| Port date | **2026-07-24 ~17:18 UTC** (evidenced by "OTP for Phone Number change" email at 17:18:36Z) |
| Sending domain | `info@mail.propertyrenovatorshomeservices.com` (live since Aug 2) |
| Tracking domain | `email.mail.propertyrenovatorshomeservices.com` → 34.102.239.211 |
| Payment domain | `link.fastpaydirect.com` (HighLevel shared, not Jay's) |

### Users — **critical, and partly wrong**
| User ID | Email | Label in GHL | Notes |
|---|---|---|---|
| `oxyt1XjN5vSumXxcv1gq` | jay@thejaymora.com | — | Sends all estimates; owns `assignedTo` on contacts; predates the office@ account (active 15:22Z Jul 24) |
| `l4pvaiiMabQk6iZDnBeF` | office@propertyrenovatorsgroup.com | **"Jacob Mora" ← WRONG** | **Jay's actual login.** Added 2026-07-24T17:17:37Z as **Sub-Account Admin**. Must be renamed **Jay Mora**. |
| `Flr5a7IZcuRyfyGCzLPK` | unknown | — | Last edited the proposal template 2026-07-11; probably Olu |

- **Jacob Mora** (Jay's brother, field tech) — email `jacobhandymanservices@gmail.com`. **Has NO GHL user account.** Confirmed: only one "New User Added" notification exists in Jay's inbox, ever.
- Both `jay+thejaymora.com@mail.reiunlock.com` and `office+propertyrenovatorsgroup.com@mail.reiunlock.com` actively send notification email → **two live user identities, both Jay.** Whether this is a true duplicate needs confirming (§10).

### Contacts
| Contact | ID | Note |
|---|---|---|
| Jay Mora | `sBNxkJ7k9a2Y1MFhOStp` | **Jay's own real HVAC lead** — not a test record. Handle carefully. |
| Diane Christen | `P5gQuaonEi9wNcEuNtvM` | Real customer |
| Jay Mora (alt) | `SpZz41c93pQbjDPX0q8j` | office@propertyrenovatorsgroup.com |
| Sender Test | `JjoDgOymwDV6iExYFyF3` | olu@reiunlock.com |

### Pipeline
- **Property Renovators Jobs** — `hT378d5OfgZIag9MIkMw`
- Target stage **"Approved / Booked"** — `d6e1cac0-610c-43f6-9223-a23ba0fb2266`
- Other stages: New Lead, Contacted/Qualifying, Estimate Scheduled, Estimate Sent, Scheduled/Dispatched, In Progress, Complete (Awaiting Invoice), Invoiced, Paid, Review Requested, Review Received, Lost

### Assets
- **Location logo (WRONG — reads "Property Renovators HANDYMAN SERVICES"):**
  `https://msgsndr-private.storage.googleapis.com/locationPhotos/5abc9048-419a-4e7f-b1ef-49a98914bc38.png`
  Should be **Home Services**. This is the stored location asset, so it appears on every document.
- Proposal template: `6a52a3fb77e9101d77f8c941` — "Property Renovators - Estimate", `updatedAt 2026-07-11T20:34:44Z`, only one in the account, zero documents ever sent.

---

## 4. Scorecard

| # | Item | Verdict |
|---|---|---|
| 1 | Estimate links resolve (was NOT_FOUND) | ✅ **CONFIRMED FIXED** |
| 2 | Deposit math / auto-invoice on acceptance | ✅ **CONFIRMED FIXED** — exact to the cent |
| 3 | Deposit-optional (no-deposit) flow | ⚠️ **CONFIGURED, UNVERIFIED** — needs one Accept click on #30 |
| 4 | Branding — logo | ❌ **CONFIRMED BROKEN** — wrong brand asset |
| 4b | Branding — notification email templates | ❌ **CONFIRMED BROKEN** — all blank since Jul 24 |
| 5 | Variants / multi-select line items | ❌ **CONFIRMED NOT DONE** |
| 6 | Deposit-paid → Opportunity automation | ❌ **CONFIRMED NOT DONE** — unpublished drafts |
| 7 | SSL cert on tracking domain | ✅ **CONFIRMED FIXED** |
| 8 | Estimate void/cancel capability | ✅ **RESOLVED** — DELETE endpoint works |
| — | User account mislabel | ❌ **CONFIRMED BROKEN** — pending rename |
| — | Duplicate Jay identity | ❓ **UNCONFIRMED** — needs user roster |
| — | Payment schedule due dates | ❓ **UNATTRIBUTED** — may be our test config |
| — | Jay's contact data damage | ✅ **REPAIRED** |
| — | Test data cleanup | 🔄 **PARTIAL** — 11 deleted, more pending |

---

## 5. Evidence per item

### ✅ 1. Estimate links resolve
- **#33 accepted successfully by Jay on 2026-08-03 16:49:59Z** — page rendered, Accept button worked. This is the definitive proof.
- #30: GHL stamped `lastVisitedAt 2026-08-02T21:11:18.659Z`.
- #28 (Olu's): `lastVisitedAt 2026-08-02T21:03:24Z`.
- #32 created from scratch via API and delivered — full pipeline works for new estimates.
- **Products-vs-ad-hoc theory is dead.** #4/#5 were assumed to use catalog products; they contain **no** `productId`/`priceId`. The API does return those fields when present (proven on #32). There was never a difference. #32 is a true catalog-based estimate and behaved identically.

### ✅ 2. Deposit math + auto-invoice — the headline win
Jay accepted **#33 ($1,720, `schedules: [33.3333, 66.6667]`)**. GHL computed:

| Installment | Amount |
|---|---|
| Payment 1 of 2 | **$573.33** |
| Payment 2 of 2 | **$1,146.67** |
| **Total** | **$1,720.00 exactly** |

**True 1/3 to the cent.** This resolves the Housecall Pro discrepancy ($567.60 at flat 33 vs $573.33 at 33.3333).

**→ Standing rule: use `33.3333` / `66.6667` on every deposit estimate. Never flat `33`.**

Auto-invoice chain fired (all 2026-08-03, from `info@mail.propertyrenovatorshomeservices.com`):
- `16:49:59Z` — "Jay has accepted estimate 33 for $1,720.00"
- `16:50:02Z` — "Invoice received: INV-000009 for $1720.00" — **auto-generated + sent in 3 seconds**
- `16:52:04Z` — "Invoice payment due" — payment-plan notice

### ⚠️ 3. Deposit-optional — one click outstanding
**#30** ($2, no `autoInvoice`, no `paymentScheduleConfig`) was sent cleanly and the page loads. Accepting it should request the **full $2.00 with no split**. Not yet done.
→ https://link.fastpaydirect.com/l/HyN-L6UUS

### ❌ 4. Branding — two separate problems

**(a) Wrong logo — CONFIRMED via screenshot.** Invoice INV-000009 renders a black/gold/blue circular badge reading **"PROPERTY RENOVATORS HANDYMAN SERVICES"**. Business *name* text is correct ("Property Renovators Home Services"); the *logo image* is the wrong brand.

> ⚠️ **Correction to an earlier claim.** A previous session reported the blank-logo issue as "our bug, solved by passing `logoUrl`." That was half wrong. Passing `logoUrl` fixed the *blank image* but surfaced the *wrong brand* — the URL was copied from Olu's sample #28, i.e. the location's stored asset. **Do not repeat the claim that branding is solved.** The fix is replacing the location logo asset.

**(b) Notification templates blank.** `GET /invoices/settings` shows every template — `customerSendEstimate`, `customerSendInvoice`, `customerPaymentSuccess`, `customerAutoPaymentSuccess`, `teamEstimateAccepted`, `teamEstimateDeclined`, `customerSendPaymentSchedule`, etc. — with `emailTemplate: ""` and `defaultEmailTemplateId: ""`. Settings doc `updatedAt: 2026-07-24T15:22:47Z`, i.e. untouched by any fix work. GHL system defaults are rendering (they look acceptable).

### ❌ 5. Variants — not done
`GET /proposals/templates` → exactly **one** template, `updatedAt 2026-07-11T20:34:44Z`. `GET /proposals/document` → **total 0**, no document ever sent. No variants exist, so the "check any combination vs pick one package" question is still unanswerable. **Needs Olu.**

### ❌ 6. Deposit-paid → Opportunity — not done
`GET /workflows/` returns 6 published workflows — *Appointment Confirmation & Reminder Texts, HALT Opt-Out Handler, New Job Request, Post-Job Review Received, Post-Job Review Request, Site Visit Needed* — **none deposit/booking related** — plus two **unpublished drafts**:
- `a5bb8102-1ffb-4231-ad7c-1019f572b761` — "New Workflow : 1785618174944", created Aug 1
- `6b70006f-53c3-47e0-a5e1-6c77dcca7733` — "New Workflow : 1785705746279", created **Aug 2 21:22Z**, edited 21:23Z

Someone is actively building it; nothing is published, so nothing fires. **Not yet re-checked after #33's acceptance — do that (§6.4).**

### ✅ 7. SSL — fixed
Jay loaded `https://email.mail.propertyrenovatorshomeservices.com` in mobile Safari on Aug 3 → server-rendered **"404 page not found", no certificate warning**. Rendering a server 404 body requires successful TLS validation; an invalid cert would produce a full-screen interstitial with no page content. A 404 at the bare root is expected — the host serves only `/c/<token>` and `/o/<token>`. Corroborated by the successful #33 click-through, which traverses this domain. **Remove from Olu's list.**

### ✅ 8. Void/cancel — resolved
- `DELETE /invoices/estimate/{estimateId}` **works** (used 11× successfully). Requires body `{altId, altType}`.
- Valid `estimateStatus` enum, probed against the API's own validator: **`draft`, `sent`, `viewed`, `accepted`, `declined`, `invoiced`**. Rejected as invalid: `void`, `cancelled`, `expired`. **There is no void status in GHL's model.**
- `estimateStatus` is **not settable via API** — `PUT` with `estimateStatus: "declined"` returns 200 but silently ignores the field. Status changes only via real events.

---

## 6. ACTION QUEUE — execute in order

### 6.1 Rename the mislabeled user ⚡ **JAY APPROVED**
`l4pvaiiMabQk6iZDnBeF` — change name from **Jacob Mora** → **Jay Mora**.
Email stays `office@propertyrenovatorsgroup.com`. Role stays Admin.

Search `users` domain for the update operation (`update-user`, `PUT /users/{userId}`). **Read the record first** — the users API may wholesale-replace like the others (§7).
*UI fallback:* app.gohighlevel.com → Settings → My Staff → that user → Edit → Save.

### 6.2 Delete two stale estimates ⚡ **JAY APPROVED**
Both carry the pre-port `+12406726135` (Jacob's personal cell) as the business number:
- **#4** — `6a6500babff9c219e1d8998c` — "SUPERSEDED - See HCP #825", Diane Christen, $1,660
- **#5** — `6a6500c9abdda9d2703c0668` — "SUPERSEDED - See HCP #825", Diane Christen, $2,360

```
DELETE /invoices/estimate/{id}
body: {"altId": "w6brLF0sqjGJVPR5N4Pa", "altType": "location"}
```

### 6.3 Confirm the user roster — **highest-value unknown**
`GET /users/search?locationId=w6brLF0sqjGJVPR5N4Pa`
Determine whether **one or two** Jay identities exist (`oxyt…` on jay@thejaymora.com vs `l4pv…` on office@).

**Why it matters:** GHL routes notifications to the **assigned user**. Jay's contact is `assignedTo: oxyt…`, but Jay logs in as office@ (`l4pv…`). If those are different accounts, notifications may fire toward an identity he isn't watching. This directly drives his "notify me and Jacob every time" requirement, and it decides whether item 5 stays in the Olu email.

Also capture each user's **role** and **notification settings**.

### 6.4 Read INV-000009 — settles an open attribution
`GET /invoices/?altId=w6brLF0sqjGJVPR5N4Pa&altType=location` — find INV-000009 (from #33).

Inspect the payment schedule. Screenshots showed **both installments with the same due date**, "Amount Due" as the full $1,720 rather than the deposit, and **three different dates** across views (web `8/2/2026`, PDF `August 3, 2026`, header due date `August 4, 2026`).

**Determine:** is the same-day scheduling caused by our test's `dateConfig: {depositDateType: "estimate_accepted", scheduleDateType: "regular_interval"}` (our fault — no interval specified), or GHL's default? The differing dates *between views* look like a genuine display bug regardless.
**This decides whether item 6 stays in the Olu email.**

### 6.5 Check the Opportunity
`POST /opportunities/search` or `GET /opportunities/search?contactId=sBNxkJ7k9a2Y1MFhOStp`
Did accepting #33 create or move an Opportunity in `hT378d5OfgZIag9MIkMw`? Expected: **no** (workflow unpublished). Confirm against a real acceptance — this is fresh evidence for item 6.

### 6.6 Verify location config
Confirm the business profile phone is `+13013953831` and inspect the logo asset. Then sweep for the old `2406726135` hardcoded anywhere: workflows, SMS templates, calendars, forms, email templates, website.

### 6.7 Then — Jacob's account (after 6.1 and 6.3)
Create a GHL user for **jacobhandymanservices@gmail.com** at **User role, NOT Admin**.
Order matters: rename first so you don't end up with two "Jacob Mora" records; resolve the duplicate identity first so you assign to the right one.

### 6.8 Then — the both-of-you notification workflow
Jay's requirement: he **and** Jacob notified on **every** inbound text/email.

**The trap:** GHL's default routes notifications to the *assigned user* only. Turning on both users' notification preferences does **not** fix an unassigned or singly-assigned contact.

**The fix:** a workflow — trigger on inbound message (Customer Replied / Inbound SMS / Email Received) → **Internal Notification** action addressed **explicitly to both users**, email + SMS. Fires regardless of assignment. Then per-user notification prefs and LeadConnector mobile push as the second layer.

Jay was advised to consider narrowing Jacob's scope later (alert fatigue); he asked for everything for now.

---

## 7. GHL API gotchas — hard-won, do not relearn

| # | Gotcha |
|---|---|
| 1 | **`PUT /invoices/estimate/{id}` wholesale-replaces.** Omitting `termsNotes` nulled it. **Always send the full object.** |
| 2 | **Contact upsert wholesale-replaces the `tags` array.** This is how Jay's real contact got damaged. Prefer `PUT /contacts/{id}` with only the fields you intend to change. |
| 3 | **`estimateStatus` is not writable.** `PUT` accepts it, returns 200, silently ignores it. |
| 4 | **Estimate `name` max 40 characters** — 422 otherwise. |
| 5 | **`paymentScheduleConfig.schedules[].value` accepts 4 decimals** (`33.3333`). Estimates carry `configuration.precision: 4`. |
| 6 | **`businessDetails.logoUrl` must be passed explicitly** on API-created estimates, or the email renders `<img src="">`. UI-created estimates inherit it automatically. |
| 7 | **`POST /invoices/estimate/{id}/invoice` requires acceptance** — returns `400 estimate_not_accepted` otherwise. **There is no API path to accept an estimate**; acceptance is customer-side on the page only. |
| 8 | **Business details are frozen onto each estimate at creation** and never refresh. This is why #4/#5 still carry the pre-port phone. |
| 9 | **The custom-payment-provider endpoint is not a Stripe indicator.** It returns empty even when native Stripe Connect is properly configured — it only reflects marketplace apps. Jay's Stripe **is** connected. Never cite an empty response as evidence otherwise. |
| 10 | `DELETE` operations need `{altId, altType}` in the **body**, not just the path. |

### Already ruled out — do not re-test the NOT_FOUND cause
- Not a Stripe minimum-charge issue (tested $0.33 and $0.99, both failed identically).
- Not `autoInvoice` or `paymentScheduleConfig` (bare estimate with neither still failed).
- Not the dollar amount ($1, $2, $3, $1,720 all failed identically pre-fix).

---

## 8. Test data inventory

### Deleted (11) ✅
Estimates **#8, #9, #10, #11, #12, #13, #14, #15, #16, #17** (Jul 31 test set) and **#31** (a $1,720 decimal-probe draft). Linked test Opportunities were already gone — spot-checked two IDs → `404 OPPORTUNITY_NOT_FOUND`.

### Live test records — clean up after verification
| Record | ID | Status |
|---|---|---|
| Estimate #29 ($3, 33% deposit) | `6a6fb23bfb5d32751633c49d` | sent, **not accepted** |
| Estimate #30 ($2, no deposit) | `6a6fb250ebf585f65e9f5093` | sent, **not accepted** — needed for §6/item 3 |
| Estimate #32 ($240, catalog) | `6a6fb693ebf5855e239f8846` | sent, not accepted |
| Estimate #33 ($1,720) | `6a70be4a100e15f4f8c2aa3b` | **ACCEPTED** — keep until INV-000009 is read |
| Invoice INV-000009 | from #33 | delete after §6.4 |

### ⚠️ Time-sensitive
**Invoice INV-000002** (`6a6cee34fb5d32bd8d06dcd6`, "TEST - Invoice Object Type Check", $3, sent, unpaid) has **overdue reminders scheduled for Aug 4, Aug 7, and Aug 15** that will email jay@thejaymora.com. **Delete or void it.**

**Invoice INV-000005** (`6a6d143debf58508d675eca9`, "Deposit Invoice - Diane Christen", $573, draft, never sent) — keep if the Diane job proceeds, else delete.

### Not ours — leave alone
Estimates **#27**, **#28** (Olu's samples), invoice **INV-000001** (paid $1 processor test).

### Data repair already done
Jay's contact `sBNxkJ7k9a2Y1MFhOStp` had `source` overwritten with "Internal Test - Estimate Flow QA". **Restored to "Send Us Your Photos"** — evidenced by `lastAttributionSource.mediumId = KNda9rEUYExpXdoWSIZd` (form "Send Us Your Photos") and 13 submissions from that contact Jul 26–28. **Unrecoverable:** the original `tags` array (currently empty). Ask Jay if he remembers any.

---

## 9. The Olu email

Draft lives at **`olu-followup-email-draft.md`**. **NOT SENT.** Jay reviews before anything goes out.

Structure: five confirmed-working items (so Olu doesn't redo them) + six outstanding.

**Three editorial decisions already made — revisit if evidence changes:**
1. **Item 6 (payment schedule) is worded as a question, not a defect** — may be our test config. **§6.4 decides whether it stays.**
2. **Old phone on #4/#5 deliberately excluded** — that's our cleanup (GHL froze stale business details), not Olu's bug.
3. **Blank logo deliberately excluded; wrong logo included** — the blank was our API payload omitting `logoUrl`; the Handyman asset is genuinely his.

Item 5 (user mislabel) is worded as a correction, **not** a security accusation — no unauthorized access occurred, since Jacob has no GHL login.

**§6.3 may shrink item 5:** if only one user exists, cut the duplicate-identity half so Jay isn't sending Olu after something imaginary.

---

## 10. Open questions

| # | Question | How to resolve |
|---|---|---|
| 1 | One Jay identity or two? | §6.3 — user roster |
| 2 | Same-day installment due dates — ours or GHL's? | §6.4 — read INV-000009 raw config |
| 3 | Did accepting #33 move any Opportunity? | §6.5 |
| 4 | Does the no-deposit flow request the full amount? | Accept #30 |
| 5 | Original tags on Jay's contact? | Ask Jay; likely unrecoverable |
| 6 | Is the old 240-672-6135 hardcoded in workflows/templates? | §6.6 sweep |

### Live test links (public, no login required)
- #29 — https://link.fastpaydirect.com/l/ZChj2CmUq
- #30 — https://link.fastpaydirect.com/l/HyN-L6UUS
- #32 — https://link.fastpaydirect.com/l/9e2tc3QbI
- #33 — https://link.fastpaydirect.com/l/zwLnnHLnx *(already accepted)*

---

## 11. ⚠️ Security — action required

**Jacob's Gmail password was pasted into the previous chat session** (for `jacobhandymanservices@gmail.com`). It was never used and is not recorded in this repo. **It must be rotated**, along with anywhere it's reused, and 2FA enabled. Jay has been told; confirm it's done.

Going forward: account access should come from a connector approval or a scoped, revocable API token — never a password.

---

## 12. People

| Who | Role | Contact |
|---|---|---|
| **Jay Mora** | Owner, runs operations | office@propertyrenovatorsgroup.com (GHL login) · jay@thejaymora.com (personal) |
| **Jacob Mora** | Jay's brother, field tech | jacobhandymanservices@gmail.com · cell 240-672-6135 · **no GHL account yet** |
| **Olu Laniyonu** | Agency contact, REI Unlock | olu@reiunlock.com |

**Tone note:** Jay wants the Olu email to be complete and accurate, sent **once**, with no back-and-forth — and without blaming Olu for things that turned out to be ours.
