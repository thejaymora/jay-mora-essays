# HANDOFF — Property Renovators GHL Verification

**Written:** 2026-08-03 · **For:** a fresh Claude Code session in Jay's local terminal
**Branch:** `claude/property-renovators-ghl-verify-hnk6rb`
**Companion files:** `ghl-verification-report-2026-08-02.md` (running evidence log) · `olu-followup-email-draft.md` (unsent draft)

> **Why this exists.** The previous session ran in a sandboxed cloud container whose network blocked every host except GitHub/Anthropic, and mid-session the GHL connector began refusing calls (`MCP error -32003: requires approval`). A local terminal has neither limitation. **§7 is ready to execute immediately.**

---

## Contents

| § | Section |
|---|---|
| 0 | Start here — first five minutes |
| 1 | Mission and standing rules |
| 2 | Why the previous session stalled |
| 3 | Account reference data |
| 4 | Chronology |
| 5 | Scorecard |
| 6 | Evidence per item |
| 7 | **Action queue — execute in order** |
| 8 | GHL API gotchas |
| 9 | Operation ID reference |
| 10 | Test data inventory |
| 11 | Primary evidence that lives outside this repo |
| 12 | The Olu email |
| 13 | Open questions |
| 14 | Security |
| 15 | People |
| 16 | Definition of done |

---

## 0. START HERE — first five minutes

```bash
git fetch origin && git checkout claude/property-renovators-ghl-verify-hnk6rb && git pull
```

Confirm GHL access — two routes, best first:

1. **REI Unlock MCP connector** — how all prior work was done. Verify with a read
   (`search_operations` → `execute_operation` on `list-estimates`). A 200 means you're live.
2. **Direct REST** — if the connector is unavailable, ask Jay for a Private Integration Token
   (GHL → Settings → Private Integrations).
   - Base URL `https://services.leadconnectorhq.com`
   - Headers: `Authorization: Bearer <token>`, `Version: 2021-07-28`, `Content-Type: application/json`
   - Scopes: `invoices/estimate`, `invoices`, `invoices/schedule`, `contacts`, `opportunities`,
     `locations`, `users`, `businesses`, `products`, `products/prices`, `workflows`,
     `documents_contracts`, `documents_contracts_template`, `payments/orders`,
     `payments/transactions`, `forms`

**Time-sensitive:** invoice **INV-000002** has overdue reminders scheduled for **Aug 4, Aug 7, Aug 15** that will email Jay. Kill it early (§10).

Then work §7 in order.

---

## 1. Mission and standing rules

Property Renovators Home Services runs on GoHighLevel, provisioned by agency contact **Olu Laniyonu** (olu@reiunlock.com). A prior chat session found Estimates returning NOT_FOUND on payment links, plus several secondary gaps. Olu replied "this is resolved," which addressed only part of it.

**The job:** independently re-verify every item with first-hand evidence, so Jay sends Olu **one** complete, accurate list — nothing missing, nothing already-fixed included by mistake.

**Standing rules from Jay:**
- Do not take Olu's or any prior session's claims at face value. Re-verify.
- **Never send anything to Olu without explicit approval.** Draft only.
- Every item gets a clear verdict: CONFIRMED FIXED / CONFIRMED BROKEN / UNABLE TO TEST (with the reason).
- Don't blame Olu for anything that turns out to be ours.

---

## 2. Why the previous session stalled

| Blocker | Detail |
|---|---|
| **Network egress** | Gateway returned 403 CONNECT for `app.gohighlevel.com`, `services.leadconnectorhq.com`, `link.fastpaydirect.com`, `email.mail.propertyrenovatorshomeservices.com`, `mail.google.com`, even `google.com`. Verified with curl **and** Playwright/Chromium (`net::ERR_TUNNEL_CONNECTION_FAILED`). Allowlist was GitHub/Anthropic only. |
| **MCP connector** | The REI Unlock server disconnected and re-registered under a new ID mid-session; every `execute_operation` afterward returned `-32003 requires approval`. A project `.claude/settings.local.json` allowlist did **not** satisfy it — the gate is server-side in the connector, not in the Claude Code harness. |

**Neither applies locally.** A local session should reach the API, load estimate pages in a browser, and drive Playwright.

`.claude/settings.local.json` pre-allows the previous session's MCP tool names. Harmless; local IDs will differ.

---

## 3. Account reference data

### 3.1 Core identifiers
| Field | Value |
|---|---|
| Business | Property Renovators Home Services |
| Location ID | `w6brLF0sqjGJVPR5N4Pa` |
| Company ID | `5MGnXUiGtGRVwRP43cta` |
| Address | 17902 Cottonwood Terrace, Gaithersburg, MD 20877, US |
| Website | `https://propertyrenovatorshomeservices.com/` |
| **Current phone** | **`+13013953831`** — (301) 395-3831 |
| Previous phone | `+12406726135` — **Jacob Mora's personal cell** |
| Phone change initiated | 2026-07-24 17:18:36Z ("OTP for Phone Number change" email) |
| Phone change effective | Between **2026-07-25 18:30Z** and **2026-07-31 17:59Z** (see §6, item on stale numbers) |
| Sending domain | `info@mail.propertyrenovatorshomeservices.com` (live since Aug 2) |
| Tracking domain | `email.mail.propertyrenovatorshomeservices.com` → `34.102.239.211` |
| Payment domain | `link.fastpaydirect.com` (HighLevel shared — not Jay's, not configurable) |
| Number prefixes | Invoices `INV-`, Estimates `EST-` |
| Tips | Enabled, `[5, 10, 15]` |

### 3.2 Users — **critical, and partly wrong**
| User ID | Email | Label in GHL | Notes |
|---|---|---|---|
| `oxyt1XjN5vSumXxcv1gq` | jay@thejaymora.com | — | Sends all estimates (`sentBy`); owns `assignedTo` on contacts; active **15:22Z Jul 24**, i.e. **predates** the office@ account |
| `l4pvaiiMabQk6iZDnBeF` | office@propertyrenovatorsgroup.com | **"Jacob Mora" ← WRONG** | **Jay's actual login.** Added 2026-07-24T17:17:37Z as **Sub-Account Admin**. Rename to **Jay Mora**. |
| `Flr5a7IZcuRyfyGCzLPK` | unknown | — | Last edited the proposal template 2026-07-11; probably Olu |

- **Jacob Mora** (Jay's brother, field tech) — `jacobhandymanservices@gmail.com`. **Has NO GHL account.** Confirmed: exactly one "New User Added" notification exists in Jay's inbox, ever.
- **Evidence of two live Jay identities:** GHL stamps the notification sender with the acting user's email, and **both** appear:
  - `jay+thejaymora.com@mail.reiunlock.com` → invoices INV-000001/000002, estimates #10–15
  - `office+propertyrenovatorsgroup.com@mail.reiunlock.com` → every "New job request" / "New lead" notification
- Jay confirmed he logs in as **office@propertyrenovatorsgroup.com** and that "Jacob Mora" on it is a mislabel.
- ⚠️ Jacob may hold multiple email addresses. `amora0406@gmail.com` sends job emails signed *"Jacob Mora 240-672-6135 Handyman Contractor."* Other family/business addresses in circulation: `propertyrenovatorshandyman@gmail.com`, `propertyrenovatorsmd@gmail.com`. Don't assume one address per person.

### 3.3 Contacts
| Contact | ID | Note |
|---|---|---|
| Jay Mora | `sBNxkJ7k9a2Y1MFhOStp` | **Jay's own real HVAC lead — NOT a test record.** Previously damaged; see §10. |
| Diane Christen | `P5gQuaonEi9wNcEuNtvM` | Real customer, real job |
| Jay Mora (alt) | `SpZz41c93pQbjDPX0q8j` | office@propertyrenovatorsgroup.com |
| Sender Test | `JjoDgOymwDV6iExYFyF3` | olu@reiunlock.com |
| Jay Mora (alt 2) | `JgAWkodiK2m3f4SvaEc1` | Tied to INV-000001 |
| Platform Test | `ukAiF8tiuBoDakm3vtdj` | help@reiunlock.com |

### 3.4 Pipeline
**Property Renovators Jobs** — `hT378d5OfgZIag9MIkMw`
Target stage **"Approved / Booked"** — `d6e1cac0-610c-43f6-9223-a23ba0fb2266`
Full order: New Lead · Contacted/Qualifying · Estimate Scheduled · Estimate Sent · **Approved/Booked** · Scheduled/Dispatched · In Progress · Complete (Awaiting Invoice) · Invoiced · Paid · Review Requested · Review Received · Lost

### 3.5 Workflows
| ID | Name | Status |
|---|---|---|
| `8694af4e-9938-4cd8-bbd0-7322149d4d38` | Appointment Confirmation & Reminder Texts | published v40 |
| `9f380980-bfc3-4341-bd32-48d76ebe8ff1` | HALT Opt-Out Handler | published v5 |
| `12795a85-6655-4338-9b29-386c3c998d57` | New Job Request | published v25 |
| `28f41786-3748-4791-85cf-c1a2090afdb4` | Post-Job Review Received | published v11 |
| `8cdcb662-5f32-43ef-87cd-03f30f0d58cf` | Post-Job Review Request (Customer Feedback) | published v13 |
| `55399d84-ad5f-4b48-92e4-08cab6ea61fe` | Site Visit Needed | published v12 |
| `a5bb8102-1ffb-4231-ad7c-1019f572b761` | "New Workflow : 1785618174944" | **DRAFT** — created Aug 1 21:02Z |
| `6b70006f-53c3-47e0-a5e1-6c77dcca7733` | "New Workflow : 1785705746279" | **DRAFT** — created Aug 2 21:22Z, edited 21:23Z |

**No published workflow touches deposits or job booking.** The two drafts are presumably Olu's in-progress attempt.

### 3.6 Forms
| ID | Name |
|---|---|
| `KNda9rEUYExpXdoWSIZd` | Send Us Your Photos ← origin of Jay's contact |
| `0lE0tIf8pen6GKtS34D8` | Request an Estimate |
| `AvLCrwFyhYdy5NCeVwAx` | Contact Us |
| `fHuK51qpAdkOo8NXTa1f` | Marketing Form - Claim Offer |
| `3fb7yG60GGifxR6GgMj9` | Newsletter Subscriptions |

### 3.7 Products & templates
- **206 products** in the catalog, seeded 2026-07-16, all `productType: SERVICE`.
- Example used in testing: **Window Crank - Replacement (Casement Windows)**
  `productId: 6a59149492a3d6cc9df817db` · `priceId: 6a591494c5b1cfd2dea339d4` · $240 "Flat Rate" · SKU `WIND-CRNK-128`
- **Proposal template:** `6a52a3fb77e9101d77f8c941` — "Property Renovators - Estimate", `type: proposal`, v2, `updatedAt 2026-07-11T20:34:44Z`, `updatedBy Flr5a7IZcuRyfyGCzLPK`. **The only one.** Zero documents ever sent.

### 3.8 Assets
**Location logo (WRONG — reads "PROPERTY RENOVATORS HANDYMAN SERVICES"):**
`https://msgsndr-private.storage.googleapis.com/locationPhotos/5abc9048-419a-4e7f-b1ef-49a98914bc38.png`
Should be **Home Services**. Black/gold/blue circular badge. This is the stored location asset, so it appears on every document that renders a logo.

Agency logo (REI Unlock, for reference): `companyPhotos/45758b26-739d-4a98-9c35-ae852c762fd6.png`

### 3.9 Custom fields on Jay's contact
| Field ID | Value |
|---|---|
| `Nm7NLyuhcvc9IgnL6GRK` | Facebook |
| `lbUaIX8O6SERCnNJwBHF` | Ballenger Creek |
| `nHsdh9qZO5m9hvvrVfqO` | HVAC (heating or cooling) |
| `x9edyBm6zy9d3Er2tVc9` | "Need a new capacitor and an OFM for my York AC" |
| `hHmrAR8SrAuM48HYhfe6` | 9 uploaded photos |
| `A3jb0vrrHpltLnrLfneX` | "built 2026-07-28T14:26:10.393Z \| 9 photos" |
| `d4J7Tmm06B2kdEYLSwVe` | lead-report URL |

---

## 4. Chronology

| When (UTC) | Event |
|---|---|
| 2026-06-04 21:11 | Jay's contact created via "Send Us Your Photos" form |
| 2026-07-11 20:34 | Proposal template last edited (by `Flr5a7IZcuRyfyGCzLPK`) — **untouched since** |
| 2026-07-16 17:27 | Products catalog seeded (206 items) |
| 2026-07-24 14:26 | Invoice settings created |
| 2026-07-24 15:22 | INV-000001 created by `oxyt…`; invoice settings last updated 15:22:47 — **never since** |
| 2026-07-24 15:25 | INV-000001 paid ($1 processor test) |
| **2026-07-24 17:17:37** | **office@ user added as Sub-Account Admin, labeled "Jacob Mora"** |
| **2026-07-24 17:18:36** | **OTP for phone number change** — 59 seconds later, same sitting |
| 2026-07-25 18:30 | Estimates #4, #5 created — **still carry `+12406726135`** |
| 2026-07-31 17:59–18:47 | Test estimates #8–#17 created — **carry `+13013953831`** |
| 2026-08-01 21:02 | Draft workflow #1 created |
| 2026-08-02 20:26 | Estimate #24 accepted (Olu's test, $900) — later deleted |
| 2026-08-02 21:00–21:03 | Olu's samples #27, #28 |
| 2026-08-02 21:10 | #29, #30 created and sent |
| 2026-08-02 21:22 | Draft workflow #2 created |
| 2026-08-02 21:28 | #32 created and sent |
| 2026-08-03 16:14 | #33 created |
| 2026-08-03 16:17 | #33 sent |
| **2026-08-03 16:49:59** | **#33 ACCEPTED by Jay** |
| **2026-08-03 16:50:02** | **INV-000009 auto-generated and sent — 3 seconds later** |
| 2026-08-03 16:52:04 | Payment-schedule notice emailed |

---

## 5. Scorecard

| # | Item | Verdict |
|---|---|---|
| 1 | Estimate links resolve (was NOT_FOUND) | ✅ **CONFIRMED FIXED** |
| 2 | Deposit math + auto-invoice on acceptance | ✅ **CONFIRMED FIXED** — exact to the cent |
| 3 | Deposit-optional (no-deposit) flow | ⚠️ **CONFIGURED, UNVERIFIED** — needs one Accept on #30 |
| 4a | Branding — logo | ❌ **CONFIRMED BROKEN** — wrong brand asset |
| 4b | Branding — notification email templates | ❌ **CONFIRMED BROKEN** — all blank since Jul 24 |
| 5 | Variants / multi-select line items | ❌ **CONFIRMED NOT DONE** |
| 6 | Deposit-paid → Opportunity automation | ❌ **CONFIRMED NOT DONE** — unpublished drafts |
| 7 | SSL cert on tracking domain | ✅ **CONFIRMED FIXED** |
| 8 | Estimate void/cancel capability | ✅ **RESOLVED** — DELETE endpoint works |
| — | User account mislabel | ❌ **CONFIRMED BROKEN** — rename pending |
| — | Duplicate Jay identity | ❓ **UNCONFIRMED** — needs user roster |
| — | Payment schedule due dates | ❓ **UNATTRIBUTED** — see §6 |
| — | Jay's contact data damage | ✅ **REPAIRED** (tags unrecoverable) |
| — | Test data cleanup | 🔄 **PARTIAL** — 11 deleted, more pending |

---

## 6. Evidence per item

### ✅ 1. Estimate links resolve
- **#33 accepted by Jay 2026-08-03 16:49:59Z** — page rendered, Accept worked. Definitive.
- #30: GHL stamped `lastVisitedAt 2026-08-02T21:11:18.659Z`.
- #28 (Olu's): `lastVisitedAt 2026-08-02T21:03:24Z`.
- #24 (Olu's, $900): accepted 2026-08-02 20:26Z per notification email — proves Accept worked post-fix even before our tests. Estimate later deleted.
- #32 created from scratch via API and delivered — the full pipeline works for new estimates, not just Olu's samples.

**The products-vs-ad-hoc theory is dead.** It was assumed #4/#5 used catalog products while failing tests used ad-hoc items. They contain **no** `productId`/`priceId` — they were ad-hoc too. The list API *does* return those fields when present (proven on #32). There was never a difference. #32 is a genuine catalog-based estimate and behaved identically.

### ✅ 2. Deposit math + auto-invoice — the headline win
Jay accepted **#33 ($1,720, `schedules: [33.3333, 66.6667]`)**. GHL computed:

| Installment | Amount |
|---|---|
| Payment 1 of 2 | **$573.33** |
| Payment 2 of 2 | **$1,146.67** |
| **Total** | **$1,720.00 exactly** |

**True 1/3, to the cent.** Resolves the Housecall Pro discrepancy:

| Config | Deposit on $1,720 |
|---|---|
| `33` (flat) | $567.60 |
| `33.33` | $573.28 |
| **`33.3333`** | **$573.33 ✓** |

**→ Standing rule: use `33.3333` / `66.6667` on every deposit estimate. Never flat `33`.**

Auto-invoice chain (all 2026-08-03, from `info@mail.propertyrenovatorshomeservices.com`):
- `16:49:59Z` — "Jay has accepted estimate 33 for $1,720.00"
- `16:50:02Z` — "Invoice received: INV-000009 for $1720.00" — **auto-generated and sent in 3 seconds**
- `16:52:04Z` — "Invoice payment due" — payment-plan notice

Note the sender: #24's acceptance email on Aug 2 came from `noreply@mail.reiunlock.com`; #33's came from the correct branded domain. Another confirmation the sending-domain fix is real.

### ⚠️ 3. Deposit-optional — one click outstanding
**#30** ($2, no `autoInvoice`, no `paymentScheduleConfig`) was sent cleanly and the page loads. Accepting it should request the **full $2.00 with no split**.
→ https://link.fastpaydirect.com/l/HyN-L6UUS

### ❌ 4a. Wrong logo — CONFIRMED
Invoice INV-000009 renders a circular badge reading **"PROPERTY RENOVATORS HANDYMAN SERVICES"**. The business *name* text is correct ("Property Renovators Home Services"); the *logo image* is the wrong brand.

> ⚠️ **CORRECTION TO AN EARLIER CLAIM.** A previous session reported the blank-logo issue as "our bug, solved by passing `logoUrl`." **That was half wrong.** Passing `logoUrl` fixed the *blank image* but surfaced the *wrong brand* — the URL was copied from Olu's sample #28, i.e. the location's stored asset. **Do not repeat the claim that branding is solved.** The real fix is replacing the location logo asset. Until then, consider *omitting* `logoUrl` on customer-facing estimates rather than advertising the wrong brand.

### ❌ 4b. Notification templates blank
`GET /invoices/settings` → every template has `emailTemplate: ""` and `defaultEmailTemplateId: ""`:
`customerSendEstimate`, `customerSendInvoice`, `customerPaymentSuccess`, `customerAutoPaymentSuccess`, `customerPaymentFailure`, `customerAutoPaymentInfo`, `customerAutoPaymentFailure`, `customerAutoPaymentAmountChanged`, `customerSendPaymentSchedule`, `teamPaymentSuccess`, `teamAutoPaymentSuccess`, `teamPaymentFailure`, `teamAutoPaymentFailure`, `teamAutoPaymentSkip`, `teamRecurringSendInvoiceFailed`, `teamEstimateAccepted`, `teamEstimateDeclined`.

Settings doc `updatedAt: 2026-07-24T15:22:47Z` — untouched by any fix work. GHL system defaults render instead (they look acceptable in practice).

### ❌ 5. Variants — not done
`GET /proposals/templates` → exactly **one** template, `updatedAt 2026-07-11T20:34:44Z`.
`GET /proposals/document` → **total 0**. No document ever sent.
No variants exist, so the "can a client check **any combination** of items, or only pick **one package**?" question remains unanswerable. **Needs Olu**, and the answer must be tested, not guessed.

### ❌ 6. Deposit-paid → Opportunity — not done
Six published workflows, none deposit/booking related (§3.5). Two unpublished drafts with auto-generated names, the second created **Aug 2 21:22Z** — minutes after Olu's fix-verification estimates. Someone is actively building it; nothing is published, so nothing fires.

**Not yet re-checked after #33's acceptance.** Do that (§7.5) — it's fresh evidence against a real acceptance.

### ✅ 7. SSL — fixed
Jay loaded `https://email.mail.propertyrenovatorshomeservices.com` in mobile Safari on Aug 3 → server-rendered **"404 page not found", no certificate warning**.

Rendering a server 404 body requires DNS → TCP → **successful TLS validation** → HTTP response. An invalid cert produces a full-screen interstitial with no page content. A 404 at the bare root is expected — the host serves only `/c/<token>` (click) and `/o/<token>` (open) tracking paths and has no homepage. Corroborated by the successful #33 click-through, which traverses this domain. **Remove from Olu's list.**

### ✅ 8. Void/cancel — resolved
- `DELETE /invoices/estimate/{estimateId}` **works** — used 11× successfully. Requires body `{altId, altType}`.
- Valid `estimateStatus` enum, probed against the API's own validator:
  **`draft`, `sent`, `viewed`, `accepted`, `declined`, `invoiced`**
  Rejected as invalid: `void`, `cancelled`, `expired`. **GHL has no void status.**
- `estimateStatus` is **not settable via API** — `PUT` with `estimateStatus: "declined"` returns 200 but silently ignores it. Status changes only through real events.

### ❓ Stale phone on #4/#5 — corrected reasoning
Estimates #4/#5 (created Jul 25 18:30Z) carry `+12406726135`; #8 (Jul 31 17:59Z) carries `+13013953831`.

> **Correction:** an earlier note claimed GHL "froze stale business details" onto those documents. More likely the **location profile genuinely still held the old number on Jul 25** and was updated sometime between Jul 25 18:30Z and Jul 31 17:59Z. Either way an estimate snapshots business details at creation and never refreshes — so these two documents permanently advertise Jacob's personal cell. **This is our cleanup, not Olu's bug.** Jay approved deleting them (§7.2).

### ❓ Payment schedule due dates — unattributed
From Jay's screenshots of INV-000009:
- **Both installments show the same due date** — the balance is not deferred to completion
- **"Amount Due (USD)" reads $1,720.00** (full total) while the Pay button reads $573.33
- **Three different dates for one invoice:** web view `8/2/2026`, PDF view `August 3, 2026`, invoice header Due Date `August 4, 2026`

**The config used on #33 was:**
```json
"autoInvoice": { "enabled": true },
"paymentScheduleConfig": {
  "type": "percentage",
  "dateConfig": {
    "depositDateType": "estimate_accepted",
    "scheduleDateType": "regular_interval"
  },
  "schedules": [ { "value": 33.3333 }, { "value": 66.6667 } ]
}
```

⚠️ **Important:** that `dateConfig` was **copied from Olu's own sample #28**, which uses the identical `depositDateType`/`scheduleDateType` pair with `schedules: [33, 67]`. So if same-day scheduling is caused by `regular_interval` without an interval, **it is Olu's pattern too**, not purely our invention. The differing dates *between views* look like a genuine display bug regardless of config. **§7.4 settles this, and it decides whether the item stays in the Olu email.**

### Already ruled out — do not re-test the NOT_FOUND cause
- **Not** a Stripe minimum-charge issue (tested $0.33 and $0.99 — both failed identically).
- **Not** `autoInvoice` or `paymentScheduleConfig` (a bare estimate with neither still failed).
- **Not** the dollar amount ($1, $2, $3, $1,720 all failed identically pre-fix).
- **Not** a Stripe-connection problem. The custom-payment-provider endpoint returns empty **even when native Stripe Connect is properly configured** — it only reflects marketplace apps. Jay's Stripe **is** connected and current.

---

## 7. ACTION QUEUE — execute in order

### 7.1 Rename the mislabeled user ⚡ **JAY APPROVED**
`l4pvaiiMabQk6iZDnBeF` — **Jacob Mora → Jay Mora**. Email stays `office@propertyrenovatorsgroup.com`; role stays Admin.

Use the `users` domain (`PUT /users/{userId}`). **Read the record first** — assume wholesale-replace semantics (§8).
*UI fallback:* app.gohighlevel.com → Settings → My Staff → that user → Edit → Save.

### 7.2 Delete two stale estimates ⚡ **JAY APPROVED**
Both advertise the pre-port `+12406726135`:
- **#4** — `6a6500babff9c219e1d8998c` — "SUPERSEDED - See HCP #825", Diane Christen, $1,660
- **#5** — `6a6500c9abdda9d2703c0668` — "SUPERSEDED - See HCP #825", Diane Christen, $2,360

```
DELETE /invoices/estimate/{id}
body: {"altId": "w6brLF0sqjGJVPR5N4Pa", "altType": "location"}
```

### 7.3 Confirm the user roster — **highest-value unknown**
`GET /users/search?locationId=w6brLF0sqjGJVPR5N4Pa`

Determine whether **one or two** Jay identities exist (`oxyt…` on jay@thejaymora.com vs `l4pv…` on office@). Capture each user's **role** and **notification settings**.

**Why it matters:** GHL routes notifications to the **assigned user**. Jay's contact is `assignedTo: oxyt…`, but Jay logs in as office@ (`l4pv…`). If those are separate accounts, notifications may fire toward an identity he isn't watching — which directly drives his "notify me and Jacob every time" requirement. **It also decides whether item 5 stays in the Olu email.**

### 7.4 Read INV-000009 — settles the attribution
`GET /invoices/?altId=w6brLF0sqjGJVPR5N4Pa&altType=location` → find INV-000009 (generated from #33).

Inspect the raw payment schedule and due dates. Compare against the §6 config block. Determine whether same-day scheduling comes from `scheduleDateType: "regular_interval"` with no interval, and whether the cross-view date discrepancy is a display bug. **This decides whether the item stays in the Olu email.**

Also check `GET /invoices/schedule` for any schedule object.

### 7.5 Check the Opportunity
`GET /opportunities/search?contactId=sBNxkJ7k9a2Y1MFhOStp` (note: **no** `location_id` param — it 422s; the connection supplies the location).

Did accepting #33 create or move an Opportunity in `hT378d5OfgZIag9MIkMw`? Expected: **no** (workflow unpublished). Confirming against a real acceptance is fresh evidence for item 6.

### 7.6 Verify location config and sweep for the old number
Confirm the business profile phone is `+13013953831` and inspect the logo asset. Then sweep for `2406726135` hardcoded anywhere: the six published workflows, SMS/email templates, calendar notifications, the five forms, and the website.

### 7.7 Then — Jacob's account (after 7.1 and 7.3)
Create a GHL user for **jacobhandymanservices@gmail.com** at **User role, NOT Admin**.

Order matters: rename first so you don't create two "Jacob Mora" records; resolve the duplicate identity first so assignments point at the right user.

**Recommended structure** (already discussed with Jay): one Admin/Owner (Jay, office@), Jacob as restricted User on his own email, and optionally a **service account** holding API tokens so integrations don't break when a human account is disabled. Never share one login — it destroys per-person attribution on customer replies and breaks notification routing.

### 7.8 Then — the both-of-you notification workflow
Jay's requirement: he **and** Jacob notified on **every** inbound text/email.

**The trap:** GHL's default routes notifications to the *assigned user* only. Enabling both users' notification preferences does **not** fix an unassigned or singly-assigned contact.

**The fix:** a workflow — trigger on inbound message (Customer Replied / Inbound SMS / Email Received) → **Internal Notification** action addressed **explicitly to both users**, email + SMS. Fires regardless of assignment. Then per-user notification prefs and LeadConnector mobile push as the second layer.

Jay was advised he may want to narrow Jacob's scope later (alert fatigue); he asked for everything for now.

### 7.9 Finally — cleanup and the Olu email
Delete remaining test records (§10), then revise `olu-followup-email-draft.md` per §7.3/§7.4 findings and present it to Jay. **Do not send.**

---

## 8. GHL API gotchas — hard-won, do not relearn

| # | Gotcha |
|---|---|
| 1 | **`PUT /invoices/estimate/{id}` wholesale-replaces.** Omitting `termsNotes` nulled it. **Always send the full object.** |
| 2 | **Contact upsert wholesale-replaces the `tags` array.** This is exactly how Jay's real contact got damaged. Prefer `PUT /contacts/{id}` with only the fields you intend to change. |
| 3 | **`estimateStatus` is not writable.** `PUT` accepts it, returns 200, silently ignores it. |
| 4 | **Estimate `name` max 40 characters** — 422 otherwise. |
| 5 | **`paymentScheduleConfig.schedules[].value` accepts 4 decimals** (`33.3333`). Estimates carry `configuration.precision: 4`. |
| 6 | **`businessDetails.logoUrl` must be passed explicitly** on API-created estimates or the email renders `<img src="">`. UI-created estimates inherit it automatically. |
| 7 | **`POST /invoices/estimate/{id}/invoice` requires acceptance** — returns `400 estimate_not_accepted` otherwise. **There is no API path to accept an estimate**; acceptance is customer-side on the page only. |
| 8 | **Business details snapshot onto each estimate at creation** and never refresh. |
| 9 | **The custom-payment-provider endpoint is not a Stripe indicator** — empty even when native Stripe Connect works. Never cite it as evidence Stripe is disconnected. |
| 10 | **`DELETE` needs `{altId, altType}` in the body**, not just the path. |
| 11 | **`GET /opportunities/search` rejects `location_id`** — 422 "property location_id should not exist". |
| 12 | **`list-estimates` `status` filter validates against the enum** — a handy way to probe valid values (invalid → 422 "status must be a valid enum value"). |
| 13 | **Estimate emails wrap every link** through `email.mail.propertyrenovatorshomeservices.com/c/<zlib+base64url payload>`. To recover the real `link.fastpaydirect.com` URL, base64url-decode then zlib-decompress and read the `l=` param. Script pattern in §11. |

---

## 9. Operation ID reference (REI Unlock MCP registry)

Verified working during this session:

| Operation ID | Method / Path |
|---|---|
| `list-estimates` | GET `/invoices/estimate/list` |
| `create-new-estimate` | POST `/invoices/estimate` |
| `update-estimate` | PUT `/invoices/estimate/{estimateId}` |
| `delete-estimate` | DELETE `/invoices/estimate/{estimateId}` |
| `send-estimate` | POST `/invoices/estimate/{estimateId}/send` |
| `create-invoice-from-estimate` | POST `/invoices/estimate/{estimateId}/invoice` |
| `list-estimate-templates` | GET `/invoices/estimate/template` |
| `generate-estimate-number` | GET `/invoices/estimate/number/generate` |
| `invoices.list-invoices` | GET `/invoices/` |
| `create-invoice` / `update-invoice` / `send-invoice` | POST/PUT `/invoices/…` |
| `record-invoice` | POST `/invoices/{invoiceId}/record-payment` |
| `get-invoice-settings` | GET `/invoices/settings` |
| `list-invoice-schedules` | GET `/invoices/schedule` |
| `get-contact` | GET `/contacts/{contactId}` |
| `update-contact` | PUT `/contacts/{contactId}` |
| `search-contacts-advanced` | POST `/contacts/search` |
| `search-users` | GET `/users/search` |
| `get-user` | GET `/users/{userId}` |
| `get-pipelines` | GET `/opportunities/pipelines` |
| `search-opportunity` | GET `/opportunities/search` |
| `get-opportunity` | GET `/opportunities/{id}` |
| `get-workflow` | GET `/workflows/` |
| `list-documents-contracts-templates` | GET `/proposals/templates` |
| `list-documents-contracts` | GET `/proposals/document` |
| `products.list-invoices` | GET `/products/` |
| `list-prices-for-product` | GET `/products/{productId}/price` |
| `get-forms` | GET `/forms/` |
| `get-forms-submissions` | GET `/forms/submissions` |
| `get-businesses-by-location` | GET `/businesses/` |

Writes require an `idempotencyKey`. `send-estimate` requires `{altId, altType, action: "email", liveMode, userId}`; `userId` determines the `sentBy` stamp — previous sends used `oxyt1XjN5vSumXxcv1gq`.

---

## 10. Test data inventory

### Deleted (11) ✅
Estimates **#8, #9, #10, #11, #12, #13, #14, #15, #16, #17** (Jul 31 test set) and **#31** (a $1,720 decimal-probe draft). Linked test Opportunities were already gone — two spot-checked IDs returned `404 OPPORTUNITY_NOT_FOUND`.

### Live test records — delete after verification
| Record | ID | Status |
|---|---|---|
| Estimate #29 ($3, 33% deposit, no `dateConfig`) | `6a6fb23bfb5d32751633c49d` | sent, **not accepted** |
| Estimate #30 ($2, no deposit config) | `6a6fb250ebf585f65e9f5093` | sent, **not accepted** — **needed for §7 item 3** |
| Estimate #32 ($240, catalog product + logoUrl) | `6a6fb693ebf5855e239f8846` | sent, not accepted |
| Estimate #33 ($1,720, 33.3333/66.6667) | `6a70be4a100e15f4f8c2aa3b` | **ACCEPTED** — keep until §7.4 done |
| Invoice INV-000009 | from #33 | delete after §7.4 |

### ⚠️ Time-sensitive
**INV-000002** — `6a6cee34fb5d32bd8d06dcd6`, "TEST - Invoice Object Type Check", $3, sent, unpaid.
Has **overdue reminders scheduled Aug 4, Aug 7, Aug 15** (`reminderStatus: initiated`) that will email jay@thejaymora.com. **Delete or void it early.**

**INV-000005** — `6a6d143debf58508d675eca9`, "Deposit Invoice - Diane Christen", $573, **draft**, never sent. Keep if the Diane job proceeds; else delete. *(Note: $573 — hand-calculated as true 1/3 of $1,720, consistent with the 33.3333 finding.)*

### Not ours — leave alone
Estimates **#2** (`6a51341ac97dd0c4590bcde9`, Platform Test), **#27**, **#28** (Olu's samples); invoice **INV-000001** (paid $1 processor test).

### Data repair already done
Jay's contact `sBNxkJ7k9a2Y1MFhOStp` had `source` overwritten with "Internal Test - Estimate Flow QA" by a prior session, and `tags` wiped.
**`source` restored to "Send Us Your Photos"** — evidenced by `lastAttributionSource.mediumId = KNda9rEUYExpXdoWSIZd` (that form's ID) plus 13 submissions from this contact Jul 26–28.
**Unrecoverable:** the original `tags` array (currently empty). GHL exposes no public audit log. Ask Jay whether he recalls any.

---

## 11. Primary evidence that lives outside this repo

### Screenshots Jay supplied (not committed — described here so the evidence survives)
1. **INV-000009, web view** (`link.fastpaydirect.com`) — logo badge reading "PROPERTY RENOVATORS HANDYMAN SERVICES"; green **Pay $573.33** button; Payment 1 of 2 **$573.33** *Pending* due 8/2/2026; Payment 2 of 2 **$1,146.67** *Pending* due 8/2/2026; Amount Due (USD) **$1,720.00**; Invoice No **INV-000009**; Issue Date Aug 3 2026; Due Date Aug 4 2026.
2. **INV-000009, PDF/download view** — same figures, but installment due dates read **August 3, 2026**; footer "Generated on August 3, 2026 12:50 pm EDT".
3. **Safari on `email.mail.propertyrenovatorshomeservices.com`** — plain **"404 page not found"**, no certificate interstitial. (The SSL proof.)

### Gmail queries that surfaced key evidence
Jay's inbox (jay@thejaymora.com) is the system-email trail. Useful searches:
- `from:info@mail.propertyrenovatorshomeservices.com newer_than:1d`
- `subject:("Added to Sub-Account" OR "New User Added" OR "New Admin Added")` → the single user-provisioning record
- `from:olu@reiunlock.com OR from:reiunlock.com`
- `newer_than:1d (estimate OR invoice OR accepted OR payment)`

### Decoding an estimate link from an email
```python
import zlib, base64, urllib.parse, re
raw = open('message.html').read()
for m in re.finditer(r'/c/([A-Za-z0-9_\-]+)', raw):
    p = m.group(1)
    try:
        d = zlib.decompress(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4))).decode()
    except Exception:
        continue
    for kv in d.split("&"):
        if kv.startswith("l="):
            print(urllib.parse.unquote(kv[2:])); break
```

### Live test links (public — no login required)
- #29 — https://link.fastpaydirect.com/l/ZChj2CmUq
- #30 — https://link.fastpaydirect.com/l/HyN-L6UUS
- #32 — https://link.fastpaydirect.com/l/9e2tc3QbI
- #33 — https://link.fastpaydirect.com/l/zwLnnHLnx *(already accepted)*

---

## 12. The Olu email

Draft: **`olu-followup-email-draft.md`**. **NOT SENT.** Jay reviews before anything goes out.

Structure: five confirmed-working items (so Olu doesn't redo them) + six outstanding.

**Editorial decisions already made — revisit if new evidence lands:**
1. **The payment-schedule item is worded as a question, not a defect** — attribution unresolved. **§7.4 decides whether it stays.** Note the `dateConfig` came from Olu's own sample, which strengthens the case for keeping it.
2. **Old phone on #4/#5 excluded** — our cleanup, not his bug (§6).
3. **Blank logo excluded; wrong logo included** — the blank was our API payload omitting `logoUrl`; the Handyman asset is genuinely his.
4. **The user mislabel is worded as a correction, not a security accusation** — no unauthorized access occurred, since Jacob has no GHL login.

**§7.3 may shrink item 5:** if only one user exists, cut the duplicate-identity half so Jay isn't sending Olu after something imaginary.

---

## 13. Open questions

| # | Question | Resolution |
|---|---|---|
| 1 | One Jay identity or two? | §7.3 |
| 2 | Same-day installment due dates — ours, Olu's pattern, or a GHL default? | §7.4 |
| 3 | Did accepting #33 move any Opportunity? | §7.5 |
| 4 | Does the no-deposit flow request the full amount? | Accept #30 |
| 5 | Original tags on Jay's contact? | Ask Jay; likely unrecoverable |
| 6 | Is `2406726135` hardcoded in workflows/templates/forms? | §7.6 |
| 7 | Can a client select **any combination** of variant items, or only one package? | Blocked on Olu building variants |
| 8 | Who is `Flr5a7IZcuRyfyGCzLPK`? | §7.3 roster |

---

## 14. ⚠️ Security — action required

**Jacob's Gmail password was pasted into the previous chat session** (for `jacobhandymanservices@gmail.com`). It was never used, and it is **not** recorded in this repo or any committed file. **It must be rotated**, along with anywhere it's reused, and 2FA enabled. Jay was told; confirm it's done.

Going forward, account access should come from a connector approval or a scoped, revocable API token — never a password.

---

## 15. People

| Who | Role | Contact |
|---|---|---|
| **Jay Mora** | Owner, runs operations | office@propertyrenovatorsgroup.com (GHL login) · jay@thejaymora.com (personal/inbox used for all testing) |
| **Jacob Mora** | Jay's brother, field tech | jacobhandymanservices@gmail.com · cell 240-672-6135 · **no GHL account yet** |
| **Olu Laniyonu** | Agency contact, REI Unlock | olu@reiunlock.com · agency mailing address 11203 Lake Victoria Ln, Bowie, MD 20720 |

**Tone note:** Jay wants the Olu email complete, accurate, sent **once**, with no back-and-forth — and without blaming Olu for anything that turned out to be ours.

---

## 16. Definition of done

- [ ] 7.1 user renamed to Jay Mora
- [ ] 7.2 estimates #4 and #5 deleted
- [ ] 7.3 user roster confirmed; duplicate-identity question answered
- [ ] 7.4 INV-000009 schedule read; due-date attribution settled
- [ ] 7.5 Opportunity checked post-acceptance
- [ ] 7.6 location phone + logo verified; old number swept for
- [ ] #30 accepted; no-deposit flow confirmed
- [ ] INV-000002 deleted (stops the Aug 4/7/15 reminder emails)
- [ ] Remaining test records deleted (#29, #30, #32, #33, INV-000009)
- [ ] Jacob created as User-role account
- [ ] Both-of-you notification workflow built and tested
- [ ] Olu draft revised with final findings and **approved by Jay before sending**
- [ ] Jacob's Gmail password rotated
