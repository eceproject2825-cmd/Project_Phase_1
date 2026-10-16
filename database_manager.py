import json
import os
import sqlite3
import sys

BASE_DIR = os.path.dirname(
   os.path.dirname(
       os.path.abspath(__file__)
   )
)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import paho.mqtt.client as mqtt
from ai.virtual_sensor import calculate_health
from ai.anomaly_detection import detect_anomaly

from ai.predictive_maintenance import(
    predict_condition,
    estimate_rul,
    maintenance_advice
)

DB_DIR = os.path.join(
  BASE_DIR,
  "database"
)

DB_FILE = os.path.join(
  DB_DIR,
  "industrial_digital_twin.db"
)
BROKER = "localhost"
PORT = 1883
TOPIC = "industrial/motor/sensor"
os.makedirs(
  DB_DIR,
  exist_ok=True
)

def initialize_database():
  connection = sqlite3.connect(DB_FILE)
  cursor = connection.cursor()
  cursor.execute(
     """
     CREATE TABLE IF NOT EXISTS sensor_readings (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         timestamp TEXT UNIQUE,
         temperature REAL,
         vibration REAL,
         cuurent REAL,
         rpm INTEGER,

         health_index REAL,
         status TEXT,
         anomaly_score REAL,
         anomaly_status TEXT,
         prediction INTEGER,
         maintenance_status TEXT,
         remaining_life_days INTEGER
     )
     """
  )

  connection.commit()
  connection.close()
  print("Database initialized successfully.")
  print("Database:", DB_FILE)

def save_sensor_data(data):
  try:
    timestamp = data["timestamp"]
    temperature = float(data["temperature"])
    vibration = float(data["vibration"])
    current = float(data["current"])
    rpm = int(data["rpm"])

    health, status = calculate_health(
        temperature,
        vibration,
        cuurent,
        rpm,
    )

    anomaly_score, anomaly_status = detect_anomaly(
        temperature,
        vibration,
        current,
        rpm
    )
    prediction = predict_condition(
        temperature,
        vibration,
        current,
        rpm
    )
    remaining_life_days = estimate_rul(
        health
    )
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT OR IGNORE INTO sensor_readings
        (
            timestamp,
            temperature,
            vibration,
            current,
            rpm,
            health_index,
            status,
            anomaly_score,
            anomaly_status,
            prediction,
            maintenance_status,
            remaining_life_days
       )
       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
       """,
       (
           timestamp,
           temperature,
           vibration,
           current,
           rpm,
           health,
           status,
           anomaly_score,
           anomaly_status,
           str(prediction),
           maintenance_status,
           remaining_life_days
       )
    )
    inserted = cursor.rowcount > 0
    connection.commit()
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sensor_readings
        """
    )
    total_records = cursor.fetchone()[0]
    connection.close()
    if inserted:
      print(
        f"Saved -> "
        f"{timestamp} | "
        f"T={temperature:.2f}°C | "
        f"V={vibration:.2f} mm/s | "
        f"I={current:.2f} A | "
        f"RPM={rpm} | "
        f"Health={health:.0f}% | "
        f"Status={status} | "
        f"Anomaly={anomaly_score} | "
        f"Anomaly Status={anomaly_status} | "
        f"Prediction={prediction} | "
        f"Maintenance={maintenance_status} | "
        f"RUL={remaining_life_days} Days"
      )

    else:
      print(
        f"Skipped duplicate -> {timestamp}"
      )
      return inserted, total_records
  except Exception as error:
    print(
      "Database save error:",
      error
    )
    return False, 0

def on_connect(
  client,
  userdata,
  flags,
  reason_code,
  properties=None
):
  if reason_code == 0:
    print()
    print("Connected to MQTT broker.")
    client.subscribe(
       TOPIC,
       qos=1
    )
    print("Subscribed to:", TOPIC)
    print("Waiting for sensor data...")
    print()

  else:
    print(
      "MQTT connection failed:",
      reason_code
    )

def on_message(
  client,
  userdata,
  message
):
  try:
    payload = message.payload.decode(
      "utf-8"
    )
    data = json.loads(payload)
    save_sensor_data(data)

  except json.JSONDecoderError:
    print(
      "Invalid JSON received."
    )
  except Exception as error:
    print(
      "MQTT message error:",
      error
    )

if __name__ == "__main__":
  print("-" * 60)
  print(
     "INDUSTRIAL DIGITAL TWIN - DATABASE MANAGER"
  )
   print("=" * 60)
   print()
   initialize_database()
   print()
   print("Connecting to MQTT broker...")
   print("Broker  :", BROKER)
   print("Port    :", PORT)
   print("Topic   :", TOPIC)
   print()

   client = mqtt.Client(
      mqtt.CallbackAPIVersion.VERSION2,
      client_id = "industrial_database_manager"
   )
   client.on_connect = on_connect
   client.on_message = on_message
   try:
      client.connect(
         BROKER,
         PORT,
         60
      )
      client.loop_forever()

except KeyboardInterrupt:
    print()
    print(
       "Stopping database manager..."
    )
except Exception as error:
    print(
       "Database manager error:",
       error
    )
finally:
    client.disconnect()
    print(
       "Database manager stopped."
    )
      
