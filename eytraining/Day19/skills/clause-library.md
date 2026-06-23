# Clause Library — Standard Language Reference

Use this library to generate redline suggestions and draft standard provisions.
Customize the `[PARTY_A]`, `[PARTY_B]`, `[N]`, and other placeholders for the specific contract.

---

## Liability & Indemnification

### Mutual Liability Cap (Standard B2B)
```
Limitation of Liability. IN NO EVENT SHALL EITHER PARTY'S AGGREGATE LIABILITY TO THE OTHER PARTY
ARISING OUT OF OR RELATED TO THIS AGREEMENT EXCEED THE TOTAL FEES PAID OR PAYABLE BY [PARTY_B]
TO [PARTY_A] IN THE [TWELVE (12)] MONTHS IMMEDIATELY PRECEDING THE CLAIM. THIS LIMITATION APPLIES
REGARDLESS OF THE FORM OF ACTION AND WHETHER SUCH LIABILITY ARISES FROM CONTRACT, TORT
(INCLUDING NEGLIGENCE), STRICT LIABILITY, OR OTHERWISE.
```

### Mutual Consequential Damages Exclusion (Standard)
```
Exclusion of Consequential Damages. IN NO EVENT SHALL EITHER PARTY BE LIABLE TO THE OTHER
FOR ANY INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE, OR CONSEQUENTIAL DAMAGES, OR
DAMAGES FOR LOSS OF PROFITS, REVENUE, BUSINESS, SAVINGS, DATA, USE, OR GOODWILL, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

Exceptions. The exclusions in the preceding paragraph shall not apply to: (i) either party's
indemnification obligations for third-party IP infringement claims; (ii) breaches of
confidentiality obligations; (iii) a party's fraud or willful misconduct; or
(iv) Customer's payment obligations.
```

### Balanced Vendor Indemnification (Provider-Favorable)
```
Indemnification by [VENDOR]. [VENDOR] shall defend, indemnify, and hold harmless [CUSTOMER]
and its officers, directors, and employees ("Customer Indemnitees") from and against any
third-party claim, suit, or proceeding alleging that the Services, as provided by [VENDOR]
and used in accordance with this Agreement, infringe or misappropriate any third-party
intellectual property right. [VENDOR]'s obligations under this Section are conditioned upon:
(a) Customer promptly notifying [VENDOR] of the claim in writing; (b) Customer granting
[VENDOR] sole control of the defense and settlement; and (c) Customer providing reasonable
cooperation. [VENDOR] shall have no obligation for claims arising from: (i) Customer's
modification of the Services; (ii) combination with third-party products not provided by
[VENDOR]; or (iii) Customer's continued use after [VENDOR] provides a non-infringing alternative.
```

---

## Intellectual Property

### IP Ownership — Services with Deliverables (Balanced)
```
Ownership of Work Product. Subject to [VENDOR]'s rights in [VENDOR] IP (as defined below),
all work product, deliverables, and materials created by [VENDOR] specifically for [CUSTOMER]
pursuant to a Statement of Work ("Work Product") shall be owned by [CUSTOMER] upon full
payment of applicable fees. [VENDOR] hereby assigns to [CUSTOMER] all right, title, and
interest in and to such Work Product.

[VENDOR] IP. [CUSTOMER] acknowledges that [VENDOR] IP includes (i) [VENDOR]'s pre-existing
tools, methodologies, frameworks, and know-how ("Pre-existing IP"), and (ii) improvements
to Pre-existing IP created during the performance of Services ("Improvements"). [VENDOR]
retains all ownership of [VENDOR] IP. To the extent Work Product incorporates [VENDOR] IP,
[VENDOR] grants [CUSTOMER] a non-exclusive, perpetual, royalty-free license to use [VENDOR] IP
solely as embedded in and necessary to use the Work Product.
```

### Customer Data License (Minimal / Privacy-Protective)
```
Customer Data. As between the parties, [CUSTOMER] retains all right, title, and interest in
and to Customer Data. [CUSTOMER] grants [VENDOR] a limited, non-exclusive license to access
and use Customer Data solely during the Term and solely to the extent necessary to provide
the Services. [VENDOR] shall not: (i) disclose Customer Data to third parties except as
required to provide the Services; (ii) use Customer Data for any purpose other than performing
the Services; or (iii) train, fine-tune, or improve any AI model using Customer Data without
[CUSTOMER]'s prior written consent. Upon termination, [VENDOR] shall delete all Customer Data
within [30] days and, upon request, certify such deletion in writing.
```

---

## Term & Termination

### Termination for Cause with Cure Period (Balanced)
```
Termination for Cause. Either party may terminate this Agreement immediately upon written
notice if the other party: (i) materially breaches this Agreement and fails to cure such
breach within [30] days after receiving written notice specifying the breach in reasonable
detail; (ii) becomes insolvent, makes a general assignment for the benefit of creditors, or
becomes subject to bankruptcy or receivership proceedings; or (iii) ceases to conduct business
in the ordinary course.
```

### Termination for Convenience (Mutual)
```
Termination for Convenience. Either party may terminate this Agreement for any reason upon
[90] days' prior written notice to the other party. In the event of termination for
convenience by [CUSTOMER], [CUSTOMER] shall pay [VENDOR] for all Services performed and
expenses incurred through the effective date of termination. [VENDOR] shall promptly
deliver to [CUSTOMER] all completed and in-progress Work Product as of the termination date.
```

### Transition Assistance
```
Transition Assistance. Upon expiration or termination of this Agreement for any reason,
[VENDOR] shall, upon [CUSTOMER]'s request, provide reasonable transition assistance for a
period not to exceed [90] days ("Transition Period") at [VENDOR]'s then-current time-and-materials
rates. During the Transition Period, [VENDOR] shall: (i) continue to perform Services at
reduced scope as directed by [CUSTOMER]; (ii) provide reasonable access to documentation,
configurations, and data; and (iii) cooperate with [CUSTOMER] and any successor vendor to
ensure an orderly transition.
```

---

## Confidentiality

### Mutual NDA Clause (Balanced)
```
Confidentiality. Each party ("Receiving Party") agrees to: (i) hold the Disclosing Party's
Confidential Information in strict confidence using no less than the same degree of care it
uses to protect its own confidential information, but in no event less than reasonable care;
(ii) use Confidential Information solely for the purposes of this Agreement; and (iii) not
disclose Confidential Information to third parties except to employees, contractors, and
advisors with a need to know who are bound by confidentiality obligations at least as
protective as those herein.

Exceptions. Confidentiality obligations do not apply to information that: (a) is or becomes
publicly known through no fault of the Receiving Party; (b) was rightfully known before
disclosure; (c) is independently developed without reference to the Disclosing Party's
information; or (d) is required to be disclosed by law or court order, provided that the
Receiving Party gives prompt prior written notice and cooperates with the Disclosing Party's
efforts to seek a protective order.

Term. Confidentiality obligations survive termination of this Agreement for [3] years;
provided that obligations with respect to trade secrets shall survive indefinitely.
```

---

## Data & Privacy

### Data Processing Addendum Reference Clause
```
Data Processing. To the extent [VENDOR] processes Personal Data (as defined in applicable
privacy laws) on behalf of [CUSTOMER] in performing the Services, the parties agree to
execute a Data Processing Addendum ("DPA") in a form consistent with applicable data protection
laws, including the GDPR and CCPA. In the event of any conflict between this Agreement and
the DPA with respect to the processing of Personal Data, the DPA shall control.
```

### Security Standards Obligation
```
Security. [VENDOR] shall implement and maintain commercially reasonable administrative,
technical, and physical safeguards designed to protect the security, confidentiality, and
integrity of Customer Data, including: (i) encryption of Customer Data at rest and in transit;
(ii) access controls limiting access to Customer Data to authorized personnel; and (iii) a
written information security program aligned with [ISO 27001 / SOC 2 Type II / NIST CSF].
[VENDOR] shall notify [CUSTOMER] of any confirmed or suspected unauthorized access to
Customer Data within [48] hours of discovery.
```

---

## Dispute Resolution

### Tiered Dispute Resolution (Negotiation → Mediation → Arbitration)
```
Dispute Resolution.

Step 1 — Escalation. The parties shall first attempt to resolve any dispute through good-faith
negotiation between senior representatives of each party for a period of [15] business days
following written notice of the dispute.

Step 2 — Mediation. If the dispute is not resolved through negotiation, either party may
submit the dispute to non-binding mediation administered by [JAMS / AAA] in [CITY, STATE].
The parties shall equally share the mediator's fees.

Step 3 — Arbitration. If the dispute is not resolved through mediation within [45] days
of the first mediation session, either party may submit the dispute to binding arbitration
administered by [JAMS / AAA] in accordance with its Commercial Arbitration Rules. The
arbitration shall be conducted by a single arbitrator in [CITY, STATE]. The arbitrator's
decision shall be final and binding and may be entered as a judgment in any court of
competent jurisdiction.

Injunctive Relief. Notwithstanding the foregoing, either party may seek emergency injunctive
relief in any court of competent jurisdiction to prevent irreparable harm.
```

---

## General / Boilerplate

### Assignment (Standard with M&A Carveout)
```
Assignment. Neither party may assign this Agreement or any rights hereunder without the other
party's prior written consent, which shall not be unreasonably withheld. Notwithstanding the
foregoing, either party may assign this Agreement without consent in connection with a merger,
acquisition, or sale of all or substantially all of its assets, provided that (i) the assignee
assumes all obligations hereunder in writing, and (ii) such assignment does not result in a
material reduction in the services or capabilities available to [CUSTOMER]. Any purported
assignment in violation of this Section shall be void. This Agreement shall be binding upon
and inure to the benefit of the parties' permitted successors and assigns.
```

### Entire Agreement / Integration
```
Entire Agreement. This Agreement, together with all Exhibits, Statements of Work, and Order
Forms incorporated herein, constitutes the entire agreement between the parties with respect
to its subject matter and supersedes all prior and contemporaneous agreements, representations,
warranties, and understandings, whether oral or written. No amendment to this Agreement shall
be effective unless made in writing and signed by authorized representatives of both parties.
The parties agree that any term or condition stated in a purchase order or similar instrument
issued by either party shall be null and void.
```
