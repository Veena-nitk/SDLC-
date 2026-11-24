"""
Financial & Enterprise Domain Scenarios Knowledge Base
───────────────────────────────────────────────────────
Comprehensive scenarios, statutory standards, and regulatory controls.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class RegulationControl:
    regulation: str
    section: str
    title: str
    description: str
    mandatory_controls: List[str]
    audit_evidence: str
    severity: str


FINANCIAL_REGULATIONS: Dict[str, RegulationControl] = {
    "PCI-DSS-4.0-REQ3": RegulationControl(
        regulation="PCI-DSS v4.0",
        section="Requirement 3",
        title="Protect Stored Account Data",
        description="Cardholder data (PAN, CVV, PIN) must be encrypted at rest using AES-256 with keys in FIPS 140-3 HSM.",
        mandatory_controls=[
            "Never store sensitive authentication data (CVV/PIN) after authorization",
            "Mask PAN when displayed (show only first 6 and last 4 digits)",
            "Automated data purging policy for cardholder data past retention date",
        ],
        audit_evidence="Key rotation logs, database column encryption verification scans",
        severity="Critical",
    ),
    "PCI-DSS-4.0-REQ8": RegulationControl(
        regulation="PCI-DSS v4.0",
        section="Requirement 8",
        title="Identify Users and Authenticate Access",
        description="Enforce Multi-Factor Authentication (MFA) for administrative and remote access to financial environments.",
        mandatory_controls=[
            "Enforce Multi-Factor Authentication across all administrative access",
            "Automatic session timeout after 15 minutes of inactivity",
        ],
        audit_evidence="IAM policies, MFA authentication logs",
        severity="Critical",
    ),
    "GDPR-ART25": RegulationControl(
        regulation="GDPR (EU) 2016/679",
        section="Article 25 & 32",
        title="Privacy by Design and Security of Processing",
        description="Implement appropriate technical measures such as pseudonymization, encryption, and erasure workflows.",
        mandatory_controls=[
            "Data minimization: collect only strictly necessary financial data",
            "Right to erasure (Article 17) automated deletion workflows",
        ],
        audit_evidence="Data Protection Impact Assessment (DPIA), data deletion test runs",
        severity="High",
    ),
    "SOX-SEC404": RegulationControl(
        regulation="Sarbanes-Oxley Act (SOX)",
        section="Section 404",
        title="Internal Controls for Financial Reporting",
        description="Ensure financial transactions and ledger records enforce strict Segregation of Duties and immutability.",
        mandatory_controls=[
            "Strict Segregation of Duties (SoD) between transaction creation and approval",
            "Immutable double-entry ledger bookkeeping with write-once audit records",
        ],
        audit_evidence="Ledger reconciliation reports, change ticket approval records",
        severity="Critical",
    ),
    "BASEL-III-OPRISK": RegulationControl(
        regulation="Basel III / IV Framework",
        section="BCBS 239",
        title="Operational Risk & Resilience",
        description="Financial transaction architectures must guarantee operational resilience (RPO < 15 min, RTO < 1 hour).",
        mandatory_controls=[
            "Active-Active or High-Availability multi-region deployment",
            "Real-time liquidity and exposure monitoring",
        ],
        audit_evidence="Disaster recovery runbook, uptime dashboards (99.99%)",
        severity="High",
    ),
    "AML-KYC-FATF": RegulationControl(
        regulation="FATF / FinCEN AML Regulations",
        section="Bank Secrecy Act / USA PATRIOT Act",
        title="Anti-Money Laundering & Customer Due Diligence",
        description="Verify identity of customer, screen against OFAC / PEP watchlists, and flag suspicious transactions.",
        mandatory_controls=[
            "Automated government-ID verification and biometric liveness during KYC",
            "Real-time screening against global Sanctions and PEP lists",
            "Suspicious Activity Report (SAR) queue with mandatory compliance review",
        ],
        audit_evidence="KYC audit logs, watchlist screening engine version records",
        severity="Critical",
    ),
    "PCI-PTS-ATM": RegulationControl(
        regulation="PCI PTS v6.0 / CEN-XFS",
        section="Device Security Standards",
        title="Physical Hardware & ATM Key Management",
        description="ATM firmware cryptographic controls and CEN/XFS device drivers for physical hardware peripherals.",
        mandatory_controls=[
            "Dual-Control Split Knowledge key loading for Encrypted PIN Pads",
            "DUKPT (Derived Unique Key Per Transaction) or Master/Session Triple-DES encryption",
            "Hardware tamper detection with automated cryptographic memory zeroization",
        ],
        audit_evidence="Lab security evaluation reports, key loading dual-custody logs",
        severity="Critical",
    ),
    "FDA-HIPAA-CLINICAL": RegulationControl(
        regulation="FDA / HIPAA Security Rule",
        section="45 CFR Part 160 & 164 / 21 CFR Part 820",
        title="Clinical Software Verification & Patient Privacy",
        description="Verification and validation of clinical order entry, electronic records, and Protected Health Information.",
        mandatory_controls=[
            "Rigorous bidirectional traceability matrix from clinical requirements to acceptance test plans",
            "Emergency break-the-glass audit trails for physician clinical overrides",
            "End-to-end encryption for HL7 FHIR diagnostic APIs",
        ],
        audit_evidence="Design History File (DHF), Verification and Validation test summary reports",
        severity="Critical",
    ),
}

# ─────────────────────────────────────────────────────────────
# 7 Core Scenarios (Demonstrating All 7 SDLC Methodologies)
# ─────────────────────────────────────────────────────────────

SAMPLE_FINANCIAL_SCENARIOS = {
    "atm_firmware": {
        "title": "ATM Fleet Terminal Firmware & ISO 8583 Switch Upgrade",
        "sdlc_model": "Waterfall Model",
        "description": (
            "Develop embedded firmware and host communication software for a national fleet of 5,000 automated teller machines (ATMs). "
            "The system interfaces with physical electromechanical peripherals (cash dispenser, motorized card reader, encrypted PIN pad, "
            "receipt printer, and depository module) via the CEN/XFS 3.30 hardware standard. Transactions are encoded in the rigid "
            "ISO 8583 financial switching format and routed to the central bank network via encrypted TCP/IP tunnels. All PIN entry and "
            "cryptographic key storage must strictly adhere to PCI PTS v6.0 and Triple-DES/AES DUKPT key management. Requirements are "
            "100% frozen upfront by the central switch protocol and hardware specifications. Zero mid-project requirement changes are "
            "permitted, requiring exhaustive sequential milestone phase gates before physical firmware flashing."
        ),
    },
    "hospital_ehr": {
        "title": "Hospital Inpatient Electronic Health Records & Clinical Order Entry System",
        "sdlc_model": "V-Model (Verification & Validation)",
        "description": (
            "Develop a mission-critical hospital inpatient electronic health records (EHR) and computerized physician order entry (CPOE) "
            "platform integrating with bedside smart pumps and pharmacy medication dispensing cabinets. The platform handles patient "
            "admission, clinical physician notes, diagnostic lab orders, and automated dosage calculations with zero tolerance for medical "
            "or medication errors. Every single requirement tier (system specification, subsystem architecture, module design) requires "
            "formal verification against a corresponding testing tier (unit testing, integration testing, system testing, clinical acceptance "
            "testing) before commissioning. Must strictly comply with HIPAA Security Rule, HL7 FHIR standards, and FDA medical software validation."
        ),
    },
    "wealth_trading": {
        "title": "High-Frequency Algorithmic Wealth Management & Quantitative Risk Engine",
        "sdlc_model": "Spiral Model (Risk-Driven)",
        "description": (
            "Build an ultra-low-latency algorithmic securities trading and automated portfolio rebalancing platform operating under high "
            "financial exposure. The system ingests microsecond market ticker data, executes proprietary quantitative statistical arbitrage "
            "strategies, and calculates real-time Value-at-Risk (VaR) across derivative portfolios. Due to extreme technical and financial "
            "risks (flash crash vulnerability, execution race conditions, catastrophic capital loss), development must proceed in risk-driven "
            "spiral iterations where each cycle performs deep risk assessment, algorithmic stress-testing, and backtesting simulation before "
            "deploying live capital. Must implement automated pre-trade risk firewalls and emergency kill-switches per SEC Rule 15c3-5 and FINRA audits."
        ),
    },
    "insurance_claims": {
        "title": "Corporate Insurance Claims Adjudication & Adjuster Review Workbench",
        "sdlc_model": "Rapid Application Development (RAD)",
        "description": (
            "Build an internal back-office claims adjudication and fraud investigation workbench for 300 internal corporate claims adjusters. "
            "The system handles property, casualty, and commercial claim folders, integrating with legacy mainframe policy databases to display "
            "claimant documentation, invoice OCR extracts, and adjusters' settlement calculations. Because the user personas (claims adjusters, "
            "supervisors) are well-known internal employees and business rules are clearly established, the system must be delivered rapidly "
            "within 60 days using rapid prototyping, visual UI form builders, and collaborative joint application design (JAD) workshops. "
            "Must enforce Segregation of Duties (SoD) under SOX 404 for claims exceeding $50,000."
        ),
    },
    "biometric_wallet": {
        "title": "Conversational AI & Biometric FinTech Mobile Wallet",
        "sdlc_model": "Prototyping Model",
        "description": (
            "Develop a next-generation consumer mobile financial wallet centered around an interactive conversational voice AI assistant "
            "and biometric payment authorization. Users initiate peer-to-peer payments, bill splitting, and balance inquiries through "
            "natural voice dialogues, authenticated via facial recognition and vocal biometric prints. Because the conversational user experience "
            "and vocal interaction workflows are highly novel and user expectations are ambiguous, development requires rapid interactive "
            "UI/UX prototyping. The team must build and evaluate throwaway voice interaction models and mock user interfaces with focus groups "
            "to validate user workflows before locking down backend microservices architecture. Must adhere to FIDO2 WebAuthn and GDPR Article 9."
        ),
    },
    "loan_origination": {
        "title": "Automated Commercial & Retail Loan Origination Platform",
        "sdlc_model": "Incremental Model",
        "description": (
            "Develop an enterprise digital loan origination and underwriting system for a commercial bank. The project must be rolled out in "
            "phased, self-contained functional increments to manage operational risk and organizational rollout: Increment 1 delivers the core "
            "applicant intake portal and basic retail loan calculators; Increment 2 adds automated credit bureau integration (Experian, TransUnion) "
            "and algorithmic risk scoring; Increment 3 introduces commercial SME underwriting workflows and underwriter escalation queues (> $250,000); "
            "Increment 4 delivers cryptographic digital contract execution and automated ISO 20022 core banking disbursement. Each increment is "
            "fully tested, deployed, and operational in production before the next module begins. Must comply with SOX 404 controls, FCRA, and GDPR."
        ),
    },
    "payment_gateway": {
        "title": "Omnichannel Payment Processing Gateway & Merchant Checkout Engine",
        "sdlc_model": "Agile / Scrum",
        "description": (
            "Build a high-volume omnichannel payment gateway processing 25,000 transactions per second (TPS) for web and mobile merchants. "
            "The system must support credit/debit card processing, instant bank transfers (FedNow / SEPA Instant), merchant SDKs, and dynamic "
            "merchant fee calculation. The platform operates in a fast-moving competitive market with continuously evolving merchant requirements, "
            "frequent API updates from payment card networks (Visa, Mastercard), and weekly feature enhancements. Development requires two-week "
            "sprint iterations, cross-functional engineering teams, continuous automated CI/CD deployment pipelines, and sprint demo reviews. "
            "Must maintain PCI-DSS v4.0 Level 1 compliance, ISO 20022 messaging, and 99.999% uptime."
        ),
    },
    "digital_banking": {
        "title": "Omnichannel Digital Banking & KYC Onboarding Platform",
        "sdlc_model": "Incremental Model",
        "description": (
            "Build a secure omnichannel retail digital banking platform with customer onboarding, account opening, account management, "
            "and fund transfers. New customers register via mobile with OCR extraction of passport/driver's license, liveness detection, "
            "and automated sanctions/PEP screening. Features are rolled out in scheduled increments: Release 1 accounts, Release 2 transfers, "
            "Release 3 loans and bill pay. The platform must implement end-to-end encryption, step-up MFA, and Open Banking APIs."
        ),
    },
    "ecommerce_marketplace": {
        "title": "Multi-Vendor E-Commerce Marketplace with Real-Time Inventory & Checkout",
        "sdlc_model": "Agile / Scrum",
        "description": (
            "Build a high-volume multi-vendor online marketplace supporting merchant product catalogs, shopping cart management, "
            "real-time distributed inventory locking during flash sales, customer order tracking, and split-escrow payments to vendors. "
            "Operates with bi-weekly agile sprints to continuously ship buyer promotional tools and vendor dashboards."
        ),
    },
}
