import json
import re
import time


class AdaptiveReasoningEngine:
    """
    Routes queries through different inference-time workflows.

    Direct:
        One concise model call.

    Deliberate:
        One structured reasoning call.

    Deep:
        Generates multiple candidate answers, runs a verifier,
        applies a constraint editor, and returns the best compliant answer.

    This is a prompt-level prototype of adaptive test-time search.
    """

    def __init__(self, llm, controller):
        self.llm = llm
        self.controller = controller
        self.last_metadata = {}

    def _extract_json(self, text):
        """
        Attempts to recover JSON even if the model adds extra text.
        """
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if not match:
            return None

        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None

    def _generate_direct_answer(self, query):
        prompt = f"""
Answer this question in one concise sentence.

Question:
{query}
"""
        return self.llm.generate(prompt)

    def _generate_deliberate_answer(self, query):
        prompt = f"""
Answer the user's question directly and technically.

Use careful reasoning before answering. Structure the answer around:
- root causes or core mechanism
- trade-offs
- practical safeguards or next steps

Do not talk about Cortex, external inference layers, model routing,
or LLM architecture unless the user's question explicitly asks about them.

Question:
{query}
"""
        return self.llm.generate(prompt)

    def _generate_candidates(self, query, count=3):
        """
        Produces distinct solution candidates for high-effort tasks.
        """
        candidate_prompts = [
            f"""
You are candidate reasoner A.

Solve the task using an inference-time systems-design mindset.
Focus on architecture, interfaces, workflow, and implementation details.

Constraints:
- The base model and all model weights remain fixed.
- Do not propose training, fine-tuning, online learning, or architecture changes.
- Allowed methods include decomposition, retrieval, tools, external memory,
  candidate generation, verification, and adaptive compute allocation.

Question:
{query}
""",
            f"""
You are candidate reasoner B.

Solve the task by focusing on trade-offs, failure modes,
evaluation criteria, and practical constraints.

Constraints:
- The base model and all model weights remain fixed.
- Do not propose training, fine-tuning, online learning, or architecture changes.
- Allowed methods include decomposition, retrieval, tools, external memory,
  candidate generation, verification, and adaptive compute allocation.

Question:
{query}
""",
            f"""
You are candidate reasoner C.

Solve the task by proposing a minimal but technically credible
implementation plan. Be concrete and avoid vague buzzwords.

Constraints:
- The base model and all model weights remain fixed.
- Do not propose training, fine-tuning, online learning, or architecture changes.
- Allowed methods include decomposition, retrieval, tools, external memory,
  candidate generation, verification, and adaptive compute allocation.

Question:
{query}
"""
        ]

        candidates = []

        for prompt in candidate_prompts[:count]:
            candidates.append(self.llm.generate(prompt))

        return candidates

    def _select_best_candidate(self, query, candidates):
        """
        Uses a separate verifier call to select the strongest candidate.
        """
        formatted_candidates = "\n\n".join(
            [
                f"Candidate {index + 1}:\n{candidate}"
                for index, candidate in enumerate(candidates)
            ]
        )

        prompt = f"""
You are a strict verifier for a test-time cognition system.

Original task:
{query}

Evaluate the candidate answers below.

Choose the answer that is:
- most responsive to the original task
- technically grounded
- internally consistent
- practical and specific
- compliant with the constraint that the base model weights remain fixed
- free of proposals involving retraining, fine-tuning, online learning,
  adversarial training, or new trainable neural modules

Return ONLY valid JSON in this format:

{{
  "best_candidate": 1,
  "score": 0.0,
  "reason": "one concise sentence"
}}

Candidates:
{formatted_candidates}
"""

        verifier_response = self.llm.generate(prompt)
        verdict = self._extract_json(verifier_response)

        if verdict is None:
            return {
                "best_candidate": 1,
                "score": None,
                "reason": "Verifier output could not be parsed; defaulted to candidate 1."
            }

        best_candidate = verdict.get("best_candidate", 1)

        try:
            best_candidate = int(best_candidate)
        except (TypeError, ValueError):
            best_candidate = 1

        best_candidate = max(1, min(len(candidates), best_candidate))

        score = verdict.get("score")

        try:
            score = round(float(score), 2)
        except (TypeError, ValueError):
            score = None

        return {
            "best_candidate": best_candidate,
            "score": score,
            "reason": verdict.get(
                "reason",
                "Verifier selected the strongest candidate."
            )
        }

    def _enforce_constraints(self, query, answer):
        """
        Final editor pass that removes proposals requiring training,
        fine-tuning, or model/architecture changes.
        """
        prompt = f"""
You are a technical editor for an inference-time cognition prototype.

Original task:
{query}

Draft answer:
{answer}

Rewrite the answer only if necessary so it strictly follows these constraints:

- Do not propose retraining, fine-tuning, online learning, adversarial training,
  learning a new neural module, or modifying model architecture.
- The base model and all model weights must remain fixed.
- Allowed methods are inference-time decomposition, multiple candidate generation,
  verifier-based selection, retrieval, tools, external memory, and adaptive compute budgets.
- Return a standalone technically credible answer.
- Do not mention that you are editing or correcting anything.

Return only the revised answer.
"""
        return self.llm.generate(prompt)

    def _generate_deep_answer(self, query):
        """
        Runs selective search:
        generate candidates -> verify -> enforce constraints -> return best.
        """
        candidates = self._generate_candidates(query, count=3)
        verdict = self._select_best_candidate(query, candidates)

        selected_index = verdict["best_candidate"] - 1
        selected_answer = candidates[selected_index]

        final_answer = self._enforce_constraints(query, selected_answer)

        return final_answer, {
            "candidate_count": len(candidates),
            "selected_candidate": verdict["best_candidate"],
            "verifier_score": verdict["score"],
            "verifier_reason": verdict["reason"]
        }

    def answer(self, query):
        start_time = time.time()

        analysis = self.controller.analyze(query)
        strategy = analysis["strategy"]

        print("\nCOGNITIVE ANALYSIS:")
        print(analysis)

        deep_metadata = {
            "candidate_count": 0,
            "selected_candidate": None,
            "verifier_score": None,
            "verifier_reason": None
        }

        if strategy == "direct":
            answer = self._generate_direct_answer(query)
            model_calls = 2

        elif strategy == "deliberate":
            answer = self._generate_deliberate_answer(query)
            model_calls = 2

        else:
            answer, deep_metadata = self._generate_deep_answer(query)
            model_calls = 6

        self.last_metadata = {
            "strategy": strategy,
            "difficulty": analysis.get("difficulty"),
            "uncertainty": analysis.get("uncertainty"),
            "effort_score": analysis.get("effort_score"),
            "model_calls": model_calls,
            "total_latency": round(time.time() - start_time, 2),
            **deep_metadata
        }

        print("\nINFERENCE METADATA:")
        print(self.last_metadata)

        return answer