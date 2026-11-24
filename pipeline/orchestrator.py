"""
Multi-Agent Financial System Orchestrator with RAG
─────────────────────────────────────────────────
Executes the collaborative pipeline across requirements, RAG compliance,
UML modeling, and SDLC methodology selection.
Produces clean, human-readable outputs without complex requirement IDs.
"""

from typing import Dict, Any, Callable, Optional, List
from datetime import datetime

from agents import (
    CoordinatorAgent,
    StakeholderInteractionAgent,
    RequirementsAgent,
    ComplianceRiskAgent,
    SDLCModelAgent,
    UMLDiagramAgent,
)
from training.trainer import AgentTrainingStudio
from rag.retriever import FinancialRAGRetriever


class FinancialAgentOrchestrator:
    """Coordinates the 5-agent pipeline with RAG knowledge grounding."""

    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.stakeholder_agent = StakeholderInteractionAgent()
        self.requirements_agent = RequirementsAgent()
        self.compliance_agent = ComplianceRiskAgent()
        self.uml_agent = UMLDiagramAgent()
        self.sdlc_agent = SDLCModelAgent()
        self.training_studio = AgentTrainingStudio()
        self.rag_retriever = FinancialRAGRetriever()

    def run_pipeline(
        self,
        project_title: str,
        project_description: str,
        on_stage_update: Optional[Callable[[int, str, str], None]] = None,
    ) -> Dict[str, Any]:
        """
        Executes the collaborative 5-agent workflow:
          Agent 1: Requirements Analyst (Extraction without complex IDs)
          Agent 2: Compliance Specialist (RAG-grounded regulatory mapping)
          Agent 3: System Architect (UML Use Case, Class, Sequence, State)
          Agent 4: SDLC Strategist (Evaluates best among Waterfall, V, Agile, RAD, Spiral, Incremental)
          Agent 5: Documentation Lead (Compiles official SRS document & PDF)
        """
        results = {
            "title": project_title,
            "description": project_description,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "stages": {},
            "retrieved_evidence": [],
        }

        # Step 0: Query RAG for statutory standards matching this project
        retrieved_chunks = self.rag_retriever.retrieve(project_description, top_k=3)
        evidence_text = self.rag_retriever.format_retrieved_evidence(retrieved_chunks)
        results["retrieved_evidence"] = retrieved_chunks

        # Agent 1: Requirements Engineering (without IDs)
        if on_stage_update:
            on_stage_update(1, "Requirements Analyst", "Extracting functional specifications and non-functional requirements...")
        req_input = (
            f"Project Title: {project_title}\n"
            f"Scope Description: {project_description}\n\n"
            f"Relevant Statutory Evidence (RAG):\n{evidence_text}"
        )
        requirements_output = self.requirements_agent.run(req_input)
        results["stages"]["requirements"] = requirements_output

        # Agent 2: Compliance Specialist (uses RAG)
        if on_stage_update:
            on_stage_update(2, "Compliance Specialist", "Checking statutory rules via RAG (PCI-DSS, SOX, GDPR, Basel)...")
        comp_input = f"{project_description}\n\n{requirements_output}\n\n{evidence_text}"
        compliance_output = self.compliance_agent.run(comp_input)
        results["stages"]["compliance_risk"] = compliance_output

        # Agent 3: System Architect (UML Diagrams)
        if on_stage_update:
            on_stage_update(3, "System Architect", "Modeling Use Case, Class, Sequence, Activity, and State diagrams...")
        uml_input = f"System: {project_title}\n\n{requirements_output}"
        uml_output = self.uml_agent.run(uml_input)
        results["stages"]["uml_diagrams"] = uml_output

        # Agent 4: SDLC Strategist (Best among Waterfall, V, Agile/Scrum, Prototyping, RAD, Spiral, Incremental)
        if on_stage_update:
            on_stage_update(4, "SDLC Strategist", "Evaluating best methodology among standard SDLC models...")
        sdlc_input = (
            f"Project: {project_title}\nScope: {project_description}\n\n"
            f"Requirements:\n{requirements_output}\n\n"
            f"Regulatory & Risk Profile:\n{compliance_output}"
        )
        sdlc_output = self.sdlc_agent.run(sdlc_input)
        results["stages"]["sdlc"] = sdlc_output

        # Agent 5: Documentation Lead
        results["consolidated_markdown"] = self.generate_consolidated_markdown(results, evidence_text)
        return results

    def generate_consolidated_markdown(self, data: Dict[str, Any], evidence_text: str = "") -> str:
        """Assembles the final Software Requirements Specification & SDLC Document."""
        title = data["title"]
        desc = data["description"]
        ts = data["timestamp"]
        stages = data["stages"]

        return f"""# Software Requirements Specification (SRS) & SDLC Recommendation
## Adheres to IEEE Std 830-1998 Guidelines

- **Project Title:** {title}
- **Document Date:** {ts}
- **Classification:** Enterprise Technical Specification
- **Authored By:** 5-Agent Collaborative LLM Architecture with RAG

---

## 1. Project Overview & Scope
{desc}

---

## 2. Software Requirements Specification
{stages.get('requirements', '')}

---

## 3. Recommended SDLC Methodology
{stages.get('sdlc', '')}

---

## 4. Unified Modeling Language (UML) Diagrams
{stages.get('uml_diagrams', '')}

---

## 5. Regulatory Compliance & Risk Controls (RAG Grounded)
{stages.get('compliance_risk', '')}

### Statutory References Retrieved via RAG:
{evidence_text}
"""
