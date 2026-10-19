import os
import sqlite3
import asyncio

from pymodbus.server import ModbusTcpServer
from pymodbus.simulator import DataType, SimData, SimDevice

BASE_DIR = os.path.dirname(
  os.path.dirname(os.path.abspath(__file__))
)
DB_FILE = os.path.join(
  BASE_DIR,
  "database",
  "industrial_digital_twin.db"
)

HOST = "0.0.0.0"
PORT = 5020

DEVICE_ID = 1

def get_latest_data():
  if not os.path.exists(DB_FILE):
    print("Database not found:")
    print(DB_FILE)
    return None

  try:
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""
       SELECT *
       FROM sensor_readings
       ORDER BY id DESC
       LIMIT 1
    """)
    row = cursor.fetchone(
    connection.close()
    if row is None:
        return None
    return dict(row)

  except Exception as error:
    print("Database read error:", error)
    return None

def encode_status(status):
  status = str(status).upper()
  if status == "NORMAL":
    return 0

  if status == "WARNING":
    return 1
  if status == "CRITICAL":
    return 2

  return 3

async def main():
  print("=" * 60)
  print(" INDUSTRIAL DIGITAL TWIN - MODBUS TCP SERVER")
  print("=" * 60)
  print(
      "Database:",
      DB_FILE
  )
  print(
  "Address:",
  f"{HOST}:{PORT}"
  )
  print()
  print("REGISTER MAP")

  print("Register 0  -> Temperature x100")
  print("Register 1  -> Vibration x100")
  print("Register 2  -> Current x100")
  print("Register 3  -> RPM")
  print("Register 4  -> Health")
  print("Register 5  -> Status")
  print("Register 6  -> Anomaly Score")
  print("Register 7  -> Anomaly Status")
  print()
  print("STATUS CODES")
  print("0 -> NORMAL")
  print("1 -> WARNING")
  print("2 -> CRITICAL")
  print("3 -> UNKNOWN")
  print("=" * 60)

  data_block = SimData(
    0,
    datatype=DataType.REGISTERS,
    values=[0] * 20
  )
  device = SimDevice(
      DEVICE_ID,
      data_block
  )
  server = ModbusTcpServer(
     context = device,
     address=(
         HOST,
         PORT
     )
  )
  async def update_registers():
    data = get_latest_data()
    if data is None:
      return
    try:
      temperature = float(
        data.get(
          "temperature",
          0.0
        )
      )
      vibration = float(
          data.get(
              "vibration",
              0.0
          )
      )
      current = float(
          data.get(
              "current",
              0.0
          )
      )
      rpm = int(
          data.get(
              "rpm",
              0
          )
      )
      health = float(
          data.get(
              "health_index",
              0.0
          )
      )
      status = data.get(
              "status",
              "UNKNOWN"
          
      )
      anomaly_score = float(
          data.get(
              "anomaly_score",
              0.0
          )
      )
      anomaly_status = data.get(
              "anomaly_status",
              "UNKNOWN"
          
      )
      registers = [
        int(round(
            temperature * 100
        )),
        int(round(
            vibration * 100
        )),
        int(round(
            current * 100
        )),
        int(round(
            health
        )),
        encode_status(
            status
        ),
        int(round(
            anomay_score
        )),
        encode_status(
            anomaly_status
        )
      ]
      await server.async_setValues(
          DEVICE_ID,
          3,
          0,
          registers
      )
      print(
        f"Modbus Data -> "
        f"T={temperature:.2f} °C | "
        f"V={vibration:.2f} mm/s | "
        f"I={current:.2f} A | "
        f"RPM={rpm} | "
        f"Health={health:.0f}% | "
        f"Status={status} | "
        f"Anomaly={anomaly_score:.0f} | "
        f"Anomaly Status={anomaly_status}"
      )
    except Exception as error:
      print(
        "Register update error:",
        error
      )

    async def database_update_loop():
      while True:
        try:
          await update_registers()

        except Exception as error:
          print(
            "update loop error:",
            error
          )
          await asyncio.sleep(1)

    update_task = asyncio.create_task(
      database_update_loop()
    )
    print(
      "Starting Modbus TCP server..."
    )
    print("=" * 60)
    try:
      await server.serve_forever()
    except asyncio.CancelledError:
      pass
    finally:
      update_task.cancel()
      try:
        await update_task
      except asyncio.CancelledError:
        pass

if __name__ == "__main__":
  try:
    asyncio.run(
      main()
    )
  except KeyboardInterrupt:
    print(
      "\nModbus TCP server stopped."
    )
        
      
