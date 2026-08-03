# DRAFT — follow-up to Olu (NOT SENT)

Reviewed by Jay before sending. Every claim below is backed by evidence in
`ghl-verification-report-2026-08-02.md`.

---

**Subject:** Property Renovators GHL — verified results and what's still open

Hi Olu,

I went through the Estimates/Invoices system end to end after your fix and tested each piece directly rather than assuming. Wanted to send you one consolidated list so nothing bounces back and forth.

**Confirmed working — no action needed on these:**

1. **Estimate links resolve.** The NOT_FOUND issue is gone. Verified on multiple estimates including brand-new ones created from scratch, and I accepted a live estimate successfully.
2. **Sending domain is live.** Estimate and invoice emails now come from info@mail.propertyrenovatorshomeservices.com, including system notifications.
3. **SSL on email.mail.propertyrenovatorshomeservices.com is valid.** The certificate error I hit earlier is resolved — verified in a browser today.
4. **Auto-invoice on acceptance works.** Accepting an estimate generated and sent the invoice within about three seconds, followed by the payment-schedule notice.
5. **Deposit math is accurate to the cent.** Using 33.3333 / 66.6667 on a $1,720 job produced $573.33 and $1,146.67. We'll use that going forward.

**Still open — these are what I need from you:**

1. **Wrong logo on the location.** Estimates and invoices render a logo reading "Property Renovators **Handyman** Services." It should be **Property Renovators Home Services**. The asset stored on the location is the Handyman one, so it appears on every document that shows a logo. Please replace it with the correct Home Services logo.

2. **Variants on the estimate template.** The only proposal template ("Property Renovators - Estimate") hasn't been modified since July 11 and has no variants configured. Two things here: please set them up, and confirm definitively whether a client can check **any combination** of line items or only select **one package** out of several. That distinction changes how we build estimates.

3. **Deposit-paid → Opportunity workflow.** There's no published workflow for this — only unpublished drafts with auto-generated names. Please finish and **publish** it: when a deposit invoice is paid, move the linked Opportunity in the "Property Renovators Jobs" pipeline to **"Approved / Booked."** Let me know when it's live and I'll run a real test.

4. **Notification email templates are all blank.** In the invoice settings, every template (customerSendEstimate, customerSendInvoice, customerPaymentSuccess, teamEstimateAccepted, and the rest) has an empty emailTemplate value, unchanged since July 24. GHL's system default is rendering instead. If custom branded templates were part of the build, that hasn't happened yet.

5. **User account is mislabeled, and there may be a duplicate.** The Sub-Account Admin created July 24 on **office@propertyrenovatorsgroup.com** is labeled **"Jacob Mora."** That's my login — it should read **Jay Mora**. Please correct it.
   Separately, there appears to be a second user tied to **jay@thejaymora.com** that also acts in the account (it owns contact assignments and sends estimates). Please confirm whether that's a duplicate of me, and which identity should own contact assignments going forward. I want notifications routing to one place before we add my brother Jacob as his own restricted user.

6. **One to check on the payment schedule.** On the invoice generated from an accepted estimate, both installments came through with the same due date, and the invoice showed the full job total as "Amount Due" rather than the deposit. I also saw three different due dates for the same invoice across the web view, the PDF, and the invoice header. Some of that may be my own schedule configuration — but the differing dates between views look like a display issue. Can you take a look?

For context on how we'll use this: deposit at acceptance, balance due at job completion — so the second installment shouldn't be due the same day as the first.

Thanks,
Jay

---

## Notes for Jay before sending

- **Item 6 is the one soft spot.** The same-day due dates may come from my test's `dateConfig` rather than a GHL defect. I've worded it as a question, not an accusation. If you'd rather not raise it until I confirm against the raw config, delete item 6 — everything else is solid.
- **Deliberately left off:** estimates #4 and #5 carrying the old 240-672-6135 number. That's our cleanup, not Olu's bug — GHL froze the business details onto those two documents. Deleting them resolves it.
- **Also left off:** the blank logo in earlier emails. That was caused by our own API payloads omitting `logoUrl`, not by Olu. The *wrong* logo (item 1) is genuinely his.
- Item 5 is worded as a correction, not an accusation — no unauthorized access occurred, since Jacob has no GHL login at all.
