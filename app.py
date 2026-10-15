import streamlit as st
import sqlite3
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

B_FILE = os.path.join(
  BASE_DIR,
  "database",
  "industrial_digital_twin.db"
t.set_page_config(
    page_title = "Industrial Digital Twin",
    page_icon = "🏭",
    layout = "wide"

ef get_sensor_data():
     connection = sqlite3.connect(DB_FILE)
     query = """
         SELECT
             timestamp,
             temperature,
             vibration,
             current,
             rpm,
             health_index,
             status,
             anomaly_score,
             anomaly_status,
        FROM sensor_readings
        ORDER BY timestamp DESC
        LIMIT 100
    """

    data = pd.read_sql_query(query, connection)
    connection.close()
    return data

st.fragment(run_every=2)
ef live_dashboard():
   data = get_sensor_data()

   if data.empty:
       st.error("No sensor data available in database.")
       return 

   latest = data.iloc[0]

   st.title("🏭 Industrial Digital Twin")
   st.subheader(
       "Real-Time Machine Monitoring Dashboard"
       )

   st.divider()

   col1, col2, col3, col4 = st.columns(4)

   with col1:
   st.metric(
       "🌡️ Temperature",
       f"{latest['temperature']:.2f} °C"
       )

   with col2:
   st.metric(
       " Health",
       f"{latest['health_index']:.0f}%"
       )

   with col3:
       st.metric(
           " Vibration",
           f"{latest['vibration']:.2f} mm/s"
           )

    with col4:
         st.metric(
             " Anomaly Score",
             f"{latest['anomaly_score']:.0f}"
             )
  
