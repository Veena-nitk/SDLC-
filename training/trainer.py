"""
Agent Training & Knowledge Fine-Tuning Manager
──────────────────────────────────────────────
Manages custom requirement datasets, enterprise guardrails, few-shot in-context
training exemplars, and fine-tuning dataset export (JSONL) for Agentic AI.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

TRAINING_DIR = Path(__file__).parent.parent / "training_data"
TRAINING_DIR.mkdir(exist_ok=True, parents=True)

GOLDEN_EXAMPLES_FILE = TRAINING_DIR / "golden_examples.json"
CUSTOM_RULES_FILE = TRAINING_DIR / "custom_rules.json"


# Default high-assurance training examples for financial software
DEFAULT_GOLDEN_EXAMPLES = [
    {
        "id": "TRAIN-EX-001",
        "domain": "Loan Origination & Underwriting",
        "input_scenario": "Digital SME credit scoring and instant loan underwriting platform with core banking integration.",
        "expected_requirements": [
            "FR-001: The system SHALL ingest borrower financial statements and credit bureau telemetry to compute debt-service coverage ratio (DSCR).",
            "FR-002: For loans exceeding $50,000, the system SHALL mandate secondary underwriter manual review before dispatching ISO 20022 settlement.",
            "NFR-SEC-001: All borrower tax identifiers and bank statements SHALL be encrypted using AES-256 with keys in FIPS 140-3 HSM.",
            "NFR-AVAIL-001: System SHALL provide 99.99% availability with zero transactional data loss (RPO = 0)."
        ],
        "expected_sdlc": "Agile-DevSecOps Hybrid",
        "justification": "Requires rapid iteration on credit ML models combined with automated compliance and security verification gates.",
        "added_on": "2026-11-14T20:00:00Z"
    },
    {
        "id": "TRAIN-EX-002",
        "domain": "Payment Gateway & Settlement",
        "input_scenario": "Ultra-low-latency card payment processor with instant fraud detection and tokenization.",
        "expected_requirements": [
            "FR-001: The system SHALL validate card tokens and execute 3D Secure 2.0 biometric challenge for transactions > $500.",
            "FR-002: Real-time fraud scoring SHALL evaluate velocity and geofence within 15 milliseconds per transaction.",
            "NFR-PERF-001: Processing throughput SHALL support 25,000 TPS with sub-50ms latency at p99.",
            "NFR-AUD-001: An immutable, cryptographically chained audit record SHALL be written for every debit/credit."
        ],
        "expected_sdlc": "DevSecOps with Formal Verification Gates",
        "justification": "High transaction concurrency and strict PCI-DSS Level 1 compliance require automated security testing in CI/CD.",
        "added_on": "2026-11-14T20:00:00Z"
    }
]

DEFAULT_CUSTOM_RULES = [
    {
        "rule_id": "RULE-FIN-001",
        "title": "Dual-Control Segregation of Duties (SoD)",
        "constraint": "Any transaction or disbursement exceeding $25,000 requires separate originator and approver credentials.",
        "mandatory": True
    },
    {
        "rule_id": "RULE-FIN-002",
        "title": "FIPS 140-3 Cryptographic Custody",
        "constraint": "Primary Account Numbers (PAN) and biometric vectors must never be decrypted in plaintext outside HSM enclave.",
        "mandatory": True
    },
    {
        "rule_id": "RULE-FIN-003",
        "title": "Audit Trail WORM Immutability",
        "constraint": "Audit logs must be written to Write-Once-Read-Many storage with NTP synchronized timestamps and SHA-256 chain hashing.",
        "mandatory": True
    }
]


class AgentTrainingStudio:
    """Manages training data, few-shot prompt injection, and fine-tuning exports."""

    def __init__(self):
        self._init_storage()

    def _init_storage(self):
        if not GOLDEN_EXAMPLES_FILE.exists():
            with open(GOLDEN_EXAMPLES_FILE, "w") as f:
                json.dump(DEFAULT_GOLDEN_EXAMPLES, f, indent=2)

        if not CUSTOM_RULES_FILE.exists():
            with open(CUSTOM_RULES_FILE, "w") as f:
                json.dump(DEFAULT_CUSTOM_RULES, f, indent=2)

    def get_golden_examples(self) -> List[Dict[str, Any]]:
        try:
            with open(GOLDEN_EXAMPLES_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_GOLDEN_EXAMPLES

    def get_custom_rules(self) -> List[Dict[str, Any]]:
        try:
            with open(CUSTOM_RULES_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_CUSTOM_RULES

    def add_golden_example(
        self,
        domain: str,
        input_scenario: str,
        expected_requirements: List[str],
        expected_sdlc: str,
        justification: str,
    ) -> Dict[str, Any]:
        examples = self.get_golden_examples()
        new_id = f"TRAIN-EX-{len(examples) + 1:03d}"
        example = {
            "id": new_id,
            "domain": domain,
            "input_scenario": input_scenario,
            "expected_requirements": expected_requirements,
            "expected_sdlc": expected_sdlc,
            "justification": justification,
            "added_on": datetime.utcnow().isoformat() + "Z",
        }
        examples.append(example)
        with open(GOLDEN_EXAMPLES_FILE, "w") as f:
            json.dump(examples, f, indent=2)
        return example

    def add_custom_rule(self, title: str, constraint: str, mandatory: bool = True) -> Dict[str, Any]:
        rules = self.get_custom_rules()
        new_id = f"RULE-FIN-{len(rules) + 1:03d}"
        rule = {
            "rule_id": new_id,
            "title": title,
            "constraint": constraint,
            "mandatory": mandatory,
        }
        rules.append(rule)
        with open(CUSTOM_RULES_FILE, "w") as f:
            json.dump(rules, f, indent=2)
        return rule

    def build_few_shot_prompt_context(self) -> str:
        """Constructs in-context training exemplars to dynamically teach the agents."""
        examples = self.get_golden_examples()
        rules = self.get_custom_rules()

        rule_bullets = "\n".join([f"- **[{r['rule_id']}] {r['title']}:** {r['constraint']}" for r in rules])
        
        exemplar_blocks = []
        for ex in examples[:3]:  # Top exemplars
            reqs = "\n  ".join(ex["expected_requirements"])
            exemplar_blocks.append(
                f"### Learned Benchmark Example: {ex['domain']}\n"
                f"- Input Scenario: {ex['input_scenario']}\n"
                f"- Ideal Extracted Requirements:\n  {reqs}\n"
                f"- Target SDLC Model: {ex['expected_sdlc']} ({ex['justification']})"
            )

        exemplars_text = "\n\n".join(exemplar_blocks)

        return (
            f"## Mandatory Enterprise Financial Guardrails (Trained Rules):\n"
            f"{rule_bullets}\n\n"
            f"## In-Context Golden Training Exemplars:\n"
            f"{exemplars_text}\n"
        )

    def export_fine_tuning_jsonl(self, output_path: Path) -> int:
        """
        Exports the dataset into JSONL format compatible with Gemini Fine-Tuning
        and OpenAI / HuggingFace tuning pipelines.
        """
        examples = self.get_golden_examples()
        rules = self.get_custom_rules()
        system_msg = (
            "You are an expert Financial Requirements & SDLC Selection Agent compliant with "
            "IEEE Std 830, PCI-DSS v4.0, GDPR, SOX 404, and Basel III standards."
        )

        count = 0
        with open(output_path, "w") as f:
            for ex in examples:
                reqs_str = "\n".join(ex["expected_requirements"])
                row = {
                    "messages": [
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": f"Elicit requirements and recommend SDLC for: {ex['input_scenario']}"},
                        {"role": "model", "content": f"### Functional & Security Requirements:\n{reqs_str}\n\n### Recommended SDLC:\n{ex['expected_sdlc']} - {ex['justification']}"}
                    ]
                }
                f.write(json.dumps(row) + "\n")
                count += 1
        return count
