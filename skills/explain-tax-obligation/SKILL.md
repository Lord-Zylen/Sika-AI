# SKILL: Explain Tax Obligation

## Trigger
User wants to know if/how they should be paying tax as an informal
trader, artisan, driver, or small business owner.

## Required Inputs (ask ONE at a time)
1. Nature of the business/work (trading, service, transport, etc.)
2. Rough annual income level (approximate range is fine)
3. Whether they are registered as a business or operating informally
4. Whether they have employees (affects PAYE obligations)

## Decision Logic (general guidance — verify current bands via RAG/live)
- Very small informal operators below certain income thresholds may
  qualify for simplified/presumptive tax arrangements designed for
  small-scale traders.
- Registered small businesses may fall under the VAT flat rate scheme
  if turnover crosses the applicable VAT registration threshold.
- Employers (even small ones) have PAYE withholding obligations for
  employees.
- Always retrieve current thresholds/rates via tool/RAG before stating
  specific cedi figures — these change with annual budget statements.

## Steps
1. Determine rough category (very small informal / growing small
   business / employer) from the inputs.
2. Explain which regime likely applies in plain terms, without stating
   specific rates unless confirmed via live/RAG retrieval.
3. Explain WHY registering can be beneficial long-term (access to
   credit, contracts requiring tax compliance, avoiding penalties)
   without being preachy.
4. Point to GRA (office, portal, or helpline) for definitive
   classification and registration.

## Guardrails
- Do not state specific tax rates or thresholds from memory as current
  fact — always flag if not freshly retrieved.
- Do not tell someone they "don't need to pay tax" — clarify obligation
  categories exist but final determination is GRA's, and encourage
  direct confirmation.
