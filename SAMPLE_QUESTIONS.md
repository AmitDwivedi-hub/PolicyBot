# PolicyBot — Sample Questions

A set of example questions you can ask PolicyBot, grouped by policy area. Each
question maps to one of the 10 policy documents in `knowledge_base/`.

> **Reminder for the workshop:** PolicyBot intentionally injects flawed answers
> roughly 40% of the time (wrong numbers, missing clauses, wrong approvers, or
> hallucinated details). Treat every answer as something to verify against the
> source document shown under **"Show retrieved documents."**

---

## HR — Leave Policy
- How many earned leaves do I get per year?
- How many earned leaves can I carry forward to the next year?
- What is the notice period for applying for planned leave?
- How many sick leaves am I entitled to, and do they need a medical certificate?
- What is the maternity leave entitlement?
- Is paternity leave available, and for how many days?
- Can I encash unused earned leave, and what is the limit?

## HR — Medical Insurance Policy
- What is the medical insurance coverage amount for an employee?
- Are my dependents (spouse, children, parents) covered under the policy?
- How do I add a newborn or new spouse to my insurance?
- What is the claim process for a cashless hospitalization?
- Is there a waiting period for pre-existing conditions?

## HR — Travel Reimbursement Policy
- What is the per-day meal allowance during domestic travel?
- What class of flight am I eligible for on international travel?
- What is the hotel stay limit per night for a metro city?
- How soon must I submit travel reimbursement claims after a trip?
- Who approves my travel request before booking?

## HR — Code of Conduct
- What is the policy on accepting gifts from vendors?
- How do I report a conflict of interest?
- What is the company's stance on workplace harassment?
- Can I do freelance or external consulting work while employed?
- What is the dress code policy?

## Finance — Expense Reimbursement Policy
- What expenses are eligible for reimbursement?
- What is the maximum amount I can claim without a receipt?
- How long does reimbursement take after submission?
- Who needs to approve expense claims above a certain amount?
- Are client-entertainment expenses reimbursable?

## Finance — Procurement Policy
- What is the approval limit for a manager to raise a purchase order?
- How many vendor quotes are required for a high-value purchase?
- What is the process for onboarding a new vendor?
- Who signs off on capital expenditure purchases?

## IT — Acceptable Use Policy
- Can I use my work laptop for personal tasks?
- Is personal use of company email allowed?
- What software am I allowed to install on my work machine?
- What is the policy on using public Wi-Fi for work?
- Are USB drives permitted on company devices?

## IT — Data Security Policy
- How should I handle confidential customer data?
- What is the password policy for company accounts?
- What do I do if I suspect a data breach or phishing attempt?
- Is it allowed to store work files on personal cloud storage?
- How often must I change my password?

## Work From Home / Remote Work Policy
- How many days per week can I work from home?
- What equipment does the company provide for remote work?
- Do I need approval to work remotely from a different city?
- What are the core working hours for remote employees?
- Is there an internet/utility allowance for working from home?

## Performance Management Policy
- How often are performance reviews conducted?
- What rating scale is used in appraisals?
- Who sets my annual performance goals?
- What is the process if I disagree with my performance rating?
- How does the promotion cycle work?

---

## Multi-turn / follow-up examples
PolicyBot keeps conversation context within a session, so you can ask follow-ups:

1. "How many earned leaves do I get per year?"
   - then: "And how many of those can I carry forward?"
2. "What is the per-day meal allowance for domestic travel?"
   - then: "What about international travel?"
3. "Can I work from home?"
   - then: "How many days per week?"

## Edge / stress-test questions (good for spotting hallucinations)
- What is the policy on sabbatical leave? *(may not exist — watch for invented details)*
- How many pet-care days am I allowed? *(not a real policy — a correct answer should say so)*
- What is the reimbursement rate for personal car mileage on a Sunday?
