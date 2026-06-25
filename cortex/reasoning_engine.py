class AdaptiveReasoningEngine:
    def __init__(self, llm, controller):
        self.llm = llm
        self.controller = controller

    def answer(self, query):
        analysis = self.controller.analyze(query)
        strategy = analysis["strategy"]

        print("\nCOGNITIVE ANALYSIS:")
        print(analysis)

        if strategy == "direct":
            prompt = f"""
Answer the question in one concise sentence.

Question:
{query}
"""

        elif strategy == "deliberate":
            prompt = f"""
You are using an external inference-time reasoning layer.

Do not claim that model weights are retrained, fine-tuned, or changed.
Reason carefully, then explain:
- the core mechanism
- relevant trade-offs
- practical safeguards

Question:
{query}
"""

        else:
            prompt = f"""
You are using an external test-time cognition layer. The base model weights cannot be changed.

Use this inference-time workflow internally:
1. Decompose the problem.
2. Consider at least two approaches.
3. Compare trade-offs and likely failure modes.
4. Give a clear final architecture or recommendation.

Do not claim that the base model is retrained, fine-tuned, or modified.

Question:
{query}
"""

        return self.llm.generate(prompt)