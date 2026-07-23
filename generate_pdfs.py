"""Generates all 10 Meridian Technologies policy PDFs into knowledge_base/.

Run directly:  python generate_pdfs.py
"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "knowledge_base"
COMPANY = "MERIDIAN TECHNOLOGIES PVT. LTD."

styles = getSampleStyleSheet()
H_STYLE = ParagraphStyle("H", parent=styles["Heading1"], fontSize=16, textColor=colors.HexColor("#1f3864"), spaceAfter=14)
SH_STYLE = ParagraphStyle("SH", parent=styles["Heading2"], fontSize=13, textColor=colors.HexColor("#2e5597"), spaceAfter=8)
SSH_STYLE = ParagraphStyle("SSH", parent=styles["Heading3"], fontSize=11, textColor=colors.HexColor("#404040"), spaceAfter=6)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=6)
CENTERED = ParagraphStyle("C", parent=styles["BodyText"], fontSize=10, alignment=TA_CENTER, spaceAfter=4)
CONFIDENTIAL = ParagraphStyle("CONF", parent=styles["BodyText"], fontSize=8, textColor=colors.red, alignment=TA_CENTER)


def _header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(colors.HexColor("#1f3864"))
    canvas.drawString(2 * cm, 28 * cm, COMPANY)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.red)
    canvas.drawRightString(19 * cm, 28 * cm, "CONFIDENTIAL")
    canvas.setStrokeColor(colors.HexColor("#1f3864"))
    canvas.line(2 * cm, 27.8 * cm, 19 * cm, 27.8 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(10.5 * cm, 1.5 * cm, f"Page {doc.page}")
    canvas.restoreState()


def _title_block(title, doc_id, version, effective):
    return [
        Paragraph(COMPANY, CENTERED),
        Paragraph("Internal Policy Document", CENTERED),
        Spacer(1, 0.4 * cm),
        Paragraph(f"<b>{title}</b>", H_STYLE),
        Spacer(1, 0.2 * cm),
        Paragraph(f"<b>Document Number:</b> {doc_id}  |  <b>Version:</b> {version}  |  <b>Effective Date:</b> {effective}", BODY),
        Paragraph("<b>Classification:</b> Internal / Confidential", BODY),
        Paragraph("This document is the property of Meridian Technologies Pvt. Ltd. Unauthorized reproduction is prohibited.", BODY),
        Spacer(1, 0.6 * cm),
    ]


def _toc(items):
    rows = [["Section", "Title"]]
    for i, t in enumerate(items, 1):
        rows.append([str(i), t])
    t = Table(rows, colWidths=[2 * cm, 14 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f3864")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4fa")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return [Paragraph("<b>Table of Contents</b>", SH_STYLE), Spacer(1, 0.2 * cm), t]


def _section(num, title, paragraphs):
    out = [Paragraph(f"{num}. {title}", SH_STYLE)]
    for p in paragraphs:
        if isinstance(p, tuple):
            sub_title, sub_body = p
            out.append(Paragraph(f"<b>{sub_title}</b>", SSH_STYLE))
            for line in sub_body:
                out.append(Paragraph(line, BODY))
        else:
            out.append(Paragraph(p, BODY))
    out.append(Spacer(1, 0.3 * cm))
    return out


def _build(filename, title, doc_id, version, effective, toc_items, sections):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / filename
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2 * cm,
    )
    story = []
    story.extend(_title_block(title, doc_id, version, effective))
    story.append(PageBreak())
    story.extend(_toc(toc_items))
    story.append(PageBreak())
    for i, (sec_title, sec_content) in enumerate(sections, 1):
        story.extend(_section(i, sec_title, sec_content))
    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    print(f"  generated: {filename}")


def gen_leave_policy():
    toc = [
        "Introduction and Scope",
        "Types of Leave",
        "Earned Leave (EL)",
        "Sick Leave (SL)",
        "Casual Leave (CL)",
        "Maternity and Paternity Leave",
        "Leave Encashment",
        "Leave Application Procedure",
        "Leave Without Pay",
        "Holiday Calendar and Special Leave",
    ]
    sections = [
        ("Introduction and Scope", [
            ("Purpose of the Policy", [
                "This policy governs all categories of leave available to permanent employees of Meridian Technologies Pvt. Ltd. It applies to all employees on the company's payroll, including those on probation, with specific clauses noted where probationers are treated differently.",
                "The intent of the policy is to provide a transparent, consistent and statutorily compliant framework that balances the wellbeing of employees with the operating needs of the business. It also acts as the single source of truth for managers, HR Business Partners, and the Payroll team when administering leave entitlements.",
                "Any deviation from this policy must be authorised in writing by the HR Head and recorded in the employee's personnel file maintained by the HR Operations team.",
            ]),
            ("Applicability and Leave Year", [
                "The leave year follows the calendar year and runs from 1 January to 31 December. All entitlements reset on 1 January each year unless explicitly stated as carry-forward.",
                "The policy applies to all employees on the rolls of Meridian Technologies Pvt. Ltd. across India locations. Employees on international assignment continue to be governed by this policy, subject to local statutory minimums of the host country where these are more favourable.",
            ]),
            ("Governance and Review", [
                "The HR Head is the policy owner and is responsible for periodic review, updates, and clarifications. The policy is reviewed at least once every two years or earlier if regulatory changes warrant.",
                "Interpretation of any clause in this document is the sole prerogative of the HR Head, in consultation with the Legal team where statutory provisions are involved.",
            ]),
        ]),
        ("Types of Leave", [
            ("Categories Recognised", [
                "Meridian Technologies provides the following categories of paid leave: Earned Leave (EL), Sick Leave (SL), Casual Leave (CL), Maternity Leave, Paternity Leave, Bereavement Leave, and Marriage Leave. Special unpaid leave categories include Leave Without Pay (LWP) and Sabbatical Leave.",
                "Each category serves a distinct purpose and the eligibility, accrual and approval rules differ across them. Employees are encouraged to read the relevant section before applying.",
            ]),
            ("Annual Entitlement Snapshot", [
                "Annual entitlements for confirmed employees: 18 days Earned Leave, 12 days Sick Leave, and 6 days Casual Leave per calendar year. Probationers receive a pro-rated entitlement based on date of joining.",
                "Pro-ration for new joiners is computed on the basis of completed calendar months of service in the leave year. A fractional month of 15 days or more is treated as a completed month for accrual purposes.",
            ]),
            ("Treatment of Weekly Offs and Holidays", [
                "Saturdays, Sundays and declared public holidays falling within a stretch of leave are not counted against the employee's leave balance, except where the rules of a specific leave category state otherwise.",
                "Prefixing or suffixing of weekly offs and holidays to leave is permitted subject to manager approval and the operational needs of the team.",
            ]),
        ]),
        ("Earned Leave (EL)", [
            ("Annual Entitlement", [
                "Confirmed employees are entitled to 18 days of Earned Leave per calendar year, credited at the rate of 1.5 days per completed month of service.",
                "Probationers accrue EL at the same rate but cannot avail it until confirmation, except in special circumstances approved by HR.",
                "Crediting happens in advance on the first day of each calendar month. In the event of separation, any excess EL availed beyond the pro-rated entitlement is recovered from the final settlement.",
            ]),
            ("Carry Forward", [
                "Unused Earned Leave may be carried forward to the next calendar year subject to a maximum accumulation of 30 days.",
                "Any EL balance beyond 30 days as on 31 December will lapse automatically unless encashed during the encashment window.",
                "The carry forward limit is intended to encourage employees to take adequate time off for rest and personal commitments while still preserving a reasonable reserve.",
            ]),
            ("Minimum and Maximum Block", [
                "Minimum EL that can be availed at a stretch is 0.5 day (half day). Maximum continuous EL is 15 working days; longer durations require Business Unit Head approval.",
                "EL must be applied at least 7 calendar days in advance for durations of 3 days or more.",
                "Last minute EL is discouraged and may be declined by the Reporting Manager if business continuity is at risk. In such cases the employee will be requested to reschedule.",
            ]),
            ("Planning and Forecasting", [
                "Each team is expected to maintain a leave plan for the calendar year by 31 January. The plan is a non-binding indicator that helps Reporting Managers plan around critical delivery milestones.",
                "Managers are expected to actively encourage team members to consume at least 10 days of EL during the year for rest and recovery.",
            ]),
        ]),
        ("Sick Leave (SL)", [
            ("Entitlement and Use", [
                "Confirmed employees are entitled to 12 days of Sick Leave per calendar year. Sick Leave cannot be clubbed with Earned Leave or Casual Leave for vacation purposes.",
                "Sick Leave of 3 or more consecutive days requires a medical certificate from a registered medical practitioner, to be submitted within 7 days of return.",
                "For shorter durations a self-declaration through the HRMS is sufficient, although the Reporting Manager may request additional documentation if a pattern of misuse is observed.",
            ]),
            ("Lapse and Encashment", [
                "Sick Leave does not carry forward to the next calendar year and lapses automatically on 31 December.",
                "Sick Leave is not encashable under any circumstances.",
                "The non-encashable nature of SL is intentional and ensures the benefit remains aligned with its primary purpose, which is recovery from illness.",
            ]),
            ("Hospitalisation and Extended Illness", [
                "In the event of hospitalisation or a serious illness lasting beyond the available SL balance, the employee may convert available EL to cover the absence, or apply for Leave Without Pay if EL is exhausted.",
                "The Employee Assistance Program (EAP) and the Group Mediclaim helpdesk should be engaged in parallel for medical and psychological support.",
            ]),
        ]),
        ("Casual Leave (CL)", [
            ("Entitlement", [
                "Confirmed employees receive 6 days of Casual Leave per calendar year for short, unplanned personal needs.",
                "CL is non-cumulative, non-encashable, and lapses on 31 December.",
                "Probationers accrue CL on a pro-rated basis and may avail it once they complete 3 months of continuous service.",
            ]),
            ("Rules", [
                "Casual Leave cannot be clubbed with Earned Leave under any circumstances. It may be clubbed with weekly off or public holidays.",
                "Maximum continuous CL that may be taken is 3 days at a stretch.",
                "Repeated casual leave on Mondays or Fridays may be reviewed by the Reporting Manager for a possible pattern of misuse.",
            ]),
        ]),
        ("Maternity and Paternity Leave", [
            ("Maternity Leave", [
                "Female employees who have completed 80 days of service are entitled to 26 weeks of paid maternity leave for the first two children, in line with the Maternity Benefit Act.",
                "For the third child onwards, maternity leave is reduced to 12 weeks paid. Adoptive and commissioning mothers are entitled to 12 weeks from the date of legal adoption or surrogacy delivery.",
                "Pre-natal and post-natal medical check-ups during working hours are treated as on-duty and do not consume any leave balance.",
            ]),
            ("Paternity Leave", [
                "Male employees are entitled to 10 working days of paid Paternity Leave, to be availed within 3 months of the birth of the child. This benefit covers up to 2 children.",
                "Paternity Leave may be split into a maximum of two instalments to accommodate the immediate post-delivery period and any follow-up medical needs.",
            ]),
            ("Return to Work Support", [
                "Employees returning from maternity leave are entitled to a flexible work arrangement for the first 6 months, including the option to work from home up to 3 days per week, subject to business needs.",
                "Creche facility reimbursement is provided up to Rs. 7,500 per month per child up to the age of 6 years, as detailed in the Benefits Handbook.",
            ]),
        ]),
        ("Leave Encashment", [
            ("Annual Encashment Window", [
                "Employees may encash unused Earned Leave (EL only) up to a maximum of 15 days per calendar year. Encashment is at the basic salary plus dearness allowance prevailing on 31 December.",
                "The encashment window opens in the first week of December and closes on 20 December. Encashment is disbursed with the January payroll.",
            ]),
            ("On Separation", [
                "On separation (resignation, retirement, or termination on grounds other than misconduct), any unused EL balance is encashed in full at the last drawn basic plus DA.",
                "Encashment on separation forms part of the full and final settlement and is subject to applicable income tax provisions.",
            ]),
            ("Exclusions", [
                "Encashment of Sick Leave and Casual Leave is not permitted under any circumstance.",
                "Employees terminated for misconduct may forfeit the right to encashment as part of the disciplinary outcome, at the sole discretion of HR.",
            ]),
        ]),
        ("Leave Application Procedure", [
            ("Where and How to Apply", [
                "All leave must be applied through the HRMS leave module. Manual leave applications are accepted only when the HRMS is unavailable and must be regularised within 3 working days.",
                "An auto-generated email notification is sent to the Reporting Manager when a leave request is raised. Employees are responsible for verifying that the leave has been approved before commencing the absence.",
            ]),
            ("Approval Workflow", [
                "Approval workflow: Reporting Manager (first level) -> Business Unit Head (for EL of 5 days or more) -> HR for any clarifications. Sick Leave can be approved post-facto where prior notice was not possible.",
                "Managers are expected to action leave requests within 2 working days. Requests not acted on within 5 working days are auto-escalated to the next level.",
            ]),
            ("Unauthorised Absence", [
                "Unauthorised absence beyond 5 consecutive working days will be treated as voluntary abandonment of employment, subject to the disciplinary procedure in the Code of Conduct.",
                "Repeated short unauthorised absences are also treated as misconduct and addressed through the standard disciplinary process.",
            ]),
        ]),
        ("Leave Without Pay", [
            ("Eligibility and Approval", [
                "Leave Without Pay (LWP) may be granted at the discretion of the Reporting Manager and HR when an employee has exhausted all entitled paid leave.",
                "LWP is not a right but a facility extended on a case-by-case basis after careful evaluation of the reason and the business impact.",
            ]),
            ("Limits and Impact", [
                "LWP exceeding 30 calendar days in a year requires approval from the Business Unit Head and HR Head jointly. Extended LWP beyond 90 days may impact appraisal eligibility for the cycle.",
                "During LWP the employee remains on the rolls of the company but does not earn salary, leave accrual, or service credit for the duration.",
            ]),
            ("Benefits Continuity", [
                "Group medical cover continues during LWP up to 60 days. Beyond 60 days the employee may opt to continue cover by paying the applicable premium directly.",
                "Provident Fund contributions are suspended during LWP and resume on the employee's return to active duty.",
            ]),
        ]),
        ("Holiday Calendar and Special Leave", [
            ("Annual Holidays", [
                "The annual holiday calendar comprises 10 public holidays, of which 3 are restricted holidays employees may choose from a published list.",
                "The holiday calendar is published by HR in the first week of December each year for the following calendar year.",
            ]),
            ("Bereavement Leave", [
                "Bereavement Leave of 5 working days is granted on the death of an immediate family member (spouse, parent, child, sibling, parent-in-law).",
                "An additional 5 days of EL or LWP may be granted at the manager's discretion for travel and last rites in the case of an out-of-station event.",
            ]),
            ("Marriage Leave", [
                "Marriage Leave of 5 working days is granted once during the tenure of employment.",
                "A copy of the marriage invitation or registration certificate must be submitted to HR for record purposes.",
            ]),
        ]),
    ]
    _build(
        "HR_Leave_Policy.pdf",
        "Leave Policy",
        "HR-POL-001", "2.1", "January 2024",
        toc, sections,
    )


def gen_travel_policy():
    toc = [
        "Purpose and Applicability",
        "Travel Authorisation",
        "Domestic Travel",
        "International Travel",
        "Accommodation and Class Entitlements",
        "Per Diem Allowance",
        "Local Conveyance",
        "Reimbursement Procedure",
        "Forex and Card Policy",
        "Violations and Disciplinary Action",
    ]
    sections = [
        ("Purpose and Applicability", [
            ("Objective", [
                "This policy defines rules for business travel undertaken by employees of Meridian Technologies, both domestic and international. It applies to all confirmed employees and pre-approved contract staff travelling on behalf of the company.",
                "The policy aims to ensure that business travel is undertaken in a manner that is safe, cost effective, and consistent with the company's values around prudence and accountability.",
            ]),
            ("Scope and Exclusions", [
                "Personal travel using corporate channels, leisure extensions to business trips, and travel by family members accompanying the employee are explicitly outside the scope of company reimbursement.",
                "Where a business trip is extended for personal reasons, the incremental cost is borne entirely by the employee and clearly segregated in the expense claim.",
            ]),
            ("Policy Owner", [
                "The Travel Desk under Admin Services is the operational owner of this policy. Finance owns the reimbursement workflow and audit aspects.",
            ]),
        ]),
        ("Travel Authorisation", [
            ("Pre-Approval", [
                "All business travel must be pre-approved by the Reporting Manager and Business Unit Head. International travel additionally requires approval from the Travel Desk and the relevant VP.",
                "Approval must be obtained before any bookings are made. Travel undertaken without prior approval is not reimbursable, except in genuine emergencies subject to post-facto ratification.",
            ]),
            ("Travel Requisition", [
                "Travel Requisition Form (TRF-01) must be submitted at least 7 working days in advance for domestic and 15 working days in advance for international travel.",
                "The TRF must include the business purpose, itinerary, estimated cost, and the funding cost centre. Incomplete TRFs are returned by the Travel Desk and may delay bookings.",
            ]),
        ]),
        ("Domestic Travel", [
            ("Air Travel", [
                "Domestic air travel is permitted in economy class for all bands. Senior Vice Presidents and above are entitled to business class on flights longer than 2 hours.",
                "Bookings must be made through the empanelled travel agent or the online travel portal. Direct purchase from airlines is reimbursable only with prior written approval.",
                "Employees are expected to book at least 5 working days in advance to benefit from advance purchase fares. Same day bookings require justification in the TRF.",
            ]),
            ("Rail Travel", [
                "Rail travel is permitted in AC 2-tier for managers and below, and AC 1-tier for AVP and above. Tatkal charges are reimbursable only if travel was urgent and approved.",
                "Auto-upgrades by the Indian Railways system are reimbursable on actuals against the upgrade receipt.",
            ]),
            ("Road Travel", [
                "Inter-city road travel by company-arranged cab or self-driven vehicle is reimbursable based on the Local Conveyance section. Sleeper class private bus travel is permitted only where rail and air are not feasible.",
            ]),
        ]),
        ("International Travel", [
            ("Class of Travel", [
                "Economy class for journeys up to 6 hours. Premium economy is permitted for journeys 6 to 10 hours for managers and above. Business class is permitted for journeys exceeding 10 hours for AVP and above.",
                "Journey duration is measured as total flight time excluding layovers. Layovers exceeding 4 hours may attract eligibility for an upgrade with prior VP approval.",
            ]),
            ("Documentation", [
                "Valid passport (minimum 6 months validity), visa, travel insurance, and an approved TRF must be in place before booking. Visa fees and travel insurance are fully reimbursable.",
                "Photocopies of passport, visa, and insurance must be uploaded to the HRMS travel module before departure. The employee is responsible for ensuring compliance with the host country's entry requirements.",
            ]),
            ("Vaccinations and Health", [
                "Mandatory vaccinations and health screenings for travel to specific countries are reimbursed against medical receipts. The Travel Desk maintains an up-to-date country-wise requirements matrix.",
            ]),
        ]),
        ("Accommodation and Class Entitlements", [
            ("Domestic Accommodation Ceilings (per night, excluding taxes)", [
                "Tier 1 cities (Bengaluru, Mumbai, Delhi NCR, Chennai, Hyderabad, Pune, Kolkata): Rs. 6,000 (managers and below), Rs. 8,500 (AVP and above).",
                "Tier 2 cities: Rs. 4,500 and Rs. 6,000 respectively.",
                "Tier 3 cities and others: Rs. 3,500 and Rs. 4,500 respectively.",
            ]),
            ("International Accommodation Ceilings (per night, USD)", [
                "USA, UK, Western Europe, Singapore, Japan: USD 200 (managers and below), USD 275 (AVP and above).",
                "Other regions: USD 150 and USD 200 respectively.",
                "Ceilings are exclusive of local taxes and resort fees, both of which are reimbursable on actuals against tax invoices.",
            ]),
            ("Hotel Selection Guidelines", [
                "Where possible, employees must book through the empanelled hotel chain partners to leverage negotiated corporate rates. Booking outside this list requires justification and may be capped at the negotiated rate.",
                "Room categories above the standard category are not reimbursable unless the standard category is unavailable, documented through a non-availability note from the hotel.",
            ]),
        ]),
        ("Per Diem Allowance", [
            ("Domestic Per Diem", [
                "Domestic per diem: Rs. 1,500 per day inclusive of meals, laundry, and local incidentals. Per diem is paid for each completed 24 hour period away from base location, with a 50 percent rate for any incomplete day beyond 6 hours.",
                "Per diem is not payable for days where the company is directly bearing the full cost of meals (for example, client-hosted full-day events with all meals provided).",
            ]),
            ("International Per Diem", [
                "International per diem: USD 75 per day for travel to USA, UK, Western Europe, Singapore, Japan. USD 60 per day for other countries. Per diem is paid in INR equivalent at the rate prevailing on the date of disbursement.",
                "Where a single trip covers multiple countries, the per diem rate of each country applies for the days spent in that country, computed on a calendar-day basis.",
            ]),
            ("Coverage and Documentation", [
                "Per diem is in addition to actual accommodation reimbursement and covers meals, laundry, tips, and incidental expenses. No separate meal bills are required to be submitted.",
                "Employees are still required to maintain a brief log of business activity for each day claimed, available for sample audit by Finance.",
            ]),
        ]),
        ("Local Conveyance", [
            ("Cab Usage", [
                "Airport transfers within the same city by app-based cabs (Uber, Ola) are reimbursable on actuals. Outstation cab usage requires prior approval.",
                "Cab class is restricted to non-premium categories (Mini, Sedan) unless a premium class is operationally necessary due to passenger or baggage requirements.",
            ]),
            ("Personal Vehicle Usage", [
                "Personal vehicle usage for business travel is reimbursed at Rs. 12 per km for cars and Rs. 5 per km for two-wheelers, supported by a log entry.",
                "Toll and parking charges incurred during business travel by personal vehicle are reimbursable separately against original receipts.",
            ]),
        ]),
        ("Reimbursement Procedure", [
            ("Submission Window", [
                "All travel expense claims must be submitted in the HRMS travel module within 15 working days of completion of travel, with original receipts attached as scans.",
                "Receipts must be legible, original, and in the name of the employee where applicable. Hand-written acknowledgements are accepted only below the de minimis threshold defined in the Expense Policy.",
            ]),
            ("Approval and Payment Flow", [
                "Claims submitted beyond 30 working days will be rejected. Approval flow: Reporting Manager -> Finance for validation -> Payroll for payment with next salary cycle.",
                "Finance may request additional clarification or documentation, in which case the claim is held in queue until the employee responds. Repeated incomplete claims may attract corrective coaching.",
            ]),
        ]),
        ("Forex and Card Policy", [
            ("Forex Drawal", [
                "Forex is to be drawn through the empanelled forex partner. The maximum forex advance is 80 percent of expected international expenses excluding accommodation if paid by company card.",
                "Forex card top-ups during the trip are permitted in case of unforeseen expenses, subject to a written request to the Travel Desk and post-trip reconciliation.",
            ]),
            ("Corporate Cards", [
                "Corporate credit cards are issued to eligible roles (AVP and above) for travel expenses. Personal expenses on corporate cards are strictly prohibited.",
                "Card statements are reconciled monthly with submitted expense claims. Any unreconciled balance after 60 days is recovered from payroll.",
            ]),
        ]),
        ("Violations and Disciplinary Action", [
            ("Fraudulent Claims", [
                "Any claim found to be inflated, fabricated, or otherwise in breach of this policy will be subject to disciplinary action under the Code of Conduct, up to and including termination of employment.",
                "Where fraud is established, the amount in question is recovered in full from the employee and may attract criminal proceedings depending on the magnitude.",
            ]),
            ("Procedural Lapses", [
                "Repeated late submissions may result in suspension of travel privileges for up to 6 months.",
                "Failure to submit settlement against advance within the stipulated window may attract recovery of the entire advance from payroll along with applicable taxes.",
            ]),
        ]),
    ]
    _build(
        "HR_Travel_Reimbursement_Policy.pdf",
        "Travel Reimbursement Policy",
        "HR-POL-002", "3.0", "April 2024",
        toc, sections,
    )


def gen_medical_policy():
    toc = [
        "Coverage Overview",
        "Eligibility",
        "Sum Insured and Family Floater",
        "Dependents Covered",
        "Inclusions",
        "Exclusions",
        "Claim Procedure",
        "Cashless Hospitalisation",
        "Maternity Cover",
        "Pre and Post Hospitalisation",
    ]
    sections = [
        ("Coverage Overview", [
            ("Policy Construct", [
                "Meridian Technologies provides a Group Mediclaim Insurance Policy (GMC) for all confirmed employees and their dependents, underwritten by a leading general insurer empanelled annually.",
                "The policy is administered through a Third Party Administrator (TPA) appointed by the insurer. The TPA manages claim intimation, pre-authorisation, network hospital coordination, and final claim settlement.",
            ]),
            ("Policy Term", [
                "Coverage commences from the date of confirmation and continues for as long as the employee is on the active payroll of the company.",
                "The policy term runs annually from 1 April to 31 March. Renewal is automatic for active employees and does not require any action on the part of the employee.",
            ]),
            ("Cost", [
                "The cost of the base policy is fully borne by the company for the employee and the enrolled base dependents. Optional top-up and parental cover are at the employee's cost through monthly payroll deduction.",
            ]),
        ]),
        ("Eligibility", [
            ("Who is Covered", [
                "All confirmed permanent employees of Meridian Technologies are automatically enrolled. Probationers are eligible from the first day of confirmation.",
                "Eligibility starts from the date of confirmation and ceases on the last working day of the employee. Continuity of cover post separation is not provided by the company but may be arranged by the employee directly with the insurer.",
            ]),
            ("Who is Not Covered", [
                "Contract employees, consultants, and interns are not covered under this policy.",
                "Such workforce categories may be covered under their respective engagement contracts or independent insurance arrangements as agreed with the engaging vendor.",
            ]),
        ]),
        ("Sum Insured and Family Floater", [
            ("Base Sum Insured", [
                "The Sum Insured is Rs. 3,00,000 per family on a floater basis. The same sum insured is shared across all dependents enrolled by the employee.",
                "Floater means that the entire sum insured is available to any one or any combination of insured members during the policy year, up to the policy ceiling.",
            ]),
            ("Top-up Cover", [
                "Top-up cover of an additional Rs. 5,00,000 is available at a subsidised employee-paid premium, opted during the enrollment window in April each year.",
                "The top-up triggers once the base sum insured is exhausted in a policy year and does not have any separate sub-limits unless explicitly stated.",
            ]),
        ]),
        ("Dependents Covered", [
            ("Eligible Dependents", [
                "An employee may enroll a maximum of 2 dependents under the base policy, in addition to themselves. Eligible dependents are: spouse and up to 2 children (natural or legally adopted).",
                "The number 2 in this clause refers to dependents in addition to the employee. The total insured headcount on the base policy is therefore the employee plus up to 2 dependents.",
            ]),
            ("Parental Cover", [
                "Parents and parents-in-law are not covered under the base policy but may be enrolled under the optional Parental Cover plan at the employee's expense.",
                "Parental Cover is offered through the same insurer with a separate sum insured and a separate set of terms; details are circulated during the annual enrollment window.",
            ]),
            ("Age Limits for Children", [
                "Children are covered up to the age of 25 or until they start earning, whichever is earlier.",
                "Differently-abled dependent children may be covered beyond 25 years subject to medical documentation accepted by the insurer.",
            ]),
        ]),
        ("Inclusions", [
            ("In-patient Hospitalisation", [
                "Inpatient hospitalisation expenses (room rent, ICU charges, doctor fees, surgery, diagnostic tests, medicines) for any treatment requiring a minimum of 24 hours of hospitalisation.",
                "Room rent is capped at the standard single occupancy room of the hospital up to 1 percent of the sum insured per day; ICU is capped at 2 percent.",
            ]),
            ("Day-care and Ambulance", [
                "Day-care procedures listed by the insurer (cataract, dialysis, chemotherapy, lithotripsy, etc.) are covered even if hospitalisation is less than 24 hours.",
                "Ambulance charges up to Rs. 2,000 per hospitalisation event.",
            ]),
        ]),
        ("Exclusions", [
            ("Common Exclusions", [
                "Cosmetic surgery, dental treatment (unless arising from accidental injury), refractive errors, vaccinations (except post bite), congenital external diseases, and self-inflicted injuries.",
                "Treatments arising from substance abuse, war or warlike operations, and participation in adventure sports are excluded unless specifically endorsed by the insurer.",
            ]),
            ("Geographical Exclusions", [
                "Treatment outside India is not covered unless the employee was on an authorised business travel and the hospitalisation directly arose during that travel.",
                "Where business travel cover applies, the employee must produce the approved travel order and the supporting medical records for the hospitalisation event.",
            ]),
        ]),
        ("Claim Procedure", [
            ("Available Modes", [
                "Two modes of claim are available: Cashless at network hospitals and Reimbursement at non-network hospitals.",
                "Cashless is the preferred mode for planned hospitalisations as it minimises out-of-pocket expense for the employee.",
            ]),
            ("Intimation Timelines", [
                "All claims must be intimated to the TPA helpline within 24 hours of hospitalisation (planned) or 48 hours (emergency).",
                "Failure to intimate within the stipulated timeline may result in claim denial; in genuine cases of delay the employee should provide a written explanation to the TPA.",
            ]),
        ]),
        ("Cashless Hospitalisation", [
            ("Planned Admissions", [
                "Cashless requests for planned hospitalisation must be submitted to the TPA at least 3 working days in advance with the prescription, estimate, and pre-authorisation form.",
                "The TPA responds with the approved amount typically within 24 hours of receiving a complete request.",
            ]),
            ("Emergency Admissions", [
                "Cashless requests for emergency hospitalisation must be filed within 48 hours of admission, supported by the doctor's certificate.",
                "Where cashless is not feasible at the time of admission (for example, at a non-network hospital), the employee may convert the case to reimbursement after discharge.",
            ]),
        ]),
        ("Maternity Cover", [
            ("Benefit and Sub-limits", [
                "Maternity benefit is included in the base policy with a sub-limit of Rs. 50,000 for normal delivery and Rs. 75,000 for caesarean section.",
                "Pre and post natal expenses related to the delivery are included within the sub-limit and not paid separately.",
            ]),
            ("Eligibility", [
                "Maternity is covered for the first 2 living children only. A waiting period of 9 months from the policy inception date applies, except for new joiners where coverage is from date of confirmation.",
                "New-born baby is automatically covered from day one within the family floater for the remainder of the policy year.",
            ]),
        ]),
        ("Pre and Post Hospitalisation", [
            ("Coverage Period", [
                "Pre-hospitalisation expenses are covered for 30 days prior to admission, and post-hospitalisation expenses are covered for 60 days post discharge, provided they are related to the same ailment.",
                "Diagnostic tests, consultations, and medicines are typical eligible expenses under this clause.",
            ]),
            ("Documentation", [
                "Original receipts, discharge summary, and the doctor's prescription must be submitted within 45 days of discharge for reimbursement claims.",
                "Bills must clearly identify the patient name, treatment, and date of service. Photocopies are accepted only where the originals have been submitted to another insurer in case of split claims.",
            ]),
        ]),
    ]
    _build(
        "HR_Medical_Insurance_Policy.pdf",
        "Medical Insurance Policy",
        "HR-POL-003", "4.2", "April 2024",
        toc, sections,
    )


def gen_conduct_policy():
    toc = [
        "Purpose",
        "Core Values",
        "Workplace Behaviour",
        "Anti-Harassment and POSH",
        "Conflict of Interest",
        "Confidentiality",
        "Gifts and Hospitality",
        "Disciplinary Procedure",
        "Whistleblower Mechanism",
        "Acknowledgement",
    ]
    sections = [
        ("Purpose", [
            ("Intent of the Code", [
                "The Code of Conduct establishes the standards of behaviour expected from all employees, contractors, and representatives of Meridian Technologies. Adherence is a condition of continued employment.",
                "The Code is the foundation on which the company's culture rests and provides the framework within which all other policies are interpreted.",
            ]),
            ("Applicability", [
                "The Code applies at all times when the employee is on company premises, on company business off premises, or representing the company in any forum including social media.",
                "Conduct in private personal life is generally outside the scope of the Code, except where it impinges on the reputation, integrity, or business interests of the company.",
            ]),
        ]),
        ("Core Values", [
            ("The Five Values", [
                "Integrity, Respect, Accountability, Innovation, and Customer Centricity are the five core values. All employees are expected to act in accordance with these values in every business interaction.",
                "Each value is elaborated in the People Handbook with examples of behaviours that exemplify it and behaviours that contradict it.",
            ]),
            ("Living the Values", [
                "Living the values is a recognised criterion in the annual Performance Management process and is one of the behavioural competencies assessed at appraisal time.",
                "Leaders are expected to role model the values and visibly recognise team members who demonstrate them in everyday work.",
            ]),
        ]),
        ("Workplace Behaviour", [
            ("Non-Discrimination", [
                "Discrimination on the basis of gender, race, religion, caste, sexual orientation, disability, or age is strictly prohibited. The company is committed to providing a workplace free from harassment and bias.",
                "Hiring, promotion, compensation, and other employment decisions are made on merit and demonstrated capability, with no reference to protected characteristics.",
            ]),
            ("Substance Use and Premises", [
                "Use of intoxicants on company premises or during company business is prohibited. Smoking is permitted only in designated zones.",
                "The company maintains the right to conduct reasonable testing where there is credible suspicion of substance use that may compromise safety or judgement.",
            ]),
        ]),
        ("Anti-Harassment and POSH", [
            ("Statutory Framework", [
                "The Prevention of Sexual Harassment (POSH) policy is fully adopted. An Internal Complaints Committee (ICC) is constituted at every location with more than 10 employees.",
                "The ICC composition complies with the Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013, including an external member.",
            ]),
            ("Complaint Process", [
                "Complaints must be filed in writing to the ICC within 3 months of the incident. The ICC will complete the inquiry within 90 days. Confidentiality is strictly maintained throughout.",
                "Retaliation against a complainant or witness is itself a violation of this Code and may result in disciplinary action.",
            ]),
        ]),
        ("Conflict of Interest", [
            ("Declaration Requirement", [
                "Employees must declare any potential conflict of interest in writing to the HR head. Examples include personal business ventures in competing fields, financial interest in vendors, and close family in supplier organisations.",
                "An annual conflict declaration is conducted in April for all employees at the level of manager and above; supplementary declarations must be raised any time a new conflict arises.",
            ]),
            ("Moonlighting", [
                "External employment (moonlighting) requires prior written approval from the Business Unit Head and HR. Unapproved external employment is treated as a serious breach of contract.",
                "Voluntary, unpaid, social work generally does not require approval, except where the time commitment may impact the employee's primary role.",
            ]),
        ]),
        ("Confidentiality", [
            ("Information Protection", [
                "Confidential business information, client data, source code, designs, and strategic plans must not be shared outside the company. The Non-Disclosure Agreement signed at the time of joining continues to apply for 3 years post separation.",
                "Confidentiality obligations cover information acquired in any form, including through informal conversations, observation, or inadvertent disclosure.",
            ]),
            ("Use of Information", [
                "Confidential information may be used only for the legitimate business purposes for which access was granted. Use for personal benefit or for the benefit of any third party is strictly prohibited.",
            ]),
        ]),
        ("Gifts and Hospitality", [
            ("Acceptable Limits", [
                "Employees may accept token gifts from clients and vendors not exceeding Rs. 2,500 in value. Gifts exceeding this limit must be declined or surrendered to HR.",
                "Hospitality (meals, event invitations) of reasonable value associated with legitimate business engagements is generally acceptable and need not be declared individually.",
            ]),
            ("Strictly Prohibited", [
                "Cash, gift cards, and equivalent instruments must NEVER be accepted regardless of value.",
                "Gifts during ongoing commercial negotiations, tenders, or contract awards are not acceptable even within the limit and must be politely declined.",
            ]),
        ]),
        ("Disciplinary Procedure", [
            ("Categories of Misconduct", [
                "Minor misconduct is addressed through verbal counselling followed by a written warning. Repeated or serious misconduct leads to a formal show-cause notice and an inquiry.",
                "Gross misconduct (fraud, theft, sexual harassment, breach of confidentiality, falsification of records) may lead to immediate termination without notice.",
            ]),
            ("Inquiry Process", [
                "Disciplinary inquiries are conducted by an Inquiry Officer appointed by HR. The employee has the right to representation, written charge sheet, and a fair hearing.",
                "The Inquiry Officer submits a report and recommendation to the HR Head, who makes the final decision after due deliberation.",
            ]),
        ]),
        ("Whistleblower Mechanism", [
            ("Reporting Channels", [
                "Employees who become aware of fraud, financial irregularity, or breaches of this Code may report it anonymously via the Ethics Helpline (ethics@meridian.example) or the third-party reporting portal listed on the intranet.",
                "All reports are reviewed by the Ethics Committee comprising the HR Head, Finance Controller, and an independent member of the Audit Committee.",
            ]),
            ("Protection from Retaliation", [
                "No retaliation against a whistleblower acting in good faith is permitted. Retaliation itself is a disciplinary offence.",
                "Identity of the whistleblower is protected to the maximum extent possible consistent with the requirements of a fair inquiry.",
            ]),
        ]),
        ("Acknowledgement", [
            ("Annual Confirmation", [
                "All employees must acknowledge this Code annually through the HRMS portal. Failure to acknowledge by the published deadline may result in suspension of system access until completion.",
                "Acknowledgement is a personal certification that the employee has read, understood, and will comply with this Code in spirit and in letter.",
            ]),
            ("Training and Refreshers", [
                "An e-learning module covering the Code is rolled out annually and must be completed by all employees. Specific topics (POSH, anti-bribery) may have additional mandatory refreshers.",
            ]),
        ]),
    ]
    _build(
        "HR_Code_of_Conduct.pdf",
        "Code of Conduct",
        "HR-POL-004", "5.0", "January 2024",
        toc, sections,
    )


def gen_it_aup():
    toc = [
        "Scope",
        "Issuance of Devices",
        "Acceptable Use of Devices",
        "Software Installation and Licensing",
        "Internet and Email",
        "Remote Access and VPN",
        "Personal Use",
        "Returns and Damages",
        "Monitoring",
        "Penalties",
    ]
    sections = [
        ("Scope", [
            ("Assets Covered", [
                "This Acceptable Use Policy covers all company-issued IT assets including laptops, desktops, mobile phones, tablets, software, networks, and cloud accounts.",
                "It also covers any personal devices that are explicitly authorised to connect to company networks or to handle company data under the Bring Your Own Device (BYOD) supplementary policy.",
            ]),
            ("Applicability", [
                "The policy applies to all employees, contractors, interns, and any third parties granted access to company IT assets.",
                "Use of company IT assets in any country is governed by this policy and any additional local regulations applicable at the location of use.",
            ]),
        ]),
        ("Issuance of Devices", [
            ("Standard Allocation", [
                "Each confirmed employee is issued one primary laptop. Additional devices (secondary monitors, mobile phones, tablets) are issued based on role eligibility and require approval from the Reporting Manager.",
                "The laptop model is determined by the role and the standard hardware catalogue maintained by IT. Specific configurations outside the catalogue require IT Head approval.",
            ]),
            ("Ownership and Return", [
                "Devices remain the property of Meridian Technologies throughout the period of issue and must be returned on separation or role change.",
                "Tampering with the IT asset tag, factory reset without IT involvement, or unauthorised transfer to another employee is strictly prohibited.",
            ]),
        ]),
        ("Acceptable Use of Devices", [
            ("Primary Purpose", [
                "Company devices are issued primarily for business use. Limited and reasonable personal use is permitted provided it does not interfere with work or violate any policy.",
                "Examples of acceptable personal use include occasional personal email, online banking, and short news reading during breaks.",
            ]),
            ("Restrictions", [
                "Employees must not modify hardware configurations, remove asset tags, or share device credentials with anyone, including family members.",
                "Installation of hardware (RAM, storage) by the employee is not permitted; any hardware upgrade must be routed through IT to preserve warranty and support arrangements.",
            ]),
        ]),
        ("Software Installation and Licensing", [
            ("Approved Software", [
                "Only software from the IT-approved catalogue (accessible via the IT Service Desk portal) may be installed. Self-installation through the catalogue is permitted for whitelisted titles.",
                "The catalogue is refreshed quarterly. Requests for inclusion of new software may be raised through the IT Service Desk for review.",
            ]),
            ("Unapproved Software", [
                "Installation of any software outside the approved catalogue requires a Software Request Ticket and IT Security review. Pirated, cracked, or unlicensed software is strictly prohibited.",
                "Use of personal cloud storage (Dropbox, Google Drive, OneDrive personal) for company data is prohibited. The approved enterprise OneDrive must be used.",
            ]),
            ("License Compliance", [
                "License compliance is the responsibility of both the employee and IT. Annual audits are conducted to reconcile installed software against entitlement records.",
            ]),
        ]),
        ("Internet and Email", [
            ("Internet Use", [
                "Internet access is provided for business purposes. Browsing of websites containing illegal content, adult material, gambling, or known phishing or malware sources is blocked and logged.",
                "Bandwidth-intensive activities not related to work (large personal downloads, streaming during meetings) may be throttled and flagged for managerial review.",
            ]),
            ("Email Use", [
                "Company email accounts must not be used to subscribe to personal services or to send chain mails. Auto-forwarding of company email to personal accounts is strictly prohibited.",
                "Out-of-office responses must be set up before any planned leave so that internal and external stakeholders are informed of the absence and the point of contact.",
            ]),
        ]),
        ("Remote Access and VPN", [
            ("VPN and MFA", [
                "Remote access to company systems requires connecting through the company VPN with multi-factor authentication. Split tunnelling and use of personal proxies is prohibited.",
                "The MFA factor must be the company-issued authenticator app or hardware token. SMS-based MFA is permitted only as a temporary fallback.",
            ]),
            ("Public Networks", [
                "Access from public Wi-Fi networks is permitted only after VPN connection is established. Public Wi-Fi without VPN is forbidden for all company work.",
                "Use of personal mobile hotspots is preferred to public Wi-Fi when an alternative is needed; mobile hotspot data may be reimbursed under the Communication Allowance scheme for eligible roles.",
            ]),
        ]),
        ("Personal Use", [
            ("Reasonable Use", [
                "Personal use is permitted only outside core working hours and only for non-resource-intensive activities. Streaming, gaming, torrents, and cryptocurrency mining are strictly prohibited.",
                "Personal storage on the company device should be minimised; any personal data is at the employee's own risk and may be wiped during routine IT operations.",
            ]),
            ("Family and Friends", [
                "Allowing family members or friends to use the company device for any purpose is not permitted. The credentials are personal to the employee and not transferable.",
            ]),
        ]),
        ("Returns and Damages", [
            ("On Separation", [
                "On separation, all devices must be returned to the IT Service Desk within 3 working days of the last working day. Failure to return devices may result in deduction from final settlement at replacement cost.",
                "Personal data must be backed up by the employee before the last working day; IT does not retain employee personal data after the device is reclaimed.",
            ]),
            ("Damage and Loss", [
                "Accidental damage must be reported within 24 hours. The first instance is treated as a no-fault event; subsequent damages may attract a recovery fee per the IT asset schedule.",
                "Loss or theft of a device must be reported to IT Security and to the nearest police station; an FIR copy is required to process the replacement.",
            ]),
        ]),
        ("Monitoring", [
            ("Right to Monitor", [
                "All activity on company networks and devices is subject to monitoring and audit. Employees should have no expectation of privacy for activities conducted on company IT assets.",
                "Monitoring is conducted in accordance with applicable law and is proportionate to the legitimate interests of the company.",
            ]),
            ("Data Retention", [
                "Logs of activity, including web browsing, email metadata, and security events, are retained for a defined period as per the Data Security Policy.",
            ]),
        ]),
        ("Penalties", [
            ("Disciplinary Action", [
                "Breach of this policy may result in disciplinary action up to and including termination, recovery of damages, and in cases of legal violation, referral to law enforcement.",
                "The severity of the action will depend on the nature of the breach, intent, and prior history of similar incidents.",
            ]),
            ("Restoration of Access", [
                "Where access has been suspended following a breach, restoration requires the explicit clearance of the IT Security Head and the HR Head.",
            ]),
        ]),
    ]
    _build(
        "IT_Acceptable_Use_Policy.pdf",
        "Acceptable Use Policy",
        "IT-POL-001", "2.5", "March 2024",
        toc, sections,
    )


def gen_data_security():
    toc = [
        "Purpose and Scope",
        "Data Classification",
        "Handling Public Data",
        "Handling Internal Data",
        "Handling Confidential Data",
        "Handling Restricted Data",
        "Data Storage and Encryption",
        "Data Transfer",
        "Data Breach Response",
        "Records Retention",
    ]
    sections = [
        ("Purpose and Scope", [
            ("Objective", [
                "This policy defines how all data assets owned, processed, or handled by Meridian Technologies must be classified, stored, transmitted, and disposed of to maintain confidentiality, integrity, and availability.",
                "The policy supports the company's obligations under contracts with clients, applicable laws, and industry standards such as ISO 27001 and the Digital Personal Data Protection Act.",
            ]),
            ("Applicability", [
                "The policy applies to all employees, contractors, and third parties handling company or client data, in any form (electronic, paper, verbal) and at any location.",
                "Any deviation must be approved in writing by the Data Protection Officer (DPO) and documented as a risk-accepted exception in the Information Security Risk Register.",
            ]),
        ]),
        ("Data Classification", [
            ("Tiers", [
                "All data is classified into one of four tiers: Public, Internal, Confidential, and Restricted. Owners of each data asset are responsible for accurate classification at creation.",
                "Misclassification, whether by under or over classification, is itself a breach of this policy and may attract disciplinary action.",
            ]),
            ("Tier Definitions", [
                "Public: information explicitly approved for public release. Internal: business information for employee use only. Confidential: business-sensitive information including client data and financials. Restricted: highly sensitive personal data, source code of products, regulatory data, and trade secrets.",
                "Where data spans multiple tiers, the highest applicable tier governs handling for the combined asset.",
            ]),
        ]),
        ("Handling Public Data", [
            ("Release Process", [
                "Public data has no handling restrictions but must still be reviewed by the Communications team before external release if it represents the company.",
                "Public data that has been distorted, redacted, or aggregated for release must be reviewed to ensure no Internal or higher data is inadvertently disclosed.",
            ]),
            ("Versioning", [
                "All publicly released data must indicate the date of release and a clear point of contact within the company for queries and corrections.",
            ]),
        ]),
        ("Handling Internal Data", [
            ("Sharing", [
                "Internal data may be shared freely with employees on a need-to-know basis. Sharing with vendors or external parties requires an NDA to be in place.",
                "Internal data must not be posted on personal social media, blogs, or any externally facing forum without prior approval from Communications.",
            ]),
            ("Storage", [
                "Internal data should reside on company-managed storage. Local copies on laptops are acceptable provided full disk encryption is in place.",
            ]),
        ]),
        ("Handling Confidential Data", [
            ("Storage Controls", [
                "Confidential data must be stored in IT-managed systems with access controls. Local storage on laptops is permitted but must be in the encrypted user profile partition.",
                "Access to Confidential repositories is granted on a least-privilege basis and reviewed every six months by the data owner.",
            ]),
            ("Sharing Controls", [
                "Sharing externally requires written approval from the data owner and the use of approved secure channels (encrypted email, secure file transfer, NDA-backed portals).",
                "Forwarding of Confidential email to external addresses is blocked at the gateway and requires explicit allow-listing for approved recipients.",
            ]),
        ]),
        ("Handling Restricted Data", [
            ("Storage and Access", [
                "Restricted data must never be stored on laptops, USB drives, or personal devices. It must reside only on designated secure servers with role-based access and full audit logging.",
                "Access to Restricted data requires explicit written approval from the Data Protection Officer (DPO) and is reviewed quarterly. All access is logged and reviewed monthly.",
            ]),
            ("Handling in Practice", [
                "Printing of Restricted data is permitted only on dedicated secure printers with badge release; printed copies must be tracked and shredded after use.",
                "Discussion of Restricted data over public channels (open offices, shared transport, public events) is prohibited.",
            ]),
        ]),
        ("Data Storage and Encryption", [
            ("Encryption Standards", [
                "All laptops and removable media must be encrypted using the company-approved disk encryption tool. Decryption keys are managed centrally by IT Security.",
                "Confidential and Restricted data at rest must be encrypted with AES-256 or stronger. Data in transit must be protected with TLS 1.2 or higher.",
            ]),
            ("Key Management", [
                "Encryption keys are stored in a Hardware Security Module (HSM) and access to keys is restricted to authorised IT Security personnel through a dual-control process.",
                "Key rotation occurs at least annually for keys used to protect Restricted data, and on demand whenever a compromise is suspected.",
            ]),
        ]),
        ("Data Transfer", [
            ("Approved Channels", [
                "Approved channels for external transfer of Confidential data: secure file transfer portal, encrypted email (S/MIME or PGP), and DRM-protected document sharing.",
                "Each external transfer must include the appropriate sensitivity label and any necessary recipient handling instructions.",
            ]),
            ("Removable Media", [
                "USB devices and removable media for data transfer are blocked by default. Exceptions require approval from IT Security and the data owner, are time-bound, and the device must be encrypted.",
                "Lost or stolen removable media containing company data must be reported immediately to IT Security as a potential data breach.",
            ]),
        ]),
        ("Data Breach Response", [
            ("Initial Response", [
                "Any suspected or confirmed data breach must be reported within 2 hours to the Incident Response Team (irt@meridian.example).",
                "Employees observing a potential breach must not attempt independent investigation; their role is to report promptly and preserve evidence.",
            ]),
            ("Response Plan", [
                "The IRT will follow the Data Breach Response Plan: contain, assess, notify the DPO and Legal, notify affected parties as per regulatory requirements, and document for post-incident review.",
                "A formal post-incident review is conducted within 30 days of closure to identify root cause and corrective actions.",
            ]),
            ("Regulatory Notification", [
                "Regulatory breach notifications, where applicable (such as under the DPDP Act), must be initiated within 72 hours of confirmation of breach.",
                "Communication with regulators is centralised through the DPO and Legal team; no other employee should communicate with regulators on breach matters.",
            ]),
        ]),
        ("Records Retention", [
            ("Retention Periods", [
                "Internal and Confidential data is retained for 7 years unless a longer period is mandated by regulation or contract. Restricted data retention is governed by the specific contract or law applicable to that data.",
                "Personal data of employees is retained for the duration of employment and 8 years post separation, in line with statutory and tax requirements.",
            ]),
            ("Disposal", [
                "On retention expiry, data must be securely disposed of using IT-approved sanitisation methods (cryptographic erasure or physical destruction for media).",
                "Disposal must be evidenced through a Certificate of Destruction issued by IT or the empanelled disposal vendor.",
            ]),
        ]),
    ]
    _build(
        "IT_Data_Security_Policy.pdf",
        "Data Security Policy",
        "IT-POL-002", "3.1", "February 2024",
        toc, sections,
    )


def gen_expense():
    toc = [
        "Purpose",
        "Eligible Expense Categories",
        "Approval Limits",
        "Documentation",
        "Submission Timelines",
        "Non-Reimbursable Items",
        "Foreign Currency Claims",
        "Audit and Sample Checks",
        "Recovery of Excess Payments",
        "Disputes",
    ]
    sections = [
        ("Purpose", [
            ("Objective", [
                "This policy governs the reimbursement of business expenses incurred by employees on behalf of Meridian Technologies. The aim is to ensure expenses are reasonable, properly approved, and well documented.",
                "The policy is designed to enable employees to perform their roles without personal financial detriment while protecting the company from fraud, waste, and abuse.",
            ]),
            ("Guiding Principles", [
                "Every claim must satisfy three tests: it must be a legitimate business expense, it must be reasonable in amount, and it must be properly evidenced. Failure on any one test renders the claim ineligible.",
                "Employees and managers are jointly accountable for the integrity of submitted claims.",
            ]),
        ]),
        ("Eligible Expense Categories", [
            ("Business Expenses", [
                "Business travel (covered separately under the Travel Policy), client entertainment, internal team events, training and certification fees, professional memberships, mobile and internet reimbursements for eligible roles, and small office supplies.",
                "Client entertainment must be associated with a genuine business meeting; attendee names and the business purpose must be recorded on the claim.",
            ]),
            ("Communication and Learning", [
                "Mobile and internet reimbursement caps are defined in the Communication Allowance Scheme by role band. Claims above the cap require Business Unit Head approval.",
                "Training and certification fees are reimbursable where the certification is aligned with the employee's role or planned career progression and approved in advance.",
            ]),
        ]),
        ("Approval Limits", [
            ("Up to Rs. 10,000", [
                "Expense claims up to Rs. 10,000 require approval from the Reporting Manager only.",
                "Claims within this band typically include team lunches, small office supplies, and minor reimbursements.",
            ]),
            ("Rs. 10,001 to Rs. 50,000", [
                "Claims between Rs. 10,001 and Rs. 50,000 require approval from the Reporting Manager and the Business Unit Head.",
                "Approvers are expected to verify the business purpose and the reasonableness of the amount before approving.",
            ]),
            ("Above Rs. 50,000", [
                "Claims above Rs. 50,000 require approval from the relevant Vice President. Claims above Rs. 2,00,000 additionally require concurrence from the Finance Controller.",
                "Such high value claims must include a written business justification attached to the claim record.",
            ]),
        ]),
        ("Documentation", [
            ("Receipts and Invoices", [
                "All claims must be supported by original receipts, invoices, or system-generated bills. Hand-written acknowledgements are accepted only for unavoidable expenses below Rs. 500.",
                "Receipts in foreign languages must be accompanied by a brief English translation of the key fields (date, amount, vendor, item).",
            ]),
            ("GST Compliance", [
                "Invoices for amounts above Rs. 5,000 must include the company GSTIN to be eligible for input tax credit. Claims without GSTIN above this threshold may be processed at the reduced amount net of tax.",
                "Vendors who consistently fail to issue compliant invoices should be flagged to the Procurement team for review.",
            ]),
        ]),
        ("Submission Timelines", [
            ("Standard Window", [
                "Expense claims must be submitted via the HRMS Finance module within 15 working days of incurring the expense. Claims for expenses older than 60 days will not be processed.",
                "The submission window starts from the date of the expense for self-incurred items or the date of receipt of the invoice for vendor-billed items.",
            ]),
            ("Manager Approval Timelines", [
                "Managers are expected to action submitted claims within 5 working days. Claims not approved within 10 working days are auto-escalated.",
            ]),
        ]),
        ("Non-Reimbursable Items", [
            ("Personal Items", [
                "Personal items, alcoholic beverages (unless part of an approved client entertainment), traffic fines, parking tickets, late fees, and any expense flagged in the Travel Policy exclusions.",
                "Spousal or family expenses on a business trip, except in the rare case of a formally approved spouse-accompanied business event.",
            ]),
            ("Statutory Exclusions", [
                "Personal taxes, donations made in personal capacity, and any item considered prohibited under applicable anti-bribery laws are not reimbursable irrespective of amount or approver.",
            ]),
        ]),
        ("Foreign Currency Claims", [
            ("Currency and Conversion", [
                "Foreign currency expenses must be claimed in the original currency, supported by credit card statements or forex card transaction records. Conversion to INR is done by Finance using the rate on the date of expense.",
                "Where the credit card statement reflects a converted INR amount, that converted amount is taken as the final claim value and the original currency amount is recorded for audit reference.",
            ]),
            ("Forex Cards", [
                "Reconciliation of forex card balances post trip is the employee's responsibility, in coordination with the Travel Desk.",
            ]),
        ]),
        ("Audit and Sample Checks", [
            ("Routine Audit", [
                "Finance conducts a quarterly audit of 5 percent of claims on a sample basis. The Internal Audit team may conduct additional reviews. Audit findings are reported to the Audit Committee.",
                "Sample selection is risk-weighted, with higher value and high frequency claimants having a greater probability of selection.",
            ]),
            ("Cooperation", [
                "Employees are expected to cooperate fully with audit queries and to provide supporting documents within 5 working days of request.",
            ]),
        ]),
        ("Recovery of Excess Payments", [
            ("Recovery Mechanism", [
                "Any excess payment identified through audit or self-disclosure must be returned within 30 days. Recovery via salary deduction is exercised only as a last resort with employee acknowledgement.",
                "Self-disclosure of excess payment is encouraged and is treated as a mitigating factor when assessing any disciplinary outcome.",
            ]),
        ]),
        ("Disputes", [
            ("Resolution Path", [
                "Disputes regarding claim rejection or partial approval should be raised in writing within 7 working days of the decision. The Finance Controller is the final authority on expense policy interpretation.",
                "The dispute resolution turnaround is 10 working days from the date all necessary documents are with Finance.",
            ]),
        ]),
    ]
    _build(
        "Finance_Expense_Reimbursement_Policy.pdf",
        "Expense Reimbursement Policy",
        "FIN-POL-001", "2.3", "April 2024",
        toc, sections,
    )


def gen_procurement():
    toc = [
        "Purpose",
        "Procurement Principles",
        "Vendor Empanelment",
        "Purchase Order Limits",
        "Tendering and Quotations",
        "Single Source Justification",
        "Contract Approvals",
        "Payment Terms",
        "Performance Review",
        "Conflict of Interest",
    ]
    sections = [
        ("Purpose", [
            ("Intent", [
                "The Procurement Policy ensures all purchases of goods and services by Meridian Technologies are made through a transparent, competitive, and value-driven process.",
                "It establishes the standards that all procurement activity must meet, irrespective of the cost centre, the geography, or the nature of the spend.",
            ]),
            ("Scope", [
                "The policy applies to all procurement undertaken by or on behalf of the company, including capital expenditure, operating expenditure, and service contracts.",
                "Procurement undertaken on behalf of clients under back-to-back contracts is additionally subject to any specific client requirements that may be more stringent.",
            ]),
        ]),
        ("Procurement Principles", [
            ("Core Principles", [
                "All procurement is guided by the principles of transparency, value for money, fairness, accountability, and adherence to legal and regulatory requirements.",
                "Value for money is not synonymous with lowest price; total cost of ownership, quality, and supplier reliability are equally important.",
            ]),
            ("Ethical Conduct", [
                "Procurement decisions must be free from personal bias, conflict of interest, and any consideration extraneous to the business merits of the proposal.",
                "All procurement personnel are required to complete an anti-bribery training annually.",
            ]),
        ]),
        ("Vendor Empanelment", [
            ("Empanelment Process", [
                "Vendors providing recurring goods or services must be empanelled through the annual vendor evaluation process. Empanelment includes due diligence on financial stability, references, statutory compliance, and a sample order.",
                "New vendors required for one-off procurements may be onboarded through a simplified due diligence track, subject to a value cap.",
            ]),
            ("Approving Authority", [
                "Vendor empanelment is approved by the Procurement Committee, comprising the Procurement Head, Finance Controller, and the user department head.",
                "Empanelment is valid for two years from the date of approval and is subject to renewal based on performance review.",
            ]),
        ]),
        ("Purchase Order Limits", [
            ("Up to Rs. 50,000", [
                "Purchase Orders up to Rs. 50,000 may be raised by the user department head with approval from the Procurement Head.",
                "These low value purchases follow a simplified workflow but must still be supported by at least one written quotation.",
            ]),
            ("Rs. 50,001 to Rs. 5,00,000", [
                "Purchase Orders from Rs. 50,001 to Rs. 5,00,000 require approval from the Procurement Head and Finance Controller.",
            ]),
            ("Above Rs. 5,00,000", [
                "Purchase Orders above Rs. 5,00,000 require approval from the relevant Vice President. POs above Rs. 25,00,000 additionally require CFO approval.",
                "Capital expenditure above Rs. 1,00,00,000 requires Board approval.",
            ]),
        ]),
        ("Tendering and Quotations", [
            ("Standard Quotations", [
                "Procurement above Rs. 1,00,000 requires a minimum of 3 written quotations from empanelled vendors.",
                "Where 3 quotations are not feasible, a written justification approved by the Procurement Head must be filed.",
            ]),
            ("Formal RFP", [
                "Procurement above Rs. 10,00,000 requires a formal RFP process with sealed bids opened by a panel of at least 3 members from Procurement, Finance, and the user department.",
                "RFP evaluation criteria must be documented before bid opening and applied consistently to all bidders.",
            ]),
        ]),
        ("Single Source Justification", [
            ("When Allowed", [
                "Single source procurement is permitted only where it is the sole supplier, an OEM, or for an emergency where time-bound delivery is essential.",
                "Brand preference of the user department alone is not sufficient justification for single source procurement.",
            ]),
            ("Approval Requirement", [
                "Single source justification must be documented in writing and approved by the Procurement Head and Finance Controller, irrespective of order value.",
                "A periodic review of single source contracts is conducted annually to determine whether alternatives can be developed.",
            ]),
        ]),
        ("Contract Approvals", [
            ("Legal Review", [
                "All contracts with vendors must be vetted by the Legal team. Contracts above Rs. 10,00,000 in value or those involving sharing of Confidential or Restricted data also require Information Security and Data Protection Officer review.",
                "Standard contract templates have been pre-approved by Legal; using these accelerates the review process.",
            ]),
            ("Signatures and Storage", [
                "Contracts must be signed by an authorised signatory as per the Delegation of Authority matrix. Signed contracts are stored in the Contract Management System and remain accessible for audit.",
            ]),
        ]),
        ("Payment Terms", [
            ("Standard Terms", [
                "Standard payment terms are net 30 days from receipt of invoice and goods or services. Advance payments are permitted only for the procurement of capital goods up to 25 percent of order value, against a bank guarantee.",
                "Early payment discounts offered by vendors should be evaluated by Finance for cash flow benefit before being accepted.",
            ]),
            ("Disputes and Holds", [
                "Disputed invoices are held in suspense until resolved between the user department, Procurement, and the vendor; aged disputes are reviewed monthly by Finance.",
            ]),
        ]),
        ("Performance Review", [
            ("Review Cadence", [
                "Vendor performance is reviewed semi-annually on quality, timeliness, responsiveness, and pricing. Underperforming vendors are issued an improvement plan; persistent issues lead to de-empanelment.",
                "Strategic vendors are reviewed jointly with the user department through a structured business review meeting.",
            ]),
            ("Feedback Mechanism", [
                "User departments are encouraged to log feedback in the Vendor Management System on an ongoing basis to ensure the periodic review is based on a complete data set.",
            ]),
        ]),
        ("Conflict of Interest", [
            ("Declarations", [
                "Employees involved in procurement decisions must declare any personal interest in a vendor. Direct family members of employees may not be vendors without explicit approval of the CFO and the Audit Committee.",
                "Declarations are refreshed annually and additionally whenever a new conflict is identified.",
            ]),
            ("Recusal", [
                "Where a conflict exists, the conflicted employee must recuse themselves from the procurement decision and have no involvement in evaluation or approval.",
            ]),
        ]),
    ]
    _build(
        "Finance_Procurement_Policy.pdf",
        "Procurement Policy",
        "FIN-POL-002", "1.8", "June 2024",
        toc, sections,
    )


def gen_wfh():
    toc = [
        "Purpose and Applicability",
        "Eligibility",
        "Maximum WFH Days",
        "Approval Workflow",
        "Equipment and Connectivity",
        "Working Hours and Availability",
        "Attendance and Productivity",
        "Information Security",
        "Wellbeing and Communication",
        "Policy Review",
    ]
    sections = [
        ("Purpose and Applicability", [
            ("Intent", [
                "This policy defines the framework under which employees may work from home (WFH) or remote locations, balancing flexibility with productivity and collaboration.",
                "WFH is offered as a benefit and an enabler, not a right; it remains subject to the operational needs of the business and the discretion of the Reporting Manager.",
            ]),
            ("Coverage", [
                "The policy applies to all Meridian Technologies employees in India. Region-specific addenda may apply for employees in other geographies, in alignment with local labour regulations.",
            ]),
        ]),
        ("Eligibility", [
            ("Confirmed Employees", [
                "All confirmed employees of Meridian Technologies are eligible to apply for WFH. Employees on probation are NOT eligible for the standard WFH benefit; exceptions may be granted only with HR Head approval for genuine reasons such as medical advisories.",
                "Where probation is extended, eligibility for WFH continues to be deferred until confirmation.",
            ]),
            ("Role Exclusions", [
                "Roles which require physical presence (such as front office, lab operations, and on-site customer support) are excluded from WFH except on a case-by-case basis.",
                "Eligibility for excluded roles may be reconsidered if the role evolves to permit remote performance without operational impact.",
            ]),
        ]),
        ("Maximum WFH Days", [
            ("Routine WFH", [
                "Confirmed employees may avail a maximum of 2 WFH days per week. The remaining 3 days must be from the office unless an approved exception is in place.",
                "WFH days are typically aligned within the team to ensure adequate in-person collaboration on agreed days.",
            ]),
            ("Extended WFH", [
                "Special WFH (extended) of up to 5 working days in a row may be requested for specific reasons (relocation, health, family emergency) and requires Business Unit Head approval.",
                "Extended WFH beyond 5 working days is exceptional and may require an explicit relocation or remote work arrangement to be formalised.",
            ]),
        ]),
        ("Approval Workflow", [
            ("Routine Approvals", [
                "Routine weekly WFH (within the 2 days entitlement) requires approval from the Reporting Manager via the HRMS leave/attendance module.",
                "Routine requests should be raised at least 1 working day in advance to enable team planning.",
            ]),
            ("Extended Approvals", [
                "Special or extended WFH requires approval from the Reporting Manager AND the Business Unit Head.",
                "Approvers are expected to balance the legitimate personal need of the employee against any business impact and propose alternatives where possible.",
            ]),
        ]),
        ("Equipment and Connectivity", [
            ("Devices", [
                "Employees on WFH must use the company-issued laptop. Personal devices are not permitted for company work.",
                "Peripherals (monitor, keyboard) are not generally provided for WFH but may be borrowed from office inventory subject to availability and asset tracking.",
            ]),
            ("Connectivity", [
                "A reliable broadband connection of at least 25 Mbps download is recommended. The company does not provide a dedicated broadband reimbursement for general WFH; eligible roles may claim under the Communication Allowance scheme.",
                "Persistent connectivity issues that impact deliverables should be raised with the Reporting Manager; in such cases the employee may be required to return to office until resolved.",
            ]),
        ]),
        ("Working Hours and Availability", [
            ("Core Hours", [
                "Core working hours during WFH are 10:00 to 16:00, during which employees must be available on Teams or the equivalent collaboration platform.",
                "Status indicators must be kept up to date so that colleagues can identify availability for ad-hoc collaboration.",
            ]),
            ("Standard Business Hours", [
                "Employees must be reachable on the registered mobile number and email throughout standard business hours of 09:00 to 18:00.",
                "Any planned unavailability within business hours should be flagged on the team calendar.",
            ]),
        ]),
        ("Attendance and Productivity", [
            ("Attendance Marking", [
                "Attendance is marked via the HRMS self-service module on WFH days. Failure to mark attendance is treated as absence.",
                "Three consecutive instances of missed attendance marking will trigger an alert to the Reporting Manager.",
            ]),
            ("Productivity Review", [
                "Periodic productivity reviews may be conducted by the Reporting Manager. Sustained underperformance during WFH may lead to suspension of the WFH benefit.",
                "Suspension of WFH is treated as a performance enablement step, not a disciplinary action, and is reviewed quarterly.",
            ]),
        ]),
        ("Information Security", [
            ("Policy Compliance", [
                "Employees on WFH must comply with the IT Acceptable Use Policy and Data Security Policy at all times. The workplace must be reasonably private to prevent shoulder-surfing of confidential information.",
                "Family members and visitors should not have visual or auditory access to the employee's work screens and calls.",
            ]),
            ("Restricted Data", [
                "Confidential calls must not be taken in shared public spaces. Restricted data work is not permitted from any location other than office premises.",
                "Where role exposure to Restricted data is incidental, the employee must coordinate with the manager to schedule such work on office days.",
            ]),
        ]),
        ("Wellbeing and Communication", [
            ("Work-Life Boundaries", [
                "Employees and managers are encouraged to take regular breaks and maintain a clear separation between work and personal time, even when working from home.",
                "Late-night or weekend communications should be the exception, not the norm; managers must role model healthy disconnection.",
            ]),
            ("Team Connection", [
                "Managers are expected to hold at least one team in-person day per fortnight to maintain team cohesion.",
                "Informal connect activities such as team lunches and offsites are encouraged to offset the dilution of relationships that can result from extended remote work.",
            ]),
        ]),
        ("Policy Review", [
            ("Review Cycle", [
                "This policy will be reviewed annually by the HR Head and Business Unit Heads in consultation with the Leadership Team to ensure it remains aligned with business needs.",
                "Employees are welcome to provide feedback through the HR feedback portal, which is reviewed as input to the annual policy refresh.",
            ]),
        ]),
    ]
    _build(
        "WFH_Remote_Work_Policy.pdf",
        "Work From Home and Remote Work Policy",
        "HR-POL-005", "1.4", "May 2024",
        toc, sections,
    )


def gen_performance():
    toc = [
        "Purpose",
        "Performance Cycle",
        "Goal Setting",
        "Rating Scale",
        "Calibration",
        "Performance Improvement Plan",
        "Promotion Eligibility",
        "Recognition and Rewards",
        "Appeals",
        "Confidentiality",
    ]
    sections = [
        ("Purpose", [
            ("Objective", [
                "The Performance Management Policy provides a structured framework for setting, reviewing, and rewarding individual performance at Meridian Technologies.",
                "The goal of the framework is to align individual contributions with the broader strategic priorities of the company and to enable continuous growth for each employee.",
            ]),
            ("Underlying Beliefs", [
                "Performance management is a continuous process, not a once-a-year event. Formal reviews codify what should already have been visible through regular conversations between the employee and the Reporting Manager.",
                "Fairness, transparency, and developmental orientation are the three values that guide the operation of this policy.",
            ]),
        ]),
        ("Performance Cycle", [
            ("Cycle Calendar", [
                "The performance management year runs from 1 April to 31 March. Goal-setting is completed by 30 April. Mid-year review is conducted in October. Annual appraisal is completed by 31 May of the following year.",
                "Employees joining mid-cycle are governed by a pro-rated cycle aligned to their joining date.",
            ]),
            ("Conversations and Documentation", [
                "Each milestone in the cycle is supported by a formal conversation between the employee and the Reporting Manager, documented in the HRMS Performance module.",
            ]),
        ]),
        ("Goal Setting", [
            ("SMART Goals", [
                "Goals are set jointly by the employee and the Reporting Manager, using the SMART framework (Specific, Measurable, Achievable, Relevant, Time-bound).",
                "Each goal must clearly identify how achievement will be measured at the end of the cycle to avoid subjectivity at appraisal time.",
            ]),
            ("Goal Count and Weight", [
                "Each employee should have between 5 and 8 goals, with explicit weighting that sums to 100 percent. At least one goal must be a development or learning goal.",
                "Goal revision during the year is permitted with manager agreement and is encouraged when business priorities shift materially.",
            ]),
        ]),
        ("Rating Scale", [
            ("Scale Definition", [
                "Annual performance is rated on a 5-point scale: 1 - Below Expectations, 2 - Partially Meets Expectations, 3 - Meets Expectations, 4 - Exceeds Expectations, 5 - Outstanding.",
                "The rating reflects performance against the agreed goals as well as how those results were achieved (the behavioural dimension).",
            ]),
            ("Computation", [
                "Final ratings are computed as a weighted score of goal achievement (70 percent) and behavioural competencies (30 percent), and then mapped to the 5-point scale.",
                "Where a goal could not be pursued for reasons outside the employee's control, the manager should record a written note and exclude the goal from the weighted computation with HR Business Partner concurrence.",
            ]),
        ]),
        ("Calibration", [
            ("Forced Distribution", [
                "All ratings are calibrated through a forced-distribution guideline at the Business Unit level: not more than 15 percent rated Outstanding or Exceeds combined, and not more than 10 percent rated Below or Partially Meets combined.",
                "The guideline is an aid to consistency and is not interpreted mechanically at the team level; smaller teams may legitimately deviate from the overall distribution.",
            ]),
            ("Calibration Forum", [
                "Calibration discussions are chaired by the Business Unit Head and attended by the HR Business Partner.",
                "Calibration discussions are confidential; managers should not discuss other employees' performance with their direct reports.",
            ]),
        ]),
        ("Performance Improvement Plan", [
            ("PIP Construct", [
                "Employees rated Below Expectations are placed on a formal Performance Improvement Plan (PIP) of 90 days duration. The PIP contains specific, measurable improvement goals and weekly check-ins.",
                "The objective of the PIP is genuine improvement; managers are expected to provide active coaching and timely feedback through the PIP period.",
            ]),
            ("PIP Outcomes", [
                "At the end of the PIP, performance is reviewed. Successful completion restores normal status. Unsuccessful completion may lead to extension by 30 days, role change, or separation, as decided by HR and the Business Unit Head jointly.",
                "Where a PIP is in progress, the employee is not eligible for promotion or for variable pay tied to high performance.",
            ]),
        ]),
        ("Promotion Eligibility", [
            ("Readiness Criteria", [
                "Promotion is based on demonstrated readiness for the next role and is independent of the annual rating, though a minimum rating of Meets Expectations is required.",
                "Readiness is assessed against the competency framework for the target level, not merely on time spent in the current role.",
            ]),
            ("Tenure Threshold", [
                "A minimum tenure of 18 months in the current role is required for promotion consideration. Exceptions for high-potential employees require Business Unit Head and HR Head approval.",
                "Promotion decisions are made during the annual cycle by the Promotion Committee comprising the Business Unit Head, HR Business Partner, and an independent member from a peer business unit.",
            ]),
        ]),
        ("Recognition and Rewards", [
            ("Annual Rewards", [
                "Annual increments and variable pay are linked to the final rating and Business Unit performance. The exact ratio is communicated during the annual compensation cycle.",
                "Increments take effect from 1 July each year following the appraisal completion.",
            ]),
            ("Spot Recognition", [
                "Spot recognition awards and quarterly excellence awards provide non-cycle recognition opportunities, governed by the Rewards and Recognition guideline.",
                "Managers are encouraged to use spot recognition liberally to reinforce desired behaviours close to the time of the achievement.",
            ]),
        ]),
        ("Appeals", [
            ("Filing an Appeal", [
                "Employees who disagree with their final rating may file a written appeal to the HR Head within 10 working days of communication. Appeals are reviewed by a panel consisting of the HR Head, Business Unit Head, and the next-level reviewer.",
                "Appeals must clearly state the grounds for disagreement and any supporting evidence.",
            ]),
            ("Panel Decision", [
                "The panel's decision on an appeal is final. The appeal process typically completes within 15 working days from the date of filing.",
            ]),
        ]),
        ("Confidentiality", [
            ("Personal Data", [
                "All performance information is strictly confidential. Disclosure of one's own or another employee's performance information to unauthorised parties is a breach of conduct.",
                "Access to performance data is on a need-to-know basis and is logged in the HRMS for audit purposes.",
            ]),
            ("Retention", [
                "Performance records are retained for the duration of employment and 5 years post separation, in line with the Records Retention section of the Data Security Policy.",
            ]),
        ]),
    ]
    _build(
        "Performance_Management_Policy.pdf",
        "Performance Management Policy",
        "HR-POL-006", "2.0", "April 2024",
        toc, sections,
    )


GENERATORS = [
    gen_leave_policy,
    gen_travel_policy,
    gen_medical_policy,
    gen_conduct_policy,
    gen_it_aup,
    gen_data_security,
    gen_expense,
    gen_procurement,
    gen_wfh,
    gen_performance,
]


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Generating policy PDFs in: {OUTPUT_DIR}")
    for gen in GENERATORS:
        gen()
    print(f"\nDone. {len(GENERATORS)} PDFs generated.")


if __name__ == "__main__":
    main()
