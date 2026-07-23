# PolicyBot Conversation

**Session ID:** `dcc7f97d-5619-4bf0-8037-56d1b5771105`  
**Date:** 2026-07-01T09:50:42.536766+00:00  
**Turns:** 2  

---

## RAGAS — Conversation (HumanMessage / AIMessage)

HumanMessage(
    content="how many leaves"
),
AIMessage(
    content="The document states that confirmed employees are entitled to 18 days of Earned Leave, 12 days of Sick Leave, and 6 days of Casual Leave per year. Probationers receive pro-rated entitlements based on their joining date."
),
HumanMessage(
    content="hw to sick leave"
),
AIMessage(
    content="To take Sick Leave, employees should apply through the HRMS leave module. For sick leave of 3 or more consecutive days, a medical certificate from a registered practitioner is required, submitted within 7 days of return. Approval is given by the Reporting Manager and, if applicable, escalated to the Business Unit Head for leave of 5 days or more."
),

---

## Retrieved Contexts (last turn)

["iscouraged and may be declined by the Reporting Manager if business continuity is at risk. In such cases the employee will be requested to reschedule. Planning and Forecasting Each team is expected to maintain a leave plan for the calendar year by 31 January. The plan is a non-binding indicator that helps Reporting Managers plan around critical delivery milestones. Managers are expected to actively encourage team members to consume at least 10 days of EL during the year for rest and recovery. 4. Sick Leave (SL) Entitlement and Use Confirmed employees are entitled to 12 days of Sick Leave per calendar year. Sick Leave cannot be clubbed with Earned Leave or Casual Leave for vacation purposes. Sick Leave of 3 or more consecutive days requires a medical certificate from a registered medical practitioner, to be submitted within 7 days of return.", "e. Approval Workflow Approval workflow: Reporting Manager (first level) -> Business Unit Head (for EL of 5 days or more) -> HR for any clarifications. Sick Leave can be approved post-facto where prior notice was not possible.", "ment and is subject to applicable income tax provisions. Exclusions Encashment of Sick Leave and Casual Leave is not permitted under any circumstance. Employees terminated for misconduct may forfeit the right to encashment as part of the disciplinary outcome, at the sole discretion of HR. 8. Leave Application Procedure Where and How to Apply All leave must be applied through the HRMS leave module. Manual leave applications are accepted only when the HRMS is unavailable and must be regularised within 3 working days. An auto-generated email notification is sent to the Reporting Manager when a leave request is raised. Employees are responsible for verifying that the leave has been approved before commencing the absence. Approval Workflow Approval workflow: Reporting Manager (first level) -> Business Unit Head (for EL of 5 days or more) -> HR for any clarifications."]

---

## Ground Truth (last turn)

Employees must apply for Sick Leave through the HRMS leave module, and Sick Leave of 3 or more consecutive days requires a medical certificate from a registered medical practitioner, which must be submitted within 7 days of return; approval is granted by the Reporting Manager and can be post-facto if prior notice was not possible.

---

## DeepEval — ConversationalTestCase (multi-turn)

convo = ConversationalTestCase(
    turns=[
        Turn(role="user", content="how many leaves"),
        Turn(role="assistant",
             content="The document states that confirmed employees are entitled to 18 days of Earned Leave, 12 days of Sick Leave, and 6 days of Casual Leave per year. Probationers receive pro-rated entitlements based on their joining date.",
             retrieval_context=["nct purpose and the eligibility, accrual and approval rules differ across them. Employees are encouraged to read the relevant section before applying. Annual Entitlement Snapshot Annual entitlements for confirmed employees: 18 days Earned Leave, 12 days Sick Leave, and 6 days Casual Leave per calendar year. Probationers receive a pro-rated entitlement based on date of joining. Pro-ration for new joiners is computed on the basis of completed calendar months of service in the leave year. A fractional month of 15 days or more is treated as a completed month for accrual purposes. Treatment of Weekly Offs and Holidays Saturdays, Sundays and declared public holidays falling within a stretch of leave are not counted against the employee's leave balance, except where the rules of a specific leave category state otherwise.", "MERIDIAN TECHNOLOGIES PVT. LTD. CONFIDENTIAL Page 4 Prefixing or suffixing of weekly offs and holidays to leave is permitted subject to manager approval and the operational needs of the team. 3. Earned Leave (EL) Annual Entitlement Confirmed employees are entitled to 18 days of Earned Leave per calendar year, credited at the rate of 1.5 days per completed month of service. Probationers accrue EL at the same rate but cannot avail it until confirmation, except in special circumstances approved by HR. Crediting happens in advance on the first day of each calendar month. In the event of separation, any excess EL availed beyond the pro-rated entitlement is recovered from the final settlement. Carry Forward Unused Earned Leave may be carried forward to the next calendar year subject to a maximum accumulation of 30 days.", "the final settlement. Carry Forward Unused Earned Leave may be carried forward to the next calendar year subject to a maximum accumulation of 30 days. Any EL balance beyond 30 days as on 31 December will lapse automatically unless encashed during the encashment window. The carry forward limit is intended to encourage employees to take adequate time off for rest and personal commitments while still preserving a reasonable reserve. Minimum and Maximum Block Minimum EL that can be availed at a stretch is 0.5 day (half day). Maximum continuous EL is 15 working days; longer durations require Business Unit Head approval. EL must be applied at least 7 calendar days in advance for durations of 3 days or more. Last minute EL is discouraged and may be declined by the Reporting Manager if business continuity is at risk. In such cases the employee will be requested to reschedule."]),
        Turn(role="user", content="hw to sick leave"),
        Turn(role="assistant",
             content="To take Sick Leave, employees should apply through the HRMS leave module. For sick leave of 3 or more consecutive days, a medical certificate from a registered practitioner is required, submitted within 7 days of return. Approval is given by the Reporting Manager and, if applicable, escalated to the Business Unit Head for leave of 5 days or more.",
             retrieval_context=["iscouraged and may be declined by the Reporting Manager if business continuity is at risk. In such cases the employee will be requested to reschedule. Planning and Forecasting Each team is expected to maintain a leave plan for the calendar year by 31 January. The plan is a non-binding indicator that helps Reporting Managers plan around critical delivery milestones. Managers are expected to actively encourage team members to consume at least 10 days of EL during the year for rest and recovery. 4. Sick Leave (SL) Entitlement and Use Confirmed employees are entitled to 12 days of Sick Leave per calendar year. Sick Leave cannot be clubbed with Earned Leave or Casual Leave for vacation purposes. Sick Leave of 3 or more consecutive days requires a medical certificate from a registered medical practitioner, to be submitted within 7 days of return.", "e. Approval Workflow Approval workflow: Reporting Manager (first level) -> Business Unit Head (for EL of 5 days or more) -> HR for any clarifications. Sick Leave can be approved post-facto where prior notice was not possible.", "ment and is subject to applicable income tax provisions. Exclusions Encashment of Sick Leave and Casual Leave is not permitted under any circumstance. Employees terminated for misconduct may forfeit the right to encashment as part of the disciplinary outcome, at the sole discretion of HR. 8. Leave Application Procedure Where and How to Apply All leave must be applied through the HRMS leave module. Manual leave applications are accepted only when the HRMS is unavailable and must be regularised within 3 working days. An auto-generated email notification is sent to the Reporting Manager when a leave request is raised. Employees are responsible for verifying that the leave has been approved before commencing the absence. Approval Workflow Approval workflow: Reporting Manager (first level) -> Business Unit Head (for EL of 5 days or more) -> HR for any clarifications."]),
    ],
)

---

*Exported for RAGAS / DeepEval evaluation*