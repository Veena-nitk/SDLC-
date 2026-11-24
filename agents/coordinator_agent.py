"""
Coordinator & Human-in-the-Loop Orchestration Agent
───────────────────────────────────────────────────
Manages multi-agent workflow execution, shared blackboard state,
audit trail generation, and human review/approval checkpoints.
"""

from typing import Dict, Any, List
from datetime import datetime
import json

from .base_agent import BaseAgent


class CoordinatorAgent(BaseAgent):
    """Central orchestrator managing multi-agent collaboration and governance."""

    def __init__(self):
        super().__init__(
            name="Coordinator & Governance Agent",
            role="Central Workflow Orchestration & Human Approval Gatekeeper",
            system_instruction="Manage agent execution order, shared state, and governance checkpoints.",
        )
        self.audit_log: List[Dict[str, Any]] = []

    def log_event(self, stage: str, agent_name: str, status: str, details: str = ""):
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "stage": stage,
            "agent": agent_name,
            "status": status,
            "details": details,
        }
        self.audit_log.append(event)

    def run(self, input_text: str) -> str:
        # Coordinator synthesizes the execution audit trail
        return self._expert_fallback(input_text)

    def _expert_fallback(self, prompt: str) -> str:
        events_md = "\n".join([
            f"- `[{e['timestamp']}]` **{e['stage']}** ({e['agent']}) -> `{e['status']}` {e['details']}"
            for e in self.audit_log
        ])

        return f"""\
### Multi-Agent Governance & Audit Trail

| Audit Timestamp (UTC) | Workflow Stage | Agent Responsible | Status | Checkpoint Summary |
| :--- | :--- | :--- | :---: | :--- |
{self._format_audit_table()}

#### Mandatory Human-in-the-Loop (HITL) Approval Checkpoints:
1. **Requirements Baseline Approval:** Sign-off by Lead Systems Analyst & Product Owner.
2. **Regulatory & Security Mapping Verification:** Sign-off by Chief Compliance Officer (CCO) and CISO.
3. **SDLC Methodology & Release Gates Approval:** Sign-off by Software Engineering Director & QA Lead.
"""

    def _format_audit_table(self) -> str:
        if not self.audit_log:
            return "| *No events logged yet* | Initialization | Coordinator | PENDING | Awaiting pipeline trigger |"
        rows = []
        for e in self.audit_log:
            rows.append(f"| {e['timestamp']} | {e['stage']} | {e['agent']} | **{e['status']}** | {e['details']} |")
        return "\n".join(rows)
