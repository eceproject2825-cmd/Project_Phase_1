import csv
import json
import os

import paho.mqtt.client as mqtt
BASE_DIR = os.path.dirname(
  os.path.dirname(
    os.path.abspath(__file__)
  )
)
DATA_DIR = os.path.join(
  BASE_DIR,
  "data"
)

CSV_FILE = os.path.join(
  DATA_DIR,
  "sensor_data.csv"
)

BROKER = "localhost"
PORT = 1883
TOPIC = "industrial/motor/sensor"

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(CSV_FILE):
  with open(
    CSV_FILE,
    "w",
    newline="",
    encoding="utf-8"
  ) as file:
    writer = csv.writer(file)
    writer.writerow([
      "timestamp",
      "temperature",
      "vibration",
      "current".
      "rpm",
    ])

def on_connect(client, userdata, flags, reason_code, properties=None):
  if reason_code == 0:
    print("Digital Twin connected to MQTT broker")
    client.subscribe(
      TOPIC,
      qos=1
    )
    print("Subscribed to:", TOPIC)
    print("Waiting for sensor data...")
    print()

  else:
    print(
      "Digital Twin MQTT connection failed:",
      reason_code
    )

def on_message(client, userdata, message):
  try:
    data = json.loads(
      message.payload.decode("utf-8")
    )
    timestamp = data.get(
      "timestamp"
    )
    temperature = float(
      data.get("temperature")
    )
    vibration = float(
      data.get("vibration")
    )
    current = float(
      data.get("current")
    )
    rpm = int(
      data.get("rpm")
    )

    with open(
      CSV_FILE,
      "a",
      newline="",
      encoding="utf-8"
    ) as file:
      writer = csv.writer(file)
      writer.writerow([
        timestamp,
        temperature,
        vibration,
        current,
        rpm
      ])

    print(
      f"Received -> "
      f"T={temperature:.2f}°C | "
      f"V={vibration:.2f} mm/s | "
      f"I={current:.2f} A | "
      f"RPM={rpm}"
    )
except Exception as e:
   print(
     "Error processing MQTT message:",
     e
   )

print("=" * 60)
print(" INDUSTRIAL DIGITAL TWIN - MQTT RECEIVER")
print("=" * 60)

print()
print("Connecting Digital Twin to MQTT broker...")
print("Broker  :", BROKER)
print("Port    :", PORT)
print("Topic   :", TOPIC)
print("CSV     :", CSV_FILE)
print()

client = mqtt.Client(
  mqtt.CallbackAPIVersion.VERSION2,
  client_id = "industrial_digital_twin_receiver"
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
  print("Stopping Digital Twin receiver...")

except Exception as e:
  print(
    "MQTT receiver error:",
    e
  )

finally:
  client.disconnect()
  print("Digital Twin receiver stopped.")
