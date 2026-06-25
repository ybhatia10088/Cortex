import time


class Evaluator:
    """
    Measures inference behavior.

    Tracks:
    - latency
    - reasoning strategy
    - response length
    """


    def evaluate(self, engine, question):

        start = time.time()

        answer = engine.answer(question)

        end = time.time()


        return {

            "question": question,

            "answer": answer,

            "latency": round(
                end - start,
                2
            ),

            "characters": len(answer)

        }