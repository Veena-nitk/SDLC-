#!/usr/bin/env python3
"""
Financial Agentic-AI System
───────────────────────────
Automated Requirements Engineering, Regulatory Compliance Mapping,
UML Modeling, and SDLC Methodology Selection for Financial Systems.

Compliant with:
  • IEEE Std 830-1998 & ISO/IEC/IEEE 29148:2018
  • PCI-DSS v4.0, GDPR, SOX Section 404, Basel III/IV, FinCEN AML/KYC
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.resolve()))

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from rich.table import Table as RichTable

from config import GEMINI_API_KEY, MODEL_NAME, OUTPUT_DIR
from knowledge_base.financial_regulations import SAMPLE_FINANCIAL_SCENARIOS
from agents import (
    StakeholderInteractionAgent,
    RequirementsAgent,
    ComplianceRiskAgent,
    SDLCModelAgent,
    UMLDiagramAgent,
)
from pipeline.orchestrator import FinancialAgentOrchestrator
from reports.pdf_generator import FinancialSRSPDFGenerator

console = Console()


def print_banner():
    mode_text = "[bold green]Online (Gemini 2.0 Flash)[/bold green]" if GEMINI_API_KEY else "[bold yellow]Offline Expert Simulation (Local Financial Engine)[/bold yellow]"
    console.print(
        Panel.fit(
            "[bold cyan]🏦  Financial Agentic-AI System[/bold cyan]\n"
            "[bold white]Autonomous Requirements Engineering, UML Modeling & SDLC Selection[/bold white]\n"
            f"[dim]Standards: IEEE Std 830 / ISO/IEC/IEEE 29148 | PCI-DSS v4.0 | SOX 404 | Basel III[/dim]\n"
            f"[dim]Engine Mode: {mode_text}[/dim]",
            border_style="cyan",
        )
    )


def select_financial_scenario() -> tuple[str, str]:
    """Allows user to select a realistic financial case study or input their own."""
    console.print("\n[bold]Select a Financial Domain Scenario or enter custom:[/bold]")
    console.print("  [cyan]1[/cyan] — Automated Loan Origination & Credit Assessment (Tier-1 Bank)")
    console.print("  [cyan]2[/cyan] — Real-Time Payment Gateway & Fraud Detection Engine (25k TPS)")
    console.print("  [cyan]3[/cyan] — Omnichannel Digital Banking & KYC Onboarding (Biometric)")
    console.print("  [cyan]4[/cyan] — Custom Financial Software Scenario (Enter your own description)")

    choice = Prompt.ask("\n[bold]Your choice[/bold]", choices=["1", "2", "3", "4"], default="1")

    if choice == "1":
        sc = SAMPLE_FINANCIAL_SCENARIOS["loan_origination"]
        return sc["title"], sc["description"]
    elif choice == "2":
        sc = SAMPLE_FINANCIAL_SCENARIOS["payment_gateway"]
        return sc["title"], sc["description"]
    elif choice == "3":
        sc = SAMPLE_FINANCIAL_SCENARIOS["digital_banking"]
        return sc["title"], sc["description"]
    else:
        title = Prompt.ask("[bold yellow]Enter Project Title[/bold yellow]", default="Financial Core Service")
        console.print("[dim](Enter detailed project description. Press Enter on an empty line to finish.)[/dim]\n")
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        desc = "\n".join(lines).strip()
        if not desc:
            desc = "Automated digital financial transaction and compliance monitoring system."
        return title, desc


def display_stage_panel(title: str, content: str, border_color: str = "cyan"):
    console.print()
    console.print(Panel(Markdown(content), title=f"[bold {border_color}]{title}[/bold {border_color}]", border_style=border_color))


def run_full_pipeline():
    """Runs the 5-agent end-to-end autonomous financial engineering pipeline."""
    title, description = select_financial_scenario()

    console.print(f"\n[bold green]🚀 Initiating Autonomous Multi-Agent Pipeline for:[/bold green] [bold cyan]{title}[/bold cyan]\n")

    orchestrator = FinancialAgentOrchestrator()

    def stage_callback(stage_num: int, agent_name: str, status_msg: str):
        console.print(f"[bold cyan]▶ Stage {stage_num}/5 — {agent_name}:[/bold cyan] [dim]{status_msg}[/dim]")

    with console.status("[bold green]Agents collaborating across elicitation, IEEE 830, compliance & SDLC...[/bold green]"):
        results = orchestrator.run_pipeline(
            project_title=title,
            project_description=description,
            on_stage_update=stage_callback,
        )

    stages = results["stages"]

    # Display outputs
    display_stage_panel("📋 Stage 1: Stakeholder Perspectives & Clarification", stages["stakeholders"], "blue")
    display_stage_panel("📑 Stage 2: IEEE 830 / 29148 Requirements Specification", stages["requirements"], "green")
    display_stage_panel("🛡️ Stage 3: Regulatory Compliance (PCI-DSS/SOX) & Risk Register", stages["compliance_risk"], "red")
    display_stage_panel("📊 Stage 4: UML System Models (Use Case, Class, Sequence, State)", stages["uml_diagrams"], "magenta")
    display_stage_panel("🔄 Stage 5: SDLC Selection & Project-Specific Workflow", stages["sdlc"], "cyan")
    display_stage_panel("🏛️ Stage 6: Governance, Audit Trail & Human Approval Gates", stages["governance"], "yellow")

    # File Exports
    safe_name = "".join(c if c.isalnum() else "_" for c in title).strip("_").lower()[:30]
    md_path = OUTPUT_DIR / f"{safe_name}_SRS_Report.md"
    pdf_path = OUTPUT_DIR / f"{safe_name}_SRS_Report.pdf"

    # Save Markdown
    with open(md_path, "w") as f:
        f.write(results["consolidated_markdown"])
    console.print(f"\n[bold green]✓ Markdown SRS report saved to:[/bold green] [cyan]{md_path}[/cyan]")

    # Generate Professional PDF Report
    with console.status("[bold green]Compiling publication-grade IEEE 830 PDF Report (ReportLab)...[/bold green]"):
        pdf_gen = FinancialSRSPDFGenerator()
        pdf_gen.build_pdf(results, str(pdf_path))

    console.print(f"[bold green]✓ Ready-to-Mail IEEE 830 PDF Report generated at:[/bold green] [bold cyan]{pdf_path}[/bold cyan]")
    console.print("[dim]You can immediately attach this PDF to an email for your Teaching Assistant (TA) or Professor![/dim]\n")


def run_requirements_only():
    title, description = select_financial_scenario()
    console.print("\n[bold green]Extracting IEEE 830 / 29148 Requirements...[/bold green]")
    with console.status("[bold green]Analyzing...[/bold green]"):
        agent = RequirementsAgent()
        output = agent.run(f"Project: {title}\n{description}")
    display_stage_panel("📋 IEEE 830 Requirements Specification", output, "green")


def run_compliance_only():
    title, description = select_financial_scenario()
    console.print("\n[bold green]Evaluating Regulatory Compliance & Risk Register...[/bold green]")
    with console.status("[bold green]Analyzing...[/bold green]"):
        agent = ComplianceRiskAgent()
        output = agent.run(f"Project: {title}\n{description}")
    display_stage_panel("🛡️ Regulatory Compliance & Risk Register", output, "red")


def run_sdlc_only():
    title, description = select_financial_scenario()
    console.print("\n[bold green]Evaluating Multi-Criteria SDLC Recommendation...[/bold green]")
    with console.status("[bold green]Analyzing...[/bold green]"):
        agent = SDLCModelAgent()
        output = agent.run(f"Project: {title}\n{description}")
    display_stage_panel("🔄 SDLC Recommendation & Customized Roadmap", output, "cyan")


def run_uml_only():
    title, description = select_financial_scenario()
    console.print("\n[bold green]Generating UML System Diagrams (Mermaid notation)...[/bold green]")
    with console.status("[bold green]Synthesizing...[/bold green]"):
        agent = UMLDiagramAgent()
        output = agent.run(f"Project: {title}\n{description}")
    display_stage_panel("📊 UML System Diagrams", output, "magenta")


def main():
    print_banner()

    while True:
        console.print("\n[bold]Choose an Execution Mode:[/bold]")
        console.print("  [cyan]1[/cyan] — 🚀 [bold]Full Autonomous Pipeline[/bold] (Stakeholder → IEEE 830 SRS → Compliance → UML → SDLC → PDF Export)")
        console.print("  [cyan]2[/cyan] — 📋 Requirements Engineering Agent only (IEEE 830 / 29148)")
        console.print("  [cyan]3[/cyan] — 🛡️ Compliance & Risk Analysis Agent only (PCI-DSS / SOX / Basel III / AML)")
        console.print("  [cyan]4[/cyan] — 🔄 SDLC Selection Engine Agent only (Multi-Criteria Decision Analysis)")
        console.print("  [cyan]5[/cyan] — 📊 UML Diagrams & Architecture Agent only (Use Case, Class, Sequence, State)")
        console.print("  [cyan]q[/cyan] — Quit")

        choice = Prompt.ask("\n[bold]Your choice[/bold]", choices=["1", "2", "3", "4", "5", "q"], default="1")

        if choice == "1":
            run_full_pipeline()
        elif choice == "2":
            run_requirements_only()
        elif choice == "3":
            run_compliance_only()
        elif choice == "4":
            run_sdlc_only()
        elif choice == "5":
            run_uml_only()
        elif choice == "q":
            console.print("[dim]Goodbye! Exiting Financial Agentic-AI System. 👋[/dim]")
            break


if __name__ == "__main__":
    main()
