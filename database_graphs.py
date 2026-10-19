import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("database/industrial_digital_twin.db")

df = pd.read_sql_query("""
SELECT *
FROM sensor_readings
ORDER BY id DESC
LIMIT 300
""", conn)

df = df.iloc[::-1]

plt.figure(figsize=(8,4))
plt.plot(df["temperature"], linewidth=1)
plt.xlabel("Samples")
plt.ylabel("Temperature (°C)")
plt.title("Temperature Variation")
plt.grid(True)
plt.tight_layout()
plt.savefig("Temperature_Graph.png", dpi=300)
plt.close()

plt.figure(figsize=(8,4))
plt.plot(df["vibration"], linewidth=1)
plt.xlabel("Samples")
plt.ylabel("Vibration (mm/s)")
plt.title("Vibration Variation")
plt.grid(True)
plt.tight_layout()
plt.savefig("Vibration_Graph.png", dpi=300)
plt.close()

plt.figure(figsize=(8,4))
plt.plot(df["current"], linewidth=1)
plt.xlabel("Samples")
plt.ylabel("Current (A)")
plt.title("Current Variation")
plt.grid(True)
plt.tight_layout()
plt.savefig("Current_Graph.png", dpi=300)
plt.close()

plt.figure(figsize=(8,4))
plt.plot(df["rpm"], linewidth=1)
plt.xlabel("Samples")
plt.ylabel("RPM")
plt.title("Motor Speed Variation")
plt.grid(True)
plt.tight_layout()
plt.savefig("RPM_Graph.png", dpi=300)
plt.close()

print("All graphs generated successfully.")

