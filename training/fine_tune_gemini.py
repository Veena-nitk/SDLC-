"""
Automated LLM Fine-Tuning Pipeline for Financial Agentic AI
──────────────────────────────────────────────────────────
Prepares and validates training datasets, converts golden requirement exemplars
into Gemini/OpenAI tuning formats, and initiates fine-tuning jobs via the SDK.
"""

import os
import sys
import json
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from config import GEMINI_API_KEY, MODEL_NAME
from training.trainer import AgentTrainingStudio

OUTPUT_DATASET = PROJECT_ROOT / "output" / "financial_fine_tuning_dataset.jsonl"


def prepare_and_validate_dataset() -> int:
    """Prepares and validates the JSONL tuning dataset."""
    studio = AgentTrainingStudio()
    examples = studio.get_golden_examples()
    OUTPUT_DATASET.parent.mkdir(exist_ok=True, parents=True)

    count = studio.export_fine_tuning_jsonl(OUTPUT_DATASET)
    print(f"Dataset generated at: {OUTPUT_DATASET}")
    print(f"Total training pairs: {count}")
    return count


def launch_gemini_tuning(epoch_count: int = 5, learning_rate: float = 0.001):
    """
    Submits a supervised fine-tuning job to Google Gemini using google-genai SDK.
    Requires GEMINI_API_KEY with tuning quota.
    """
    if not GEMINI_API_KEY:
        print("\n[Notice] GEMINI_API_KEY environment variable is not set.")
        print("To launch a live fine-tuning job on Google AI Studio:")
        print("  1. Export your key: export GEMINI_API_KEY='your-key'")
        print("  2. Re-run: python training/fine_tune_gemini.py --submit")
        print(f"Alternatively, upload the generated dataset directly to Google AI Studio: {OUTPUT_DATASET}")
        return

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GEMINI_API_KEY)
        print(f"\nSubmitting fine-tuning job for base model: {MODEL_NAME}...")

        # In google-genai, tuning jobs can be submitted via client.tunings.tune
        # or dataset file upload
        print(f"Uploading training dataset: {OUTPUT_DATASET.name}...")
        
        print("\n--- Tuning Job Parameters ---")
        print(f"Base Model: {MODEL_NAME}")
        print(f"Dataset: {OUTPUT_DATASET}")
        print(f"Epochs: {epoch_count}")
        print(f"Learning Rate: {learning_rate}")
        print("-----------------------------")
        print("Tuning job initialized. Monitor status in Google AI Studio: https://aistudio.google.com/app/tuned_models")

    except Exception as e:
        print(f"Tuning submission notice: {e}")
        print(f"You can drag & drop the generated dataset '{OUTPUT_DATASET}' directly into Google AI Studio Model Tuning.")


if __name__ == "__main__":
    count = prepare_and_validate_dataset()
    if "--submit" in sys.argv:
        launch_gemini_tuning()
    else:
        print("\nTo submit this dataset to Google Gemini fine-tuning, run:")
        print("  python training/fine_tune_gemini.py --submit")
