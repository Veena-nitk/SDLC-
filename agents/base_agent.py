"""
Base agent class providing shared LLM communication, grounding, and fallback execution.
"""

from abc import ABC, abstractmethod
import os
import logging

from config import GEMINI_API_KEY, MODEL_NAME, GENERATION_CONFIG

logger = logging.getLogger("sdlc_agents")


class BaseAgent(ABC):
    """Abstract base class for all agents in the financial agentic platform."""

    def __init__(self, name: str, role: str, system_instruction: str):
        self.name = name
        self.role = role
        self.system_instruction = system_instruction
        self.has_llm = False
        self.client = None

        if GEMINI_API_KEY:
            try:
                from google import genai
                self.client = genai.Client(api_key=GEMINI_API_KEY)
                self.has_llm = True
            except Exception as e:
                logger.warning(f"Could not initialize Gemini Client for {self.name}: {e}")
                self.has_llm = False

    def _call_llm(self, prompt: str) -> str:
        """Send prompt to Gemini if available, else return fallback generation."""
        if self.has_llm and self.client:
            try:
                from google.genai import types
                response = self.client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                        temperature=GENERATION_CONFIG["temperature"],
                        top_p=GENERATION_CONFIG["top_p"],
                        max_output_tokens=GENERATION_CONFIG["max_output_tokens"],
                    ),
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                logger.warning(f"LLM call failed for {self.name} ({e}). Using expert domain engine.")

        # Fallback to local expert engine
        return self._expert_fallback(prompt)

    @abstractmethod
    def run(self, input_data: str) -> str:
        """Execute the agent's core task."""
        ...

    @abstractmethod
    def _expert_fallback(self, prompt: str) -> str:
        """Domain-grounded deterministic expert fallback when LLM is offline or keyless."""
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} role={self.role!r}>"
