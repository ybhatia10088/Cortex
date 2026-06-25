from cortex.ollama_client import OllamaClient
from cortex.controller import CognitiveController
from cortex.reasoning_engine import AdaptiveReasoningEngine


llm = OllamaClient()

controller = CognitiveController(llm)

cortex = AdaptiveReasoningEngine(
    llm,
    controller
)

questions = [
    "What is the capital of Japan?",
    "Debug why a distributed database might lose consistency during network failures.",
    "Design an AI system that improves reasoning without changing model weights."
]

for question in questions:
    print("\n===================")
    print("QUESTION:")
    print(question)

    answer = cortex.answer(question)

    print("\nANSWER:")
    print(answer)