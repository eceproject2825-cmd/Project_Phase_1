from anomaly_detection import detect_anomaly
score, status = detect_anomaly(
  temperature = 88.17,
  vibration = 7.79,
  current = 8.79,
  rpm = 1006
)
print("Anomaly Score:", score)
print("Status:", status)
