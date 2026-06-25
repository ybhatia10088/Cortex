import json
import pandas as pd

from cortex.ollama_client import OllamaClient
from cortex.controller import CognitiveController
from cortex.reasoning_engine import AdaptiveReasoningEngine
from cortex.evaluator import Evaluator


def main():
    llm = OllamaClient()

    controller = CognitiveController(llm)

    engine = AdaptiveReasoningEngine(
        llm,
        controller
    )

    evaluator = Evaluator()

    with open("benchmarks/questions.json", "r") as file:
        questions = json.load(file)

    results = []

    for item in questions:
        output = evaluator.evaluate(
            engine,
            item["question"]
        )

        output["type"] = item["type"]

        results.append(output)

    df = pd.DataFrame(results)

    # Full raw outputs, including answers.
    df.to_csv(
        "benchmarks/results.csv",
        index=False
    )

    # Compact metrics file for GitHub and charts.
    summary = df[[
        "type",
        "latency",
        "characters"
    ]].copy()

    summary.to_csv(
        "benchmarks/summary.csv",
        index=False
    )

    print("\nBenchmark summary:")
    print(summary)


if __name__ == "__main__":
    main()