import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("benchmarks/summary.csv")

plt.figure(figsize=(8, 5))
plt.bar(df["type"], df["latency"])
plt.title("Cortex: Latency by Cognitive Strategy")
plt.xlabel("Task Type")
plt.ylabel("Latency (seconds)")
plt.tight_layout()
plt.savefig("assets/latency_by_task.png", dpi=200)

plt.figure(figsize=(8, 5))
plt.bar(df["type"], df["characters"])
plt.title("Cortex: Response Length by Cognitive Strategy")
plt.xlabel("Task Type")
plt.ylabel("Response Length (characters)")
plt.tight_layout()
plt.savefig("assets/response_length_by_task.png", dpi=200)

print("Saved charts to assets/")