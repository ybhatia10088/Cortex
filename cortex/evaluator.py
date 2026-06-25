import time


class Evaluator:
    """
    Captures output quality proxies and inference-time metadata
    from a Cortex run.
    """

    def evaluate(self, engine, question):
        start_time = time.time()

        answer = engine.answer(question)

        elapsed = round(time.time() - start_time, 2)

        metadata = engine.last_metadata.copy()

        return {
            "question": question,
            "answer": answer,
            "latency": elapsed,
            "characters": len(answer),
            "strategy": metadata.get("strategy"),
            "difficulty": metadata.get("difficulty"),
            "uncertainty": metadata.get("uncertainty"),
            "effort_score": metadata.get("effort_score"),
            "model_calls": metadata.get("model_calls"),
            "candidate_count": metadata.get("candidate_count"),
            "selected_candidate": metadata.get("selected_candidate"),
            "verifier_score": metadata.get("verifier_score"),
            "verifier_reason": metadata.get("verifier_reason")
        }