"""
Agent Pipeline
──────────────
Chains multiple agents so the output of one feeds into the next.
This enables the "pipeline mode" where:
  Project Description → Requirements Agent → SDLC Model Agent → Final Report
"""

from typing import List, Callable

from agents.base_agent import BaseAgent


class AgentPipeline:
    """
    A simple sequential pipeline that chains agents together.

    Each agent's output becomes the next agent's input.
    Optional callbacks are fired between stages for logging / display.
    """

    def __init__(self, agents: List[BaseAgent]):
        if len(agents) < 2:
            raise ValueError("A pipeline needs at least 2 agents.")
        self.agents = agents

    def run(
        self,
        initial_input: str,
        on_stage_complete: Callable[[int, str, str], None] | None = None,
    ) -> dict[str, str]:
        """
        Execute the pipeline sequentially.

        Args:
            initial_input: The starting input (e.g. project description).
            on_stage_complete: Optional callback(stage_index, agent_name, output)
                               called after each agent finishes.

        Returns:
            Dict mapping agent names to their outputs, plus a "final" key.
        """
        results: dict[str, str] = {}
        current_input = initial_input

        for i, agent in enumerate(self.agents):
            output = agent.run(current_input)
            results[agent.name] = output

            if on_stage_complete:
                on_stage_complete(i, agent.name, output)

            # Feed this agent's output as the next agent's input
            current_input = output

        results["final"] = current_input
        return results
