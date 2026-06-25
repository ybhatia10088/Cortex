import requests


class OllamaClient:
    """
    Model abstraction layer.

    Cortex can work with any LLM because reasoning control
    happens outside the model weights.
    """

    def __init__(self, model="llama3.2"):
        self.model = model
        self.endpoint = "http://localhost:11434/api/generate"


    def generate(self, prompt):

        response = requests.post(
            self.endpoint,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()

        return response.json()["response"]


if __name__ == "__main__":

    llm = OllamaClient()

    print(
        llm.generate(
            "Explain adaptive cognition in one sentence."
        )
    )