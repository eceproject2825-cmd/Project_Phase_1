import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("database/industrial_digital.twin.db")
df = pd.read_sql_query("""
SELECT rpm
FROM sensor_readings
ORDER BY id DESC
LIMIT 300
""", conn)

df = df.iloc[::-1]
plt.figure(figsize=(8,4))
plt.plot(df["rpm"], linewidth=1)
plt.xlabel("Samples")
plt.ylabel("RPM")
plt.title("Motor Speed Variation")
plt.grid(True)
plt.tight_layout()

plt.savefig("RPM_Graph.png", dpi=300)
print("RPM graph generated successfully")
