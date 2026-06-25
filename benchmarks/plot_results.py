import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("benchmarks/summary.csv")

plt.figure(figsize=(8, 5))
plt.bar(df["type"], df["latency"])
plt.title("Cortex: Observed Latency by Routing Strategy")
plt.xlabel("Task Type")
plt.ylabel("Latency (seconds)")
plt.tight_layout()
plt.savefig("assets/latency_by_task.png", dpi=200)

plt.figure(figsize=(8, 5))
plt.bar(df["type"], df["model_calls"])
plt.title("Cortex: Adaptive Test-Time Model Calls")
plt.xlabel("Task Type")
plt.ylabel("Model Calls")
plt.tight_layout()
plt.savefig("assets/model_calls_by_task.png", dpi=200)

plt.figure(figsize=(8, 5))
plt.bar(df["type"], df["candidate_count"])
plt.title("Cortex: Candidate Search Budget")
plt.xlabel("Task Type")
plt.ylabel("Candidate Answers Generated")
plt.tight_layout()
plt.savefig("assets/candidate_budget_by_task.png", dpi=200)

print("Saved charts to assets/")