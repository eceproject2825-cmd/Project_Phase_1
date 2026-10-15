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
       "🏥 Health",
       f"{latest['health_index']:.0f}%"
       )

   with col3:
       st.metric(
           "📳 Vibration",
           f"{latest['vibration']:.2f} mm/s"
           )

    with col4:
         st.metric(
             "🚨 Anomaly Score",
             f"{latest['anomaly_score']:.0f}"
             )
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric(
            "⚡ Current",
            f"{latest['current']:.2f} A"
            )

    with col6:
         st.metric(
             "🔄 RPM",
             f"{int(latest['rpm'])}"
             )

    with col7:
        st.metric(
            "📊 Status",
            latest["status"]
            )

    with col8:
         st.metric(
             "🤖 AI Status",
             latest['anomaly_status']
             )

    st.divider()

    st.subheader("Machine Status")
    status = str(latest["status"]).upper()
    if status == "NORMAL":
        st.success("🟢 NORMAL")
    elif status = "WARNING":
       st.warning("🟡 WARNING")
    else:
      st.error("🔴 CRITICAL")

    st.write(
        f"Last updated: **{latest['timestamp']}**"
        )
    st.divider()

    st.subheader("AI Anomaly Detection")
    ai_status = str(latest["anomaly_status"]).upper()
    if ai_status == "NORMAL":
       st.success("🟢 NORMAL")
    elif ai_status == "WARNING":
      st.warning("🟡 WARNING")
    else:
      st.error("🔴 CRITICAL")

    st.write(
      f"Anomaly Score: **{latest['anomaly_score']:.0f}**"
      )

    st.divider()

    st.subheader("Sensor Trends")

    chart_data = data.copy()
    chart_data["timestamp"] = pd.to_datetime(
        chart_data["timestamp"]
        )

    chart_data = chart_data.sort_values(
        "timestamp"
        )
    chart_data = chart_data.set_index(
        "timestamp"
        )

    st.write("🌡️ Temperature")
    st.line_chart(
       chart_data["temperature"]
       )

    st.write("📳 Vibration")
    st.line_chart(
       chart_data["vibration"]
       )

    st.write("⚡Current")
    st.line_chart(
       chart_data["current"]
       )

       
    st.write("🔄 RPM")
    st.line_chart(
      chart_data["rpm"]
      )

    st.write("🏥 Machine Health")
    st.line_chart(
       chart_data["health_index"]
       )

    st.write("🚨 AI Anomaly Score")
    st.line_chart(
       chart_data["anomaly_score"]
       )

    st.divider()
    st.subheader("🗄️ Database Information")
    st.write(
        f"Latest database reading: "
        f"**{latest['timestamp']}**"
    )
    st.write(
        f"**{len(chart_data)} records displayed**"
        )

  live_dashboard()
      
    
