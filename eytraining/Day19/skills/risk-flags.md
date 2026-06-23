# Contract Risk Flags Reference

This reference covers common risky clauses by category and severity. During a review pass, scan for each item and assess based on party posture and deal context.

---

## 🔴 HIGH RISK — Must Address

### Indemnification
- **Unlimited / uncapped indemnity** — any indemnity clause with no dollar cap or scope limit
  - Signal: "any and all claims", "all losses", no "arising from" qualifier
  - Fix: Limit to third-party claims arising from the indemnifying party's own acts/omissions; tie to liability cap

- **Mutual indemnity without symmetry** — one side has broader indemnity triggers than the other
  - Fix: Mirror the language; if you're the provider, limit to IP infringement and data breach

- **Indemnify for *any* IP claim** — often hidden in SaaS agreements for the customer side
  - Signal: "Customer shall indemnify Vendor for any claim that Customer's data infringes..."
  - Fix: Limit to claims arising from Customer's misuse; require Vendor to handle IP challenges to their own product

### Liability
- **No liability cap** — total liability is uncapped or expressed as "actual damages"
  - Fix: Cap at fees paid in the 12 months preceding the claim (standard); consider a separate cap for IP/confidentiality

- **Consequential damages not excluded for client** — standard exclusion should be mutual
  - Signal: "Neither party shall be liable for consequential damages" but carved out for one party's indemnity obligations
  - Fix: Ensure mutual exclusion; carve-outs should be narrow (fraud, willful misconduct, confidentiality breach, data breach)

- **Personal liability clause** — individual officer/employee liability, rarely acceptable in B2B
  - Fix: Remove entirely or limit to fraud

### Intellectual Property
- **Work-for-hire / IP assignment with no carveout** — vendor assigns all IP with no carveout for pre-existing IP or tools
  - Signal: "All work product... shall be the sole property of Customer"
  - Fix: Add carveout for pre-existing IP; grant Customer a license to use vendor's tools embedded in deliverables

- **Perpetual, irrevocable license to client data** — common in platform/SaaS agreements
  - Signal: "Customer grants Vendor a perpetual, worldwide, irrevocable license to Customer data..."
  - Fix: Limit to "term of agreement, solely to perform services"; delete perpetual/irrevocable

- **Ownership of derivative works** — who owns improvements, models trained on client data
  - Fix: Define clearly; if vendor trains models on client data, client should own any client-specific model output

### Termination
- **Termination for convenience only by one party** — asymmetric walk-away rights
  - Fix: Make mutual; or if asymmetric, require longer notice + transition assistance for the disadvantaged party

- **Auto-renewal with short cancellation window** — less than 60 days notice for multi-year agreements
  - Fix: Extend to 90 days; add explicit written notice requirement; add "failure to notify does not extend beyond X months"

- **No termination for cause / cure period** — no right to terminate for material breach
  - Fix: Add: "Either party may terminate for material breach with 30-day written notice and opportunity to cure"

### Data & Privacy
- **No data deletion obligation post-termination** — vendor retains client data indefinitely
  - Fix: Add 30-day deletion obligation; request certificate of deletion; backup retention cap of 90 days

- **Broad sublicense of data to affiliates / partners** — data can be shared without client consent
  - Fix: Limit to subprocessors needed to perform services; require prior written consent for new categories

- **No breach notification requirement** — or notification window longer than 72 hours
  - Fix: Require notification within 48-72 hours of discovery; specify point of contact

---

## 🟡 MEDIUM RISK — Negotiate If Possible

### Contract Structure
- **Evergreen auto-renewal without price lock** — price may increase on renewal
  - Fix: Lock pricing for renewal term, or require 90-day price-increase notice

- **Unilateral modification rights** — vendor can change terms on 30 days notice
  - Fix: Limit to non-material changes; require consent for material changes; add exit right if modified

- **Entire agreement clause missing** — allows prior representations to create liability
  - Fix: Add standard entire agreement / merger clause

### Financial
- **Late payment interest above 1.5% per month** — can compound quickly on disputed invoices
  - Fix: Cap at 1% per month / 12% per year; require prior written notice before applying

- **Invoice dispute process missing** — client can't freeze disputed amounts
  - Fix: Add "Client may withhold in good faith disputed amounts without breach, pending resolution"

- **No most-favored-customer clause** — especially relevant for enterprise multi-year deals
  - Note: If volume justifies, request MFN pricing protection

### Dispute Resolution
- **Mandatory arbitration with no class waiver opt-out** — can limit remedies
  - Fix: Ensure arbitration is optional OR mutual; confirm location/venue is neutral

- **Governing law in an unfavorable jurisdiction** — e.g., Delaware for IP disputes if client is in EU
  - Fix: Negotiate for mutual home state or neutral jurisdiction

- **Attorney fees shifting** — loser pays provision, can deter good-faith disputes
  - Fix: Remove or limit to frivolous claims

### Representations & Warranties
- **No warranty of fitness for purpose** — vendor disclaims all implied warranties
  - Fix: Ensure express warranty that services will perform materially in accordance with documentation

- **Disclaimer of all warranties including non-infringement** — leaves client exposed to IP risk
  - Fix: Retain non-infringement warranty; this is standard and vendor should carry it

---

## 🟢 LOW RISK — Standard / Accept As-Is

These are common, well-understood clauses that are generally acceptable without modification:

- Standard confidentiality with 2-5 year term (NDA context)
- Mutual non-solicitation of employees (12-24 month window)
- Assignment prohibition without consent (standard; carve out for M&A)
- Standard force majeure (pandemics, natural disasters, government action)
- Limitation of liability for free/trial services
- Usage data for product improvement (anonymized, aggregated)
- Notice provisions with email confirmation
- Severability clause
- Waiver clause (waiver of one breach does not waive future breaches)

---

## ✅ MISSING CLAUSE CHECKLIST

Check whether the following are present — if absent, consider adding:

| Clause | Why it matters |
|---|---|
| Data Processing Addendum (DPA) | Required for GDPR/CCPA compliance; governs data as processor |
| Business Associate Agreement (BAA) | Required if any PHI is processed (healthcare) |
| SLA / uptime commitment | Without it, no remedy for downtime |
| Change order process | Without it, scope creep has no pricing mechanism |
| Source code escrow | For critical software where vendor insolvency is a risk |
| Step-in rights | For regulated industries; right to step in if vendor fails |
| Insurance minimums | At minimum: commercial general liability, E&O, cyber liability |
| Audit rights | Right to audit vendor's compliance with privacy/security obligations |
| Transition assistance | Obligation to help with handoff at end of term |
| Non-disparagement | Mutual; prevents public disputes |
