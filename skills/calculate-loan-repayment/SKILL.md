# SKILL: Calculate Loan Repayment

## Trigger
User wants to understand monthly payments, total interest cost, or
compare two or more loan offers (bank, MFI, susu company, informal lender).

## Required Inputs (ask ONE at a time, in this order)
1. Principal amount (GHS)
2. Interest rate offered, AND whether it's described as "flat rate" or
   "reducing balance" — if the user doesn't know, ask them to read back
   exactly what the lender told them; explain the difference before
   proceeding
3. Loan term (in months)
4. (Optional) Repayment frequency — monthly, weekly, or daily (common
   for susu-linked microloans)

## Decision Logic
- If interest type is unclear or described only as "X% per month/year"
  with no method named, treat as FLAT RATE by default (most common in
  Ghanaian informal/microfinance lending) but flag this assumption to
  the user explicitly.
- Flat rate formula:
  Total Interest = Principal × Rate × Term
  Monthly Payment = (Principal + Total Interest) / Term
- Reducing balance formula: standard amortization —
  Monthly Payment = P × [r(1+r)^n] / [(1+r)^n - 1]
  where r = monthly rate, n = number of months
- Always calculate and show the EFFECTIVE ANNUAL RATE for flat-rate
  loans, since flat rate quoted rates understate true cost significantly
  compared to reducing balance.

## Steps
1. Confirm/clarify interest type before calculating anything.
2. Run the appropriate formula.
3. Present:
   - Monthly (or weekly/daily) payment amount
   - Total amount repaid over the loan term
   - Total interest paid
   - Effective annual rate (if flat rate)
4. If comparing multiple offers, build a side-by-side comparison table.
5. Flag clearly if total repayment exceeds 1.5x principal on a short-term
   loan — this is a signal worth double-checking, not an automatic red
   flag.

## Output Format
Short plain-language summary first (e.g., "You'll pay about GHS X per
month for Y months, totaling GHS Z — that's GHS [interest] in interest.")
followed by a simple table if term > 3 months.

## Guardrails
- Never recommend a specific lender or say "this is a good/bad deal" —
  present the numbers and let the user judge, though you may note if
  the effective rate looks unusually high compared to typical Tier 2/3
  microfinance rates.
- Always state this is a calculation aid, not financial advice.
- If the user's numbers seem to describe a loan-shark pattern (extremely
  short term, very high effective rate, daily compounding), calculate
  honestly but note the effective annual rate plainly so the user can
  see the real cost.
