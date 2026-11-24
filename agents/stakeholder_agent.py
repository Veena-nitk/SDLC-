"""
Stakeholder Interaction & Clarification Agent
─────────────────────────────────────────────
Simulates adaptive stakeholder interviews, clarifies vague inputs,
and detects missing financial, security, and operational constraints.
"""

from .base_agent import BaseAgent

SYSTEM_INSTRUCTION = """\
You are a **Principal Financial Systems Business Analyst & Stakeholder Interaction Agent** 
with deep expertise in retail banking, payments, underwriting, and compliance.

Your task is to analyze the user's initial project description or scenario and:
1. Identify primary and secondary stakeholder groups (Business, Compliance, Security, Architecture, End-Users).
2. Generate role-tailored requirement clarification questions to eliminate ambiguity.
3. Highlight missing financial controls (e.g., transaction limits, audit retention, authentication factor thresholds).
4. Provide structured stakeholder interview findings ready to feed the Requirement Extraction Agent.

Adhere to IEEE 29148 stakeholder requirements elicitation practices. Format in clean, structured Markdown.
"""


class StakeholderInteractionAgent(BaseAgent):
    """Conducts adaptive stakeholder requirement elicitation and clarification."""

    def __init__(self):
        super().__init__(
            name="Stakeholder Interaction & Clarification Agent",
            role="Stakeholder Elicitation & Ambiguity Detection",
            system_instruction=SYSTEM_INSTRUCTION,
        )

    def run(self, scenario_description: str) -> str:
        prompt = (
            f"Analyze the following financial project description from multiple stakeholder perspectives "
            f"and formulate clarification questions and elicited constraints:\n\n"
            f"---\n{scenario_description}\n---"
        )
        return self._call_llm(prompt)

    def _expert_fallback(self, prompt: str) -> str:
        return """\
### 1. Stakeholder Group Matrix & Elicitation Scope

| Stakeholder Role | Primary Focus Area | Key Elicited Perspectives |
| :--- | :--- | :--- |
| **Product Owner & Business Ops** | Business value, conversion, throughput | Target customer segments, loan/transaction SLA, credit decision turn-around time (< 60s) |
| **CISO & InfoSec Team** | Confidentiality, integrity, threat protection | Zero-trust architecture, TLS 1.3, HSM-backed tokenization, step-up MFA, AES-256 at rest |
| **Chief Compliance Officer (CCO)** | Regulatory compliance & auditability | PCI-DSS v4.0, SOX 404, GDPR right-to-erasure, FinCEN AML/KYC automated reporting |
| **Chief Architect & DevOps** | Resilience, scalability, integration | 99.99% availability, RPO=0, RTO < 15 min, microservices, Kafka event streaming, legacy core banking connectors |
| **Auditor / Risk Committee** | Traceability & non-repudiation | Write-once read-many (WORM) audit logging, Segregation of Duties (SoD), change-control gates |

---

### 2. Context-Aware Clarification & Ambiguity Analysis

1. **Transaction Velocity & Scalability Bounds:**
   - *Clarification:* What are peak TPS (transactions per second) requirements and maximum allowable p99 latency during high-volume settlement windows?
   - *Resolution Target:* Baseline capacity defined at 5,000 TPS baseline, 25,000 TPS peak, sub-100ms response time.

2. **Step-Up Authentication & Risk-Based Step Thresholds:**
   - *Clarification:* What monetary transfer or loan disbursement threshold triggers mandatory secondary out-of-band verification?
   - *Resolution Target:* Transactions > $10,000 (or anomalous risk score > 75/100) require mandatory biometric / hardware token MFA.

3. **Legacy Core Banking Interoperability:**
   - *Clarification:* Are core banking accounting ledgers updated via batch EOD files (ACH/NACHA) or synchronous real-time ISO 20022 message APIs?
   - *Resolution Target:* Dual-mode: real-time ISO 20022 REST/gRPC events with end-of-day reconciliation batch sync.

4. **Data Retention & Sovereignty Constraints:**
   - *Clarification:* What are the exact geographical jurisdiction data-residency boundaries and statutory retention rules?
   - *Resolution Target:* Financial ledger records retained for 7 years (SOX/IRS); PII subject to GDPR right-to-erasure masking after account closure.
"""
