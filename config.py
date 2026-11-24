"""
Configuration for the Financial SDLC Multi-Agent System.
"""

import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).parent.resolve()
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# ──────────────────────────────────────────────
# Gemini API Configuration
# ──────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Default model name
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

# LLM Generation Parameters
GENERATION_CONFIG = {
    "temperature": 0.4,  # Lower temperature for rigorous engineering & compliance precision
    "top_p": 0.95,
    "max_output_tokens": 8192,
}

# ──────────────────────────────────────────────
# Financial Sector Compliance & Standards Flags
# ──────────────────────────────────────────────
DEFAULT_STANDARDS = [
    "IEEE Std 830-1998 (Recommended Practice for Software Requirements Specifications)",
    "ISO/IEC/IEEE 29148:2018 (Systems and software engineering — Life cycle processes)",
    "PCI-DSS v4.0 (Payment Card Industry Data Security Standard)",
    "GDPR (Regulation (EU) 2016/679 - Privacy by Design & Erasure)",
    "SOX Section 404 (Internal Financial Controls & Audit Trails)",
    "Basel III / IV (Operational Risk & Liquidity Reporting)",
    "FATF / FinCEN Anti-Money Laundering (AML) & Know Your Customer (KYC)",
]
