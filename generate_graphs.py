import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/sensor_data.csv")
df["Sample"] = range(len(df))

plt.figure(figsize=(8,4))
plt.plot(df["Sample"], df["temperature"])
plt.xlabel("Sample Number")
plt.ylabel("Temperature (°C)")
plt.title("Temperature Variation")
plt.grid(True)
plt.savefig("Temperature_Graph.png", dpi=300)
plt.close()

plt.figure(figsize=(8,4))
plt.plot(df["Sample"], df["vibration"])
plt.xlabel("Sample Number")
plt.ylabel("Vibration (mm/s)")
plt.title("Vibration Variation")
plt.grid(True)
plt.savefig("Vibration_Graph.png", dpi=300)
plt.close()

plt.figure(figsize=(8,4))
plt.plot(df["Sample"], df["current"])
plt.xlabel("Sample Number")
plt.ylabel("Current (A)")
plt.title("Current Variation")
plt.grid(True)
plt.savefig("Current_Graph.png", dpi=300)
plt.close()

plt.figure(figsize=(8,4))
plt.plot(df["Sample"], df["rpm"])
plt.xlabel("Sample Number")
plt.ylabel("RPM")
plt.title("Motor Speed Variation")
plt.grid(True)
plt.savefig("RPM_Graph.png", dpi=300)
plt.close()

print("Graphs Generated Successfully")


