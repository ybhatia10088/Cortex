import json
import re


class CognitiveController:
    """
    Estimates task complexity and routes a query
    to an inference-time reasoning strategy.
    """

    def __init__(self, llm):
        self.llm = llm

    def analyze(self, query):
        prompt = f"""
You are an uncertainty estimator for an LLM inference controller.

Evaluate this query:

{query}

Return ONLY valid JSON:
{{
  "difficulty": 0.0,
  "uncertainty": 0.0,
  "reason": "brief explanation"
}}

Difficulty guide:
- 0.0 to 0.29: factual recall or simple transformation
- 0.30 to 0.59: explanation, debugging, bounded analysis
- 0.60 to 1.0: design, architecture, research, strategy, multi-step reasoning
"""

        response = self.llm.generate(prompt).strip()

        try:
            match = re.search(r"\{.*\}", response, re.DOTALL)
            data = json.loads(match.group()) if match else json.loads(response)

            difficulty = max(
                0.0,
                min(1.0, float(data.get("difficulty", 0.5)))
            )

            uncertainty = max(
                0.0,
                min(1.0, float(data.get("uncertainty", 0.5)))
            )

            deep_terms = [
                "design",
                "architecture",
                "strategy",
                "research",
                "evaluate",
                "failure modes",
                "trade-offs",
                "multiple candidate",
                "system"
            ]

            if any(term in query.lower() for term in deep_terms):
                difficulty = max(difficulty, 0.75)

            effort_score = 0.7 * difficulty + 0.3 * uncertainty

            if effort_score < 0.30:
                strategy = "direct"
            elif effort_score < 0.50:
                strategy = "deliberate"
            else:
                strategy = "deep"

            return {
                "difficulty": difficulty,
                "uncertainty": uncertainty,
                "effort_score": round(effort_score, 2),
                "strategy": strategy,
                "reason": data.get(
                    "reason",
                    "Estimated from task structure."
                )
            }

        except (
            json.JSONDecodeError,
            TypeError,
            ValueError,
            AttributeError
        ):
            return {
                "difficulty": 0.5,
                "uncertainty": 0.5,
                "effort_score": 0.5,
                "strategy": "deep",
                "reason": (
                    "Fallback allocation because model output "
                    "was not valid JSON."
                )
            }