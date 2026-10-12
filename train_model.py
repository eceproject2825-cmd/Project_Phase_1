import sqlite3
import pandas as pd
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.model selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

BASE_DIR = os.path.dirname(
  os.path.dirname(os.path.abspath(__file__))
)

DB_FILE = os.path.join(
  BASE_DIR,
  "database",
  "industrial_digital_twin.db"
)

MODEL_FILE = os.path.join(
  BASE_DIR,
  "ai",
  "model.pkl"
)

print("=" * 60)
print("TRAINING PREDICTIVE MAINTENANCE MODEL")
print("=" * 60)

conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query(
  "SELECT * FROM sensor_readings",
  conn
)

conn.close()
print("Records:", len(df))
if len(df) < 100:
  print("Not enough data for training.")
  exit()

df = df.dropna(
  subset=[
    "temperature",
    "vibration",
    "current",
    "rpm",
    "status"
  ]
)

print(
  "Valid Records:",
  len(df)
)
df["target"] = df["status"]
x = df[
    [
      "temperature",
      "vibration",
      "current",
      "rpm"
    ]
]

y = df["target"]
x_train, x_test, y_train, y_test = train_test_split(
  x,
  y,
  test_size = 0.2,
  random_state = 42
)

model.fit(
  x_train,
  y_train
)
predictions = model.predict(
  x_test
)
accuracy = accuracy_score(
  y_test,
  predictions
)
joblib.dump(
  model,
  MODEL_FILE

)
print(
  f"Model Accuracy: {accuracy*100:.2f}%"
)
print(
  f"Model Saved: {MODEL_FILE}"
)
print("=" * 60)
  
