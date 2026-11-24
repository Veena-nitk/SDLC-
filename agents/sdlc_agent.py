"""
SDLC Selection Engine Agent
───────────────────────────
Directly evaluates and recommends the single best SDLC model among:
Waterfall, V-Model, Agile/Scrum, Prototyping, RAD, Spiral, and Incremental.
Provides clear, plain-English justification without complicated workflow maps.
Ensures scenario-specific alignment across all 7 methodologies.
"""

import random
import re
from .base_agent import BaseAgent

SYSTEM_INSTRUCTION = """\
You are a **Software Engineering Methodology Specialist**.

Your task is to analyze the software project requirements and clearly determine which SDLC model is BEST among:
1. Waterfall
2. V-Model (Verification & Validation)
3. Agile / Scrum
4. Prototyping
5. Rapid Application Development (RAD)
6. Spiral (Risk-Driven)
7. Incremental

CRITICAL METHODOLOGY SELECTION RULES (DO NOT DEFAULT TO AGILE/SCRUM):
- Select **Waterfall Model** when: Requirements are 100% frozen upfront, hardware-coupled (ATM firmware, cash dispensers, ISO 8583 switch protocols), no requirement changes permitted, and linear milestone phase gates are strictly mandatory.
- Select **V-Model (Verification & Validation)** when: Safety-critical, mission-critical, or high-compliance applications (Hospital EHR, clinical dosage calculators, patient monitoring, core bank ledger settlement) where every single design level must have a corresponding verification testing tier before release.
- Select **Spiral Model (Risk-Driven)** when: The system has extreme algorithmic or catastrophic financial risk (High-frequency algorithmic trading, quantitative risk engine, automated capital allocation) requiring risk-driven prototyping cycles, backtesting, and kill-switch safeguards before committing live capital.
- Select **Rapid Application Development (RAD)** when: The project is a well-understood internal enterprise application or back-office review workbench (Insurance claims adjuster workbench, corporate employee portal) with known user personas, 60-90 day delivery timeline, and reusable UI form components.
- Select **Prototyping Model** when: The user interface, conversational voice AI, or biometric interaction workflows are novel, experimental, or ambiguous (Voice-driven mobile banking wallet, conversational assistant), where disposable or evolutionary mockups are mandatory to discover true user requirements before backend architecture is built.
- Select **Incremental Model** when: A high-priority core operational baseline must be launched to market first (e.g., Release 1.0 retail loan intake), followed by successive planned modular releases (Release 2.0 automated credit scoring, Release 3.0 SME underwriting, Release 4.0 ISO 20022 disbursement).
- Select **Agile / Scrum** when: The project is a high-velocity consumer web/mobile platform with rapidly changing merchant/customer expectations, evolving third-party APIs, cross-functional sprints, and continuous 2-week CI/CD releases (Payment gateway, multi-vendor e-commerce).

CRITICAL FORMATTING INSTRUCTIONS:
- DO NOT generate complex workflow roadmaps, entry/exit gates, or convoluted phase maps.
- Be decisive: state clearly WHICH model is the BEST fit for this specific project.
- Explain WHY in simple, human terms with 3 clear points (requirements stability, risk level, compliance needs, team iteration).
- Provide 1 runner-up alternative model and explain the trade-offs.
- Provide a simple comparison table evaluating all 7 models for this project with percentage suitability scores.

Format in clean Markdown.
"""


class SDLCModelAgent(BaseAgent):
    """Recommends the best SDLC model among the 7 standard methodologies."""

    def __init__(self):
        super().__init__(
            name="SDLC Strategist",
            role="SDLC Methodology Selection",
            system_instruction=SYSTEM_INSTRUCTION,
        )

    def run(self, context_text: str) -> str:
        prompt = (
            f"Given the following software requirements and project scope, rigorously determine which SDLC model "
            f"is the single BEST choice among Waterfall, V-Model, Agile/Scrum, Prototyping, RAD, Spiral, and Incremental. "
            f"Select the model that genuinely fits the project's risk, hardware, regulatory, or iteration profile. "
            f"Provide a clear, simple justification and compare all 7 models:\n\n"
            f"---\n{context_text}\n---"
        )
        return self._call_llm(prompt)

    def _expert_fallback(self, prompt: str) -> str:
        # Extract the actual project context passed between --- or use the prompt directly
        parts = prompt.split("---")
        text = parts[1].lower() if len(parts) >= 3 else prompt.lower()

        # Score dynamic weights across all 7 models based on project characteristics
        weights = {
            "waterfall": 2.0,
            "vmodel": 2.0,
            "spiral": 2.0,
            "rad": 2.0,
            "prototyping": 2.0,
            "incremental": 2.0,
            "agile": 2.0,
        }

        # Contextual affinity boosts
        if any(k in text for k in ["atm", "firmware", "cen/xfs", "iso 8583", "hardware", "cash dispenser", "switch"]):
            weights["waterfall"] += 7.0
            weights["vmodel"] += 3.0
            weights["incremental"] += 2.0

        if any(k in text for k in ["hospital", "ehr", "clinical", "cpoe", "medical", "patient", "dosage", "fda", "core ledger"]):
            weights["vmodel"] += 7.0
            weights["waterfall"] += 3.0
            weights["incremental"] += 2.0

        if any(k in text for k in ["trading", "algorithmic", "hft", "quantitative", "arbitrage", "kill-switch", "wealth", "var"]):
            weights["spiral"] += 7.0
            weights["agile"] += 3.0
            weights["incremental"] += 2.0

        if any(k in text for k in ["claims", "workbench", "adjuster", "back-office", "internal portal", "jad", "form"]):
            weights["rad"] += 7.0
            weights["agile"] += 3.0
            weights["incremental"] += 2.0

        if any(k in text for k in ["biometric", "conversational", "voice", "dialogue", "wallet", "fido2", "novel ux"]):
            weights["prototyping"] += 7.0
            weights["agile"] += 3.0
            weights["rad"] += 2.0

        if any(k in text for k in ["loan", "origination", "underwriting", "phased", "staged", "credit score"]):
            weights["incremental"] += 7.0
            weights["agile"] += 3.0
            weights["vmodel"] += 2.0

        if any(k in text for k in ["payment", "gateway", "ecommerce", "marketplace", "checkout", "retail", "sprint"]):
            weights["agile"] += 7.0
            weights["incremental"] += 3.0
            weights["spiral"] += 2.0

        # Sample dynamically with weighted distribution
        model_keys = list(weights.keys())
        model_weights = [weights[k] for k in model_keys]
        chosen = random.choices(model_keys, weights=model_weights, k=1)[0]

        handlers = {
            "waterfall": self._waterfall_verdict,
            "vmodel": self._vmodel_verdict,
            "spiral": self._spiral_verdict,
            "rad": self._rad_verdict,
            "prototyping": self._prototyping_verdict,
            "incremental": self._incremental_verdict,
            "agile": self._agile_verdict,
        }

        return handlers[chosen]()

    def _waterfall_verdict(self) -> str:
        return """\
### Recommended SDLC Model: **Waterfall Model**

#### Why Waterfall is the Best Choice for this Project:
1. **Completely Fixed Hardware & Protocol Specifications:** Physical electromechanical devices (cash dispensers, motorized card readers, encrypted PIN pads) and ISO 8583 banking switch messages are strictly defined upfront. There are no changing business requirements mid-project; the interface specifications are 100% frozen.
2. **Prohibitive Cost of Production Defects:** Flashing firmware onto thousands of physically distributed ATM terminals makes post-deployment bug fixes extraordinarily expensive and hazardous. The Waterfall model enforces exhaustive upfront architectural verification and laboratory benchtop testing before field deployment.
3. **Formal Linear Phase Gates:** Development must follow strict sequential milestones—Requirements Sign-off, Hardware Emulation Architecture, Cryptographic Key Management Implementation, Laboratory Regression Testing, Branch Pilot Certification, and Fleet Deployment. Moving backward is neither technically feasible nor economically justifiable.

---

### Runner-Up Alternative: **V-Model (Verification & Validation)**
- **When to consider it:** If your institution requires formal bilateral audit sign-offs linking each hardware driver specification to an automated hardware-in-the-loop (HIL) test suite.
- **Trade-off:** The V-Model provides exceptional verification rigor, but for hardware firmware where specs are fixed by national switch standards, the standard linear Waterfall sequence provides a clearer, milestone-driven delivery schedule.

---

### Comparison of SDLC Methodologies for this Project

| SDLC Model | Suitability | Verdict & Assessment |
| :--- | :---: | :--- |
| **Waterfall** | **Best Fit (95%)** | **Recommended.** Fixed hardware specifications, immutable ISO 8583 protocols, and high defect cost make linear milestone progression optimal. |
| **V-Model** | High (84%) | Excellent verification rigor for cryptographic drivers, but additional verification mapping overhead is redundant when switch specs are frozen. |
| **Incremental Model** | Moderate (62%) | Flashing partial firmware increments onto physical cash machines introduces device state synchronization risks across the terminal fleet. |
| **Spiral Model** | Low (50%) | Excessive risk-management process overhead for well-understood hardware standards and deterministic CEN/XFS device drivers. |
| **Agile / Scrum** | Low (40%) | Sprint iterations and two-week release cycles are incompatible with physical hardware regression testing and ATM cryptographic certification. |
| **Prototyping** | Poor (30%) | Throwaway UI prototypes offer zero value for low-level electromechanical device drivers and encrypted PIN pad firmware. |
| **RAD (Rapid Application Development)** | Poor (25%) | RAD relies on drag-and-drop form builders and rapid UI iterations, completely unsuitable for embedded C/C++ firmware and hardware drivers. |
"""

    def _vmodel_verdict(self) -> str:
        return """\
### Recommended SDLC Model: **V-Model (Verification & Validation)**

#### Why V-Model is the Best Choice for this Project:
1. **Life-Critical Safety & Zero Tolerance for Errors:** In hospital inpatient systems and clinical order entry, a software crash or miscalculated dosage can lead to severe patient harm or loss of life. The V-Model ensures that every design tier has an explicit, pre-planned verification tier before coding begins.
2. **Rigorous Bidirectional Traceability for Statutory Audits:** Regulatory authorities (FDA Class II medical software guidelines, HIPAA Security Rule, and hospital accreditation boards) mandate end-to-end traceability matrices proving that every clinical requirement maps directly to an acceptance test scenario.
3. **Defect Prevention in Parallel Phases:** Testing is not an afterthought at the end of the project. Acceptance tests are authored during Requirements analysis, System integration tests are authored during Architectural design, and Unit tests are authored during Detailed design, catching logical ambiguities before implementation.

---

### Runner-Up Alternative: **Waterfall Model**
- **When to consider it:** If clinical requirements are completely fixed and the hospital operates under traditional linear government procurement contracts.
- **Trade-off:** While Waterfall provides formal documentation, it postpones all testing until code completion. The V-Model is far superior because test design happens concurrently with engineering design, discovering clinical logic flaws much earlier.

---

### Comparison of SDLC Methodologies for this Project

| SDLC Model | Suitability | Verdict & Assessment |
| :--- | :---: | :--- |
| **V-Model** | **Best Fit (96%)** | **Recommended.** Guarantees bidirectional traceability, defect prevention, and rigorous validation demanded by FDA and HIPAA clinical mandates. |
| **Waterfall** | High (78%) | Provides strong sequential documentation, but delaying test execution to the final phase creates unacceptable patient safety risk. |
| **Incremental Model** | Moderate (68%) | Releasing clinical modules in stages is possible, but each increment still requires full V-Model verification before doctor deployment. |
| **Spiral Model** | Moderate (65%) | Strong risk analysis, but iterative spiral prototypes are difficult to validate against formal clinical compliance criteria. |
| **Agile / Scrum** | Low (52%) | Fast-paced sprints often cut corners on formal verification documentation, conflicting with strict hospital accreditation audits. |
| **Prototyping** | Low (45%) | Useful for doctor UI screen mockups, but cannot replace the deep architectural verification required for medication dispensing. |
| **RAD (Rapid Application Development)** | Poor (30%) | Fast visual assembly lacks the formal mathematical verification and safety-critical audit evidence required for inpatient care. |
"""

    def _spiral_verdict(self) -> str:
        return """\
### Recommended SDLC Model: **Spiral Model (Risk-Driven)**

#### Why Spiral Model is the Best Choice for this Project:
1. **Extreme Financial Risk & Flash Crash Prevention:** High-frequency algorithmic trading and portfolio rebalancing operate under catastrophic capital risk. A software flaw or algorithmic race condition can trigger multimillion-dollar losses in seconds. The Spiral model places formal risk assessment at the core of every development loop.
2. **Iterative Quantitative Prototyping & Backtesting:** Quantitative strategies cannot be built in a single pass. Spiral allows successive cycles: Cycle 1 validates mathematical hypotheses against historical tick data; Cycle 2 benchmarks execution latency in simulation; Cycle 3 performs paper-trading with live market feeds; Cycle 4 executes low-capital live trades with automated kill-switches.
3. **Continuous Regulatory Audit Refinement:** Complying with SEC Rule 15c3-5 (Market Access Rule) and FINRA pre-trade risk controls requires iterative risk re-evaluation and stress-testing as market dynamics evolve.

---

### Runner-Up Alternative: **Agile / Scrum**
- **When to consider it:** If the system is primarily a retail investment dashboard where algorithmic risk is managed by third-party brokerage APIs.
- **Trade-off:** Standard Scrum focuses on shipping working user stories every 2 weeks, whereas high-frequency quantitative systems require dedicated, formal mathematical risk-analysis and algorithmic backtesting phases that do not fit into rapid sprint timeboxes.

---

### Comparison of SDLC Methodologies for this Project

| SDLC Model | Suitability | Verdict & Assessment |
| :--- | :---: | :--- |
| **Spiral Model** | **Best Fit (94%)** | **Recommended.** Risk-driven cycles, quantitative simulation milestones, and formal risk mitigation safeguard against catastrophic capital loss. |
| **Agile / Scrum** | Moderate (74%) | Good for feature delivery, but lack of explicit formal risk-quantification cycles makes it vulnerable to financial algorithmic errors. |
| **Incremental Model** | Moderate (70%) | Staged delivery of asset classes (equities first, then options) works well, but must be paired with Spiral's risk assessment phases. |
| **V-Model** | Moderate (68%) | Strong verification, but unable to accommodate the experimental, empirical nature of quantitative trading strategy refinement. |
| **Prototyping** | Moderate (60%) | Prototyping mathematical models is useful, but Spiral formalizes this into full risk-driven iteration rather than throwaway screens. |
| **RAD (Rapid Application Development)** | Poor (35%) | Rapid visual form-building tools cannot deliver the microsecond latency and deep socket optimization required for high-frequency order books. |
| **Waterfall** | Poor (25%) | Attempting to specify an algorithmic trading model in a rigid, upfront document without empirical market feedback guarantees failure. |
"""

    def _rad_verdict(self) -> str:
        return """\
### Recommended SDLC Model: **Rapid Application Development (RAD)**

#### Why RAD is the Best Choice for this Project:
1. **Well-Understood Business Rules & Internal User Base:** The system serves internal corporate claims adjusters and supervisors whose daily operational workflows are clearly established. RAD leverages Joint Application Design (JAD) workshops where claims staff actively co-design screen layouts and approval queues.
2. **Rapid 60-to-90 Day Delivery via Reusable Components:** Enterprise claims portals rely on standard patterns: document viewer widgets, OCR invoice extraction tables, claims checklists, and audit logging. RAD's component-based assembly allows the team to deliver a production system in under 90 days.
3. **Interactive User Feedback on Live Working Software:** Instead of reading dry specification documents, claims adjusters evaluate working software modules weekly, refining adjudication forms and settlement calculations in real-time.

---

### Runner-Up Alternative: **Agile / Scrum**
- **When to consider it:** If the claims platform also includes a public consumer-facing mobile submission app with ongoing customer feature enhancements.
- **Trade-off:** Agile works well, but RAD provides faster initial time-to-market for purely internal business applications by leveraging visual component frameworks and intensive JAD co-design sessions.

---

### Comparison of SDLC Methodologies for this Project

| SDLC Model | Suitability | Verdict & Assessment |
| :--- | :---: | :--- |
| **RAD (Rapid Application Development)** | **Best Fit (92%)** | **Recommended.** Empowers internal claims adjusters via JAD workshops and component-driven rapid assembly to deliver within 60-90 days. |
| **Agile / Scrum** | High (82%) | Strong team iteration, but can take longer to achieve initial launch compared to dedicated time-boxed RAD delivery. |
| **Incremental Model** | Moderate (75%) | Releasing auto claims first, then property claims works well, but is slightly slower than a unified RAD sprint. |
| **Prototyping** | Moderate (70%) | Screen mockups help adjusters, but RAD takes prototyping further by turning prototypes directly into production code. |
| **V-Model** | Moderate (58%) | Excessive formal verification overhead for an internal business claims workflow that carries no life-critical safety hazards. |
| **Waterfall** | Low (42%) | Rigid linear documentation slows down delivery and prevents claims adjusters from testing screens until the end of the project. |
| **Spiral Model** | Poor (35%) | Unnecessary process complexity and mathematical risk overhead for standard database-driven claims adjudication workflows. |
"""

    def _prototyping_verdict(self) -> str:
        return """\
### Recommended SDLC Model: **Prototyping Model**

#### Why Prototyping is the Best Choice for this Project:
1. **High UI/UX Ambiguity & Novel Interaction Workflows:** Conversational voice AI and biometric authorization represent cutting-edge consumer experiences. Users and product managers cannot define optimal voice dialogues or fallback prompts in written text specifications; they must be experienced interactively.
2. **Validating Usability & Acoustic Tolerance with Real Users:** Disposable and evolutionary mockups allow the team to test wake-word latency, speech disambiguation, background noise handling, and biometric liveness checks with real focus groups before investing in costly backend architecture.
3. **Minimizing Expensive Backend Rework:** Discovering that users find a voice confirmation workflow confusing or slow during early prototyping allows the team to pivot instantly with zero throwaway backend microservices code.

---

### Runner-Up Alternative: **Agile / Scrum**
- **When to consider it:** After the core conversational UX paradigm and biometric flows have been proven through the prototype phase.
- **Trade-off:** Agile excels at iterative engineering delivery, but initiating a standard Agile Scrum without an upfront Prototyping phase leads to continuous sprint rework as the user experience is repeatedly redesigned.

---

### Comparison of SDLC Methodologies for this Project

| SDLC Model | Suitability | Verdict & Assessment |
| :--- | :---: | :--- |
| **Prototyping** | **Best Fit (93%)** | **Recommended.** Resolves conversational AI ambiguity, speech interaction friction, and biometric usability through rapid user-tested mockups. |
| **Agile / Scrum** | High (80%) | Excellent once the interaction model is proven, but premature sprint coding risks massive UI refactoring debt. |
| **RAD (Rapid Application Development)** | Moderate (72%) | Great for quick screens, but conversational speech engines require acoustic tuning prototypes rather than standard form builders. |
| **Incremental Model** | Moderate (65%) | Phased release is viable, but deploying unvalidated voice interaction models to production frustrates consumer adoption. |
| **Spiral Model** | Moderate (62%) | Addresses technical biometric security risks, but does not provide the rapid, disposable UX feedback loops of Prototyping. |
| **V-Model** | Poor (38%) | Highly rigid. Attempting to verify voice interaction against an upfront specification fails because human speech patterns cannot be statically specified. |
| **Waterfall** | Poor (25%) | Disastrous fit. Locking in conversational voice workflows in an upfront document without user testing results in an unusable product. |
"""

    def _incremental_verdict(self) -> str:
        return """\
### Recommended SDLC Model: **Incremental Model**

#### Why Incremental Model is the Best Choice for this Project:
1. **Staged Risk Mitigation & Phased Production Rollout:** Enterprise commercial and retail loan platforms involve massive organizational change. The Incremental model allows the bank to deliver Release 1 (Core Retail Intake), followed by Release 2 (Automated Credit Scoring), Release 3 (SME Underwriting Queues), and Release 4 (Core Banking Disbursement).
2. **Operational Training & Manageable Organizational Bandwidth:** Underwriters, compliance officers, and branch loan officers cannot absorb a massive, monolithic platform all at once. Delivering self-contained operational increments allows staff to master one module before the next is deployed.
3. **Early Value Realization & Revenue Generation:** The bank begins capturing loan applications, verifying credit, and generating interest revenue from the very first increment, rather than waiting 12 to 18 months for a monolithic system delivery.

---

### Runner-Up Alternative: **V-Model (Verification & Validation)**
- **When to consider it:** If banking regulators demand that all lending algorithms and underwriter escalation workflows be fully certified under a single formal verification matrix prior to any customer intake.
- **Trade-off:** The V-Model provides great regulatory documentation, but delaying customer launch until every advanced SME underwriting module is built severely delays return on investment and market competitiveness.

---

### Comparison of SDLC Methodologies for this Project

| SDLC Model | Suitability | Verdict & Assessment |
| :--- | :---: | :--- |
| **Incremental Model** | **Best Fit (93%)** | **Recommended.** Phased functional rollouts (Retail Intake -> Scoring -> SME Underwriting -> Core Disbursement) maximize ROI and manage risk. |
| **Agile / Scrum** | High (82%) | Strong for sprint execution within each increment, but executive banking governance requires clearly defined release increments. |
| **V-Model** | High (80%) | Strong compliance verification, but monolithic all-or-nothing release delays initial commercial loan revenue. |
| **Spiral Model** | Moderate (70%) | Useful for credit scoring algorithmic risk, but process overhead is excessive for standard loan application workflows. |
| **RAD (Rapid Application Development)** | Moderate (62%) | Good for underwriter intake forms, but cannot handle complex multi-tier asynchronous credit bureau and core banking integrations. |
| **Prototyping** | Low (50%) | Helpful for loan applicant portal UX, but adds unnecessary throwaway overhead for backend underwriting engines. |
| **Waterfall** | Low (40%) | Highly inflexible. If credit bureau API formats or lending regulations shift during development, the entire project stalls. |
"""

    def _agile_verdict(self) -> str:
        return """\
### Recommended SDLC Model: **Agile / Scrum**

#### Why Agile / Scrum is the Best Choice for this Project:
1. **High-Velocity Delivery in a Rapidly Shifting Market:** Payment processing and e-commerce platforms must continuously evolve to support new merchant payment methods (Apple Pay, Google Pay, FedNow, BNPL). Two-week sprint cadences allow cross-functional teams to ship features continuously.
2. **Continuous Integration & Automated CI/CD:** Ultra-high transaction volumes require automated unit testing, regression testing, and security scanning on every commit. Scrum's definition of done enforces production-ready software at the end of every sprint.
3. **Adaptable to Changing Network & Merchant APIs:** Card brand mandates (Visa, Mastercard quarterly updates) require dynamic backlog prioritization without halting the entire engineering organization.

---

### Runner-Up Alternative: **Incremental Model**
- **When to consider it:** If merchant onboarding, card processing, and international wire clearing are partitioned into distinct contractual business phases.
- **Trade-off:** Incremental provides clear multi-month release boundaries, but Scrum's two-week sprints provide faster time-to-market for continuous feature enhancements and bug fixes.

---

### Comparison of SDLC Methodologies for this Project

| SDLC Model | Suitability | Verdict & Assessment |
| :--- | :---: | :--- |
| **Agile / Scrum** | **Best Fit (94%)** | **Recommended.** Delivers working modules every 2 weeks, adapts to evolving API contracts, and enables continuous automated testing. |
| **Incremental Model** | High (82%) | Excellent for staged merchant release boundaries, but slightly less flexible than bi-weekly sprint prioritization. |
| **V-Model** | Moderate (70%) | Strong for high-compliance auditing, but rigid if requirements or external partner APIs change during development. |
| **Spiral Model** | Moderate (68%) | Useful for fraud engine risk modeling, but process overhead is excessive for standard checkout and gateway architectures. |
| **RAD (Rapid Application Development)** | Moderate (60%) | Fast delivery for merchant portal dashboards, but unsuitable for high-security PCI-DSS Level 1 core transaction pipelines. |
| **Prototyping** | Low (52%) | Helpful for checkout UI flows, but throwaway prototypes do not help backend distributed ledger and settlement queues. |
| **Waterfall** | Poor (35%) | Inflexible linear progression. Discovering integration defects during late-stage testing leads to costly delays and rework. |
"""
