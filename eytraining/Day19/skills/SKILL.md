---
name: legal-contract-review
description: >
  Comprehensive legal contract review, redlining, and drafting for law firms and in-house legal teams.
  Use this skill whenever asked to: review a contract, redline a clause, spot risky provisions,
  draft or revise any legal agreement (NDA, MSA, SLA, vendor contract, employment agreement,
  IP assignment, licensing agreement), explain contract language in plain English, or compare
  contract versions. Triggers on: contract, NDA, MSA, SLA, agreement, clause, redline, legal review,
  indemnification, liability cap, IP ownership, governing law, arbitration, breach, cure period,
  termination for cause, force majeure, SOW, vendor agreement, MNDA, CNDA.
---

# Legal Contract Review & Drafting

A skill for law firms and corporate legal teams to review, redline, and draft commercial contracts accurately and efficiently.

> **Read before acting:** load `references/risk-flags.md` whenever doing a risk review. Load the
> appropriate template from `references/templates/` when drafting from scratch.

---

## Scope

This skill handles:
- **Review & Risk Assessment** — flag, explain, and prioritize risky clauses
- **Redlining** — suggest revised language with tracked-change style markups
- **Plain-English Translation** — explain legalese to non-lawyer stakeholders
- **From-Scratch Drafting** — generate first drafts from templates + client facts
- **Version Comparison** — diff two contract versions and summarize what changed

---

## Workflow

### Step 1 — Identify the Task

Determine what the user needs:

| Request type | Key signal phrases | Action |
|---|---|---|
| Risk review | "review this", "flag issues", "what should I watch out for" | Run full risk pass (see below) |
| Redline | "redline this", "mark up", "revise clause X" | Inline markup with `[REDLINE]` tags |
| Draft | "draft an NDA", "write a vendor agreement" | Load template, gather facts, generate |
| Translate | "what does this mean", "explain in plain English" | Paraphrase + implications |
| Compare | "what changed", "diff these two" | Side-by-side delta summary |

If the request is ambiguous, ask one clarifying question: **"Are you looking to review this for risks, revise specific clauses, or draft something from scratch?"**

---

### Step 2 — Gather Context (for drafting or targeted review)

Before reviewing or drafting, confirm:

1. **Party roles** — Who is the client? (disclosing vs. receiving party, service provider vs. customer, licensor vs. licensee)
2. **Deal type** — What is the underlying transaction?
3. **Client posture** — Is the client providing or receiving this contract? (affects which terms favor them)
4. **Jurisdiction** — Governing law state/country
5. **Deal size / risk appetite** — Enterprise SaaS vs. one-off consulting changes what matters

Pull any of the above from the contract text itself before asking.

---

### Step 3 — Risk Review Pass

Load `references/risk-flags.md` and scan the contract for all flagged clause types.

**Output format — Risk Summary Card:**
```
## Contract Risk Summary
**Document:** [contract name/type]
**Reviewed for:** [party name]
**Date:** [today]

### 🔴 High Risk (must address before signing)
1. **[Clause name]** (§X.X) — [one-sentence issue] → [recommended fix]

### 🟡 Medium Risk (negotiate if possible)
1. **[Clause name]** (§X.X) — [one-sentence issue] → [recommended fix]

### 🟢 Low Risk / Standard (note only)
- [Clause name]: standard, acceptable as-is

### ✅ Missing Clauses (consider adding)
- [Clause] — reason it matters for this deal type
```

Always state *why* something is risky for **this specific party**, not just that it's unusual.

---

### Step 4 — Redlining

Use this markup convention (compatible with Word comments workflow):

```
ORIGINAL:  "Vendor shall indemnify Customer for any and all claims..."
REDLINE:   "Vendor shall indemnify Customer for third-party claims arising
            directly from Vendor's gross negligence or willful misconduct..."
REASON:    Narrows unlimited indemnity to fault-based; removes strict liability exposure.
```

For multi-clause redlines, number each `[REDLINE-1]`, `[REDLINE-2]`, etc. and provide a cover note summarizing the overall negotiating strategy.

---

### Step 5 — Drafting from Template

1. Load the relevant template from `references/templates/`
2. Fill in party names, deal-specific terms, and jurisdiction
3. Highlight every `[PLACEHOLDER]` that still needs client input
4. Present the draft with a brief cover memo noting key choices made and alternatives available

---

### Step 6 — Plain-English Summary

Structure as:
- **What this contract does** (2-3 sentences)
- **Your key obligations** (bullet list)
- **Their key obligations** (bullet list)
- **What happens if something goes wrong** (termination, liability, dispute resolution)
- **Watch out for** (top 2-3 issues in plain language)

---

## Output Standards

- **Always cite section numbers** when flagging issues
- **Always state impact** ("this means you could be liable for...") not just the legal issue
- **Never give final legal advice** — frame as "this should be reviewed with counsel before signing" for high-stakes items
- **Use the client's perspective** throughout — "you" = the client the review is for
- **Track confidence** — if a clause is jurisdiction-specific or unusual, flag "jurisdiction-dependent" or "confirm with local counsel"

---

## Reference Files

| File | When to load |
|---|---|
| `references/risk-flags.md` | Every risk review pass |
| `references/clause-library.md` | When drafting redline language or standard alternatives |
| `references/templates/nda.md` | Drafting a new NDA from scratch |
| `references/templates/msa.md` | Drafting a Master Services Agreement |

---

## Quick Checklist — Before Returning Output

- [ ] Did I read the document from the client's perspective?
- [ ] Did I cite section numbers for all flagged issues?
- [ ] Did I explain *why* each risk matters in business terms?
- [ ] Did I suggest concrete fix language, not just flag the problem?
- [ ] Did I note any jurisdiction-specific issues?
- [ ] Did I include a "missing clauses" check?
