# Project Proposal & Requirement Analysis Submission (For TA / Instructor Review)

**Subject:** Project Architecture, Tech Stack & Requirements Specification Review — Financial Agentic-AI System

**Dear Teaching Assistant / Instructor,**

Please find below our project overview, technology stack, and initial requirement analysis for our **Agentic AI–based LLM System for Automated Requirement Gathering, Analysis, and SDLC Identification in the Financial Sector**.

We have attached the generated **IEEE Std 830-1998 Software Requirements Specification & SDLC Strategy Report (PDF)** for your formal review.

---

### 1. Executive Summary & Problem Scope
Financial institutions operate under strict statutory regulations (PCI-DSS v4.0, SOX Section 404, GDPR, Basel III/IV, and FATF AML/KYC) and high security sensitivity. Traditional manual requirements engineering in banking is time-consuming, prone to ambiguities, inconsistent, and frequently misses regulatory controls.

Our solution designs and develops a **Collaborative Multi-Agent LLM Platform** that autonomously interacts with financial stakeholder perspectives, extracts structured IEEE 830 / ISO/IEC/IEEE 29148 requirements, maps statutory compliance obligations, generates UML system architecture diagrams, and executes a Multi-Criteria Decision Analysis (MCDA) engine to recommend and customize the optimal SDLC model (e.g., Agile-DevSecOps Hybrid).

---

### 2. Multi-Agent System Architecture

The platform comprises specialized collaborative agents coordinated by a central orchestrator:

1. **Coordinator & Governance Agent:** Manages inter-agent blackboard state, audit trails, and mandatory Human-in-the-Loop (HITL) validation checkpoints.
2. **Stakeholder Interaction & Clarification Agent:** Simulates role-tailored interviews across Business, CISO/Security, Compliance (CCO), and Systems Architecture; detects ambiguous parameters and missing constraints.
3. **Requirements Engineering & Classification Agent:** Produces atomic, testable Functional (FR) and Non-Functional (NFR: Security, Performance, Availability, Auditability) requirements with MoSCoW prioritization and Gherkin (Given-When-Then) acceptance criteria.
4. **Compliance, Security & Risk Analysis Agent:** Cross-references requirements against regulatory controls (PCI-DSS v4.0, GDPR Art 17/25/32, SOX 404, Basel III BCBS 239) and builds a quantitative Risk Register (Likelihood × Impact).
5. **UML Diagrams & Modeling Agent:** Synthesizes standard Mermaid UML models (Use Case, Domain Class, High-Value Transaction Sequence, Activity/State Machine, Component Topology).
6. **SDLC Selection Engine Agent:** Employs a hybrid Multi-Criteria Decision Analysis (MCDA) mathematical model to score and rank SDLC methodologies (Agile-DevSecOps, V-Model, Spiral, Waterfall) and generates a phase-by-phase workflow with entry/exit gates and compliance checks.

---

### 3. Complete Technology Stack

| Layer | Technology / Framework | Role & Justification |
| :--- | :--- | :--- |
| **Language & Runtime** | Python 3.14 (Virtual Environment) | Robust ecosystem for AI orchestration and document processing. |
| **LLM Reasoning Engine** | Google Gemini 2.0 Flash (`google-genai` SDK) | Low latency, 1M token context window, state-of-the-art reasoning. |
| **Fallback Engine** | Deterministic Financial Domain Expert System | Guarantees 100% reliable execution and auditability when offline. |
| **Multi-Agent Orchestrator** | Custom Sequential & Selective Pipeline | Centralized state management, audit logging, and Human-in-the-Loop checkpoints. |
| **Knowledge Base** | Embedded Financial Regulations Registry | Formal definitions of PCI-DSS v4.0, GDPR, SOX 404, Basel III, AML/KYC. |
| **Decision Analysis** | Multi-Criteria Decision Analysis (MCDA) | Mathematical weighted scoring matrix evaluating 6 critical risk factors. |
| **Diagram Modeling** | Mermaid UML Engine | High-precision Use Case, Class, Sequence, State, and Component diagrams. |
| **Document & PDF Publishing**| ReportLab 5.1.0 + Pillow | Publication-grade IEEE 830 PDF generation with running headers and sign-offs. |
| **CLI & User Interface** | Rich 15.0 | Interactive terminal UI with color-coded stage panels and progress spinners. |

---

### 4. Attached Artifacts & Verification
1. **IEEE 830 Software Requirements Specification (PDF):** `loan_origination_srs.pdf`
2. **Consolidated Markdown Specification:** `loan_origination_srs.md`
3. **Codebase Repository:** `~/.gemini/antigravity/scratch/sdlc-agents/`

---

### 5. Questions for TA / Instructor Feedback
We would appreciate your feedback on the following aspects:
1. Are there specific additional financial compliance frameworks (e.g., FFIEC, PSD2/Open Banking, or ISO 20022) you would like us to explicitly incorporate into the automated compliance verification matrix?
2. Does the current 5-agent decomposition meet your requirements, or would you recommend further separating any agent (e.g., separating Security from Compliance)?
3. For the final evaluation phase, are there particular benchmarks or metrics (e.g., hallucination rate, extraction precision/recall against gold-standard SRS) you want us to emphasize?

Thank you for your guidance and review!

**Best regards,**  
[Your Name / Team Members]  
[Course Name & ID]  
[University / Institution]
