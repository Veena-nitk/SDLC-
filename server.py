"""
Financial Agentic-AI Web Application Server with RAG & Training
───────────────────────────────────────────────────────────────
FastAPI backend providing REST endpoints for multi-agent pipeline execution,
RAG knowledge retrieval, agent training & fine-tuning dataset management,
and publication-grade IEEE 830 PDF report downloads.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from config import GEMINI_API_KEY, MODEL_NAME, OUTPUT_DIR
from knowledge_base.financial_regulations import SAMPLE_FINANCIAL_SCENARIOS
from pipeline.orchestrator import FinancialAgentOrchestrator
from reports.pdf_generator import FinancialSRSPDFGenerator
from training.trainer import AgentTrainingStudio
from rag.retriever import FinancialRAGRetriever

app = FastAPI(
    title="Financial Agentic-AI System",
    description="Autonomous Requirements Engineering, RAG Knowledge Grounding & SDLC Platform",
    version="2.1.0",
)

# Initialize singletons
orchestrator = FinancialAgentOrchestrator()
training_studio = AgentTrainingStudio()
pdf_generator = FinancialSRSPDFGenerator()
rag_retriever = orchestrator.rag_retriever

# Mount static files
STATIC_DIR = PROJECT_ROOT / "static"
STATIC_DIR.mkdir(exist_ok=True, parents=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ── Request / Response Models ──

class RunPipelineRequest(BaseModel):
    title: str
    description: str
    scenario_key: Optional[str] = None


class AddRuleRequest(BaseModel):
    title: str
    constraint: str
    mandatory: bool = True


class AddGoldenExampleRequest(BaseModel):
    domain: str
    input_scenario: str
    expected_requirements: List[str]
    expected_sdlc: str
    justification: str


class RAGQueryRequest(BaseModel):
    query: str
    top_k: int = 3


class AddDocumentRequest(BaseModel):
    filename: str
    title: str
    jurisdiction: str
    content: str


# ── Routes ──

@app.get("/")
def get_index():
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        return JSONResponse({"status": "healthy", "message": "Static index.html not found yet"})
    return FileResponse(str(index_file))


@app.get("/api/status")
def get_system_status():
    rules = training_studio.get_custom_rules()
    examples = training_studio.get_golden_examples()
    return {
        "status": "online",
        "has_gemini_key": bool(GEMINI_API_KEY),
        "model_name": MODEL_NAME if GEMINI_API_KEY else "Deterministic Financial Expert Simulation",
        "active_rules_count": len(rules),
        "golden_examples_count": len(examples),
        "indexed_rag_chunks_count": len(rag_retriever.chunks),
        "standards": [
            "IEEE Std 830-1998",
            "ISO/IEC/IEEE 29148:2018",
            "PCI-DSS v4.0",
            "GDPR (Articles 17, 25, 32)",
            "SOX Section 404",
            "Basel III / IV (BCBS 239)",
            "FATF AML / KYC",
        ],
    }


@app.get("/api/scenarios")
def get_sample_scenarios():
    return SAMPLE_FINANCIAL_SCENARIOS


@app.post("/api/pipeline/run")
def run_pipeline_api(req: RunPipelineRequest):
    try:
        title = req.title.strip() or "Financial Enterprise Application"
        desc = req.description.strip()
        if not desc:
            raise HTTPException(status_code=400, detail="Project description cannot be empty.")

        # Run multi-agent orchestrator with RAG
        results = orchestrator.run_pipeline(
            project_title=title,
            project_description=desc,
        )

        # Generate and save deliverables
        safe_name = "".join(c if c.isalnum() else "_" for c in title).strip("_").lower()[:30]
        md_path = OUTPUT_DIR / f"{safe_name}_srs.md"
        pdf_path = OUTPUT_DIR / f"{safe_name}_srs.pdf"

        with open(md_path, "w") as f:
            f.write(results["consolidated_markdown"])

        pdf_generator.build_pdf(results, str(pdf_path))

        return {
            "success": True,
            "title": results["title"],
            "timestamp": results["timestamp"],
            "stages": results["stages"],
            "retrieved_evidence": results.get("retrieved_evidence", []),
            "markdown_url": f"/api/download/md?file={md_path.name}",
            "pdf_url": f"/api/download/pdf?file={pdf_path.name}",
            "pdf_filename": pdf_path.name,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/pdf")
def download_pdf(file: str = "loan_origination_srs.pdf"):
    pdf_path = OUTPUT_DIR / file
    if not pdf_path.exists():
        default_pdf = OUTPUT_DIR / "loan_origination_srs.pdf"
        if default_pdf.exists():
            return FileResponse(str(default_pdf), media_type="application/pdf", filename=default_pdf.name)
        raise HTTPException(status_code=404, detail="PDF report not found. Run pipeline first.")
    return FileResponse(str(pdf_path), media_type="application/pdf", filename=pdf_path.name)


@app.get("/api/download/md")
def download_markdown(file: str = "loan_origination_srs.md"):
    md_path = OUTPUT_DIR / file
    if not md_path.exists():
        raise HTTPException(status_code=404, detail="Markdown report not found.")
    return FileResponse(str(md_path), media_type="text/markdown", filename=md_path.name)


# ── RAG Knowledge Base Routes ──

@app.get("/api/rag/documents")
def get_rag_documents():
    return {
        "total_chunks": len(rag_retriever.chunks),
        "chunks": [
            {
                "chunk_id": c.chunk_id,
                "title": c.title,
                "jurisdiction": c.jurisdiction,
                "standard_id": c.standard_id,
                "excerpt": c.text[:160] + "...",
                "source_file": c.doc_id,
            }
            for c in rag_retriever.chunks
        ],
    }


@app.post("/api/rag/query")
def query_rag_knowledge(req: RAGQueryRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    results = rag_retriever.retrieve(req.query.strip(), top_k=req.top_k)
    return {"query": req.query, "results": results}


@app.post("/api/rag/add-document")
def add_rag_document(req: AddDocumentRequest):
    if not req.filename.strip() or not req.content.strip():
        raise HTTPException(status_code=400, detail="Filename and content required.")
    
    docs_dir = PROJECT_ROOT / "knowledge_base" / "documents"
    docs_dir.mkdir(exist_ok=True, parents=True)
    clean_name = req.filename.strip()
    if not clean_name.endswith(".txt"):
        clean_name += ".txt"
    file_path = docs_dir / clean_name

    full_content = (
        f"Title: {req.title.strip()}\n"
        f"Jurisdiction: {req.jurisdiction.strip()}\n"
        f"Standard Identifier: {clean_name.split('.')[0].upper()}\n\n"
        f"{req.content.strip()}\n"
    )
    file_path.write_text(full_content, encoding="utf-8")

    # Re-index RAG chunks
    rag_retriever._index_documents()
    return {"success": True, "filename": clean_name, "total_chunks": len(rag_retriever.chunks)}


# ── Training & Fine-Tuning Studio Routes ──

@app.get("/api/training/data")
def get_training_data():
    return {
        "rules": training_studio.get_custom_rules(),
        "golden_examples": training_studio.get_golden_examples(),
    }


@app.post("/api/training/add-rule")
def add_custom_rule(req: AddRuleRequest):
    if not req.title.strip() or not req.constraint.strip():
        raise HTTPException(status_code=400, detail="Title and constraint are required.")
    rule = training_studio.add_custom_rule(
        title=req.title.strip(),
        constraint=req.constraint.strip(),
        mandatory=req.mandatory,
    )
    return {"success": True, "rule": rule}


@app.post("/api/training/add-example")
def add_golden_example(req: AddGoldenExampleRequest):
    if not req.domain.strip() or not req.input_scenario.strip() or not req.expected_requirements:
        raise HTTPException(status_code=400, detail="Domain, scenario, and requirements are required.")
    example = training_studio.add_golden_example(
        domain=req.domain.strip(),
        input_scenario=req.input_scenario.strip(),
        expected_requirements=req.expected_requirements,
        expected_sdlc=req.expected_sdlc.strip(),
        justification=req.justification.strip(),
    )
    return {"success": True, "example": example}


@app.get("/api/training/export-tuning-dataset")
def export_tuning_dataset():
    export_path = OUTPUT_DIR / "financial_fine_tuning_dataset.jsonl"
    count = training_studio.export_fine_tuning_jsonl(export_path)
    return FileResponse(
        str(export_path),
        media_type="application/x-jsonlines",
        filename="financial_fine_tuning_dataset.jsonl",
        headers={"X-Dataset-Count": str(count)},
    )


if __name__ == "__main__":
    import uvicorn
    print("\nStarting Financial Agentic-AI Web Dashboard with RAG...")
    print("Open your browser at: http://127.0.0.1:8000\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
