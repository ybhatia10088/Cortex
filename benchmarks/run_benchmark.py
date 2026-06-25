import json
import pandas as pd

from cortex.ollama_client import OllamaClient
from cortex.controller import CognitiveController
from cortex.reasoning_engine import AdaptiveReasoningEngine
from cortex.evaluator import Evaluator


def main():
    llm = OllamaClient()
    controller = CognitiveController(llm)
    engine = AdaptiveReasoningEngine(llm, controller)
    evaluator = Evaluator()

    with open("benchmarks/questions.json", "r") as file:
        questions = json.load(file)

    results = []

    for item in questions:
        output = evaluator.evaluate(engine, item["question"])
        output["type"] = item["type"]
        results.append(output)

    df = pd.DataFrame(results)

    df.to_csv(
        "benchmarks/results.csv",
        index=False
    )

    summary_columns = [
        "type",
        "strategy",
        "difficulty",
        "uncertainty",
        "effort_score",
        "model_calls",
        "candidate_count",
        "selected_candidate",
        "verifier_score",
        "latency",
        "characters"
    ]

    summary = df[summary_columns].copy()

    summary.to_csv(
        "benchmarks/summary.csv",
        index=False
    )

    print("\nBenchmark summary:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()