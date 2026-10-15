import sqlite3
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(BASE_DIR, "data", "sensor_data.csv")
DB_FILE = os.path.join(BASE_DIR, "database", "industrial_digital_twin.db")

def create_database():
  """Create the SQLite database and sensor table."""
  connection = sqlite3.connect(DB_FILE)
  cursor = connection.cursor()

  cursor.execute("""
      CREATE TABLE IF NOT EXISTS sensor_readings (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          timestamp TEXT NOT NULL UNIQUE,
          temperature REAL NOT NULL,
          vibration REAL NOT NULL,
          current REAL NOT NULL,
          rpm INTEGER NOT NULL
  )
  """)

   connection.commit()
   connection.close()

def import_csv_data():
  """Import only new CSV records into SQLite."""

  connection = sqlite3.connect(DB_FILE)
  cursor = connection.cursor()

  inserted = 0
  skipped = 0
  with open(CSV_FILE, "r", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
      if len(row) != 5:
        continue

      if row[0].strip().lower() == "timestamp":
          continue

      timestamp, temperature, vibration, current , rpm = row
      cursor.execute("""
          SELECT 1
          FROM sensor_readings
          WHERE timestamp = ?
      """, (timestamp,))
      exists = cursor.fetchone()
      if exists:
        skipped += 1
        continue

      cursor.execute("""
          INSERT INTO sensor_readings
          (timestamp, temperature, vibration, current, rpm)
          VALUES (?, ?, ?, ?, ?)
      """, (
         timestamp,
         float(temperature),
         float(vibration),
         float(current),
         int(rpm)
      ))
      inserted += 1

  connection.commit()
  connection.close()

  return inserted, skipped

def show_database_info(inserted, skipped):
  """Display database statistics."""
  connection = sqlite3.connect(DB_FILE)
  cursor = connection.cursor()

  cursor.execute("SELECT COUNT(*) FROM sensor_readings")
  total_records = cursor.fetchone()[0]

  print("\n=========================================")
  print("DIGITAL TWIN DATABASE")
  print("==========================================")
  print(f"Database               : {DB_FILE}")
  print(f"CSV                    : {CSV_FILE}")
  print(f"New Records            : {inserted}")
  print(f"Skipped duplicates     : {skipped}")
  print(f"Total records          : {total_records}")
  print("==========================================")

  cursor.execute("""
      SELECT timestamp, temperature, vibration, current, rpm
      FROM sensor_readings
      ORDER BY id DESC
      LIMIT 5
  """)

  print("\nLatest 5 records:")
  print("------------------------------------------")
  for row in cursor.fetchall():
    print(row)

  connection.close()

if __name__ == "__main__":
  create_database()
  inserted, skipped = import_csv_data()
  show_database_info(inserted, skipped)
