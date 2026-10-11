import os
import joblib

BASE_DIR = os.path.dirname(
  os.path.dirname(os.path.abspath(__file__))
)
MODEL_FILE = os.path.join(
  BASE_DIR,
  "ai",
  "model.pkl"
)

model = joblib.load(
  MODEL_FILE
)

def predict_condition(
  temperature,
  vibration,
  current,
  rpm
):

  prediction = model.predict(
    [[
      temperature,
      vibration,
      current,
      rpm
    ]]
  )[0]
  return prediction

def estimate_rul(
  health
):
  rul_days = int(
    max(
       1,
       health
    )
  )
  return rul_days

def maintenance_advice(
  health
):
  if health >= 80:
    return "NO ACTION REQUIRED"

  elif health >= 50:
    return "SCHEDULE MAINTENANCE"

  elif health >= 20:
    return "MAINTENANCE REQUIRED SOON"

  else:
    return "IMMEDIATE MAINTENANCE REQUIRED"
