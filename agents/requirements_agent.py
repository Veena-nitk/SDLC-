"""
Requirements Engineering Agent
───────────────────────────────
Extracts clean, unambiguous functional and non-functional requirements
in plain English without complicated requirement IDs (no FR-001 or NFR-xxx codes).
Adheres to IEEE 830 recommendations while maintaining high legibility.
"""

from .base_agent import BaseAgent

SYSTEM_INSTRUCTION = """\
You are a **Senior Software Requirements Analyst**.

Your task is to take a software project description and produce a clean, professional,
and easy-to-read Software Requirements Specification (SRS) in plain English.

CRITICAL INSTRUCTIONS:
1. DO NOT USE ANY REQUIREMENT IDS (do NOT use FR-001, NFR-SEC-001, REQ-001, etc.).
   Make the requirements clean and readable for human stakeholders.
2. Structure the document clearly:
   - **System Overview & Purpose**: A concise description of what the system does.
   - **User Roles**: Key stakeholders and users of the system.
   - **Functional Features**: Clear, actionable bullet points describing what the system must do.
   - **Security, Performance & Reliability**: Clear operational expectations (e.g., encryption, uptime, response time).
   - **Key User Stories & Acceptance Criteria**: Written in simple "As a [role], I want [feature], so that [benefit]" with Given-When-Then criteria.

Format in clean, elegant Markdown. Keep language natural, direct, and unambiguous.
"""


class RequirementsAgent(BaseAgent):
    """Produces clean, human-readable requirements specifications without complex IDs."""

    def __init__(self):
        super().__init__(
            name="Requirements Analyst",
            role="Requirements Extraction & Specification",
            system_instruction=SYSTEM_INSTRUCTION,
        )

    def run(self, input_text: str) -> str:
        prompt = (
            f"Analyze the following software project and write a clean, readable requirements document "
            f"without using any requirement IDs or complex codes:\n\n"
            f"---\n{input_text}\n---"
        )
        return self._call_llm(prompt)

    def _expert_fallback(self, prompt: str) -> str:
        return """\
### 1. System Overview & Core Capabilities
The platform provides an automated, end-to-end digital processing and transaction workflow. It captures customer requests via web and mobile interfaces, runs automated identity verification, integrates with credit/external bureaus, evaluates financial risk, and manages automated fund disbursement or settlement with an immutable audit trail.

---

### 2. Primary User Roles
- **Customers & Applicants:** Submit applications, upload identity documents, review terms, and track transaction status.
- **Operations & Underwriters:** Review flagged applications, assess exceptions, and authorize disbursements.
- **Compliance & Legal Officers:** Oversee regulatory standards, monitor sanction watchlists, and handle dispute escalation.
- **System Administrators:** Monitor system health, manage user permissions, and ensure security policy enforcement.

---

### 3. Core Functional Requirements

#### User Registration & Identity Verification
- The system must capture applicant credentials, national identity cards, and proof of address.
- The system must verify biometric face liveness and perform optical character recognition (OCR) on uploaded identification documents within 15 seconds.
- The system must automatically cross-reference applicant details against international sanction watchlists, Politically Exposed Persons (PEP) lists, and fraud databases before granting approval.

#### Automated Assessment & Decision Engine
- The system must securely ingest credit bureau records, financial statements, and account history via authenticated APIs.
- The system must calculate real-time risk scores and automatically assign customers to the appropriate eligibility tier or pricing level.
- Applications with risk scores falling in the borderline range must be routed to human underwriter queues with an itemized risk breakdown.

#### Authentication & Transaction Security
- The system must require step-up Multi-Factor Authentication (biometric or hardware security token) whenever an applicant initiates a transaction or disbursement exceeding $10,000.
- All digital contracts and loan agreements must be signed with cryptographic e-signatures and time-stamped in an immutable audit log.

#### Payment Settlement & Notification
- Upon approved authorization, the system must trigger automated payment settlement through core banking payment rails (ISO 20022 / ACH).
- The system must dispatch automated confirmation notifications to the customer via SMS and email with transaction references.

---

### 4. Non-Functional Requirements

- **Data Security:** All customer sensitive data, payment information, and credit histories must be encrypted at rest using AES-256 and protected in transit using TLS 1.3 with mutual authentication.
- **Performance & Speed:** Transaction authorization and automated decisioning must complete within 200 milliseconds during standard load, with peak capacity supporting at least 5,000 requests per second.
- **System Availability:** The core service must achieve a minimum uptime of 99.99% with multi-region active-active cloud disaster recovery guaranteeing zero transactional data loss.
- **Auditability & Privacy:** All administrative actions and transaction state changes must be recorded in write-once audit logs retained for 7 years, with automated masking of customer personal identifiers.

---

### 5. Key User Story & Acceptance Criteria

**As a** retail customer  
**I want to** apply for and complete my financial request online  
**So that** I receive an instant automated decision and secure fund disbursement without visiting a branch.

**Acceptance Criteria:**
- **Given** an applicant has completed identity verification and uploaded valid documentation
- **When** the applicant submits their application
- **Then** the automated risk scoring engine evaluates the request within 30 seconds
- **And** if approved, an itemized agreement is generated for digital cryptographic signature
- **And** funds are automatically scheduled for settlement upon signature confirmation.
"""
