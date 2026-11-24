"""
Compliance, Security & Risk Analysis Agent
───────────────────────────────────────────
Maps requirements to major financial regulations (PCI-DSS, GDPR, SOX 404,
Basel III, AML/KYC), identifies regulatory compliance gaps, and produces
a quantified Risk Register (Likelihood x Impact).
"""

from .base_agent import BaseAgent
from knowledge_base.financial_regulations import FINANCIAL_REGULATIONS

SYSTEM_INSTRUCTION = """\
You are a **Chief Regulatory Compliance & Financial Risk Assessment Officer**
with credentials in CISA, CISSP, and CRMA.

Your responsibility is to analyze the extracted software requirements and:
1. Map each requirement to applicable statutory regulations and financial standards:
   - PCI-DSS v4.0 (Payment security, tokenization, access control)
   - GDPR (Articles 17, 25, 32 - Privacy by Design, Erasure, Data minimization)
   - SOX Section 404 (Internal financial controls, non-repudiation, audit trails)
   - Basel III / IV (Operational resilience, capital risk, BCBS 239)
   - FATF / FinCEN AML/KYC (Sanctions, PEP screening, Suspicious Activity Reports)
2. Identify Compliance Gaps and Mandatory Control Checkpoints.
3. Build a Quantitative Risk Register:
   - Risk ID, Threat Description, Likelihood (1-5), Impact (1-5), Severity Score (1-25)
   - Mitigation Controls
   - Human-in-the-Loop Sign-off requirements

Produce clear, audit-ready Markdown tables.
"""


class ComplianceRiskAgent(BaseAgent):
    """Evaluates regulatory compliance and constructs the financial risk register."""

    def __init__(self):
        super().__init__(
            name="Compliance, Security & Risk Analysis Agent",
            role="Regulatory Compliance Mapping & Financial Risk Assessment",
            system_instruction=SYSTEM_INSTRUCTION,
        )

    def run(self, requirements_text: str) -> str:
        prompt = (
            f"Analyze the following software requirements against financial regulations "
            f"(PCI-DSS v4.0, GDPR, SOX 404, Basel III, AML/KYC) and build a Compliance Matrix "
            f"and a Quantified Risk Register:\n\n"
            f"---\n{requirements_text}\n---"
        )
        return self._call_llm(prompt)

    def _expert_fallback(self, prompt: str) -> str:
        return """\
### 1. Regulatory Compliance Control Matrix

| Regulation / Standard | Mandatory Section | Enforced System Controls | Target Requirement | Audit Evidence Artifact |
| :--- | :--- | :--- | :--- | :--- |
| **PCI-DSS v4.0** | Req 3.4 & 3.5 | AES-256 encryption for cardholder data; FIPS 140-3 HSM key custody; CVV never stored post-auth. | NFR-SEC-001, FR-AUTH-004 | HSM key rotation certificates, database column encryption verification scans. |
| **PCI-DSS v4.0** | Req 8.3 | Mandatory step-up MFA for administrative, remote, and elevated financial operations. | FR-AUTH-004 | IAM MFA authentication audit logs, conditional access policy export. |
| **GDPR (EU) 2016/679** | Art 25 & 32 | Privacy-by-design, automated customer PII anonymization, right to erasure data purge pipelines. | NFR-PRIV-003, FR-ONB-001 | Data Protection Impact Assessment (DPIA), automated erasure test report. |
| **SOX Section 404** | Internal Controls | Double-entry ledger immutability, strict Segregation of Duties (SoD) between originator and approver. | FR-AUD-007, FR-DISB-005 | Change control board records, ledger checksum validation logs, SoD access matrices. |
| **FATF / FinCEN AML** | 31 CFR § 1020.220 | Real-time OFAC/PEP watchlist screening; automated threshold detection (> $10k) with SAR escalation. | FR-AML-002, FR-DISB-005 | Watchlist screening engine configuration logs, FinCEN SAR filing queue audit records. |
| **Basel III (BCBS 239)** | Operational Risk | Multi-region active-active disaster recovery (RPO=0, RTO < 15 min), automated real-time exposure monitoring. | NFR-AVAIL-001, NFR-AVAIL-002 | Annual disaster recovery failover drill sign-off, live telemetry uptime reports. |

---

### 2. Financial Threat & Risk Register

| Risk ID | Threat Scenario | L (1-5) | I (1-5) | Score (L×I) | Risk Level | Mitigation Strategy | Human Approval Gate |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **RSK-001** | Account Takeover (ATO) / Credential Stuffing on High-Value Disbursements | 3 | 5 | **15** | **High** | Mandatory FIDO2 / Biometric step-up MFA, device fingerprinting, velocity checks. | CISO Security Sign-off |
| **RSK-002** | Unsanctioned Ledger Tampering / Internal Fraud | 2 | 5 | **10** | **High** | Write-Once-Read-Many (WORM) cryptographic ledger hashing, strict Segregation of Duties (SoD). | Internal Audit Committee |
| **RSK-003** | Sanction Screening Failure (False Negative on Specially Designated Nationals) | 2 | 5 | **10** | **High** | Daily automated sync with OFAC/UN/EU watchlists; secondary manual review for fuzzy score > 0.80. | Chief Compliance Officer (CCO) |
| **RSK-004** | Core Banking API Outage / Network Partition During Peak Clearing Window | 3 | 4 | **12** | **High** | Resilient asynchronous Kafka queue buffering with idempotent consumer retries. | Lead Infrastructure Architect |
| **RSK-005** | Unauthorized PII Exposure in Log Files / Telemetry | 3 | 4 | **12** | **High** | Automated regex data scrubber in log pipelines before routing to SIEM / Elasticsearch. | Data Protection Officer (DPO) |

*Scoring Criteria: Low (1–4), Medium (5–9), High (10–19), Critical (20–25).*
"""
