# INDUSTRIAL DIGITAL TWIN
# AI ANOMALY DETECTION

def detect_anomaly(temperature, vibration, current, rpm):
  """
  Detect abnormal machine operating conditions.
  Returns:
      anomaly_score
      anomaly_status
  """
  score = 0

  if temperature > 80:
    score += 35
  elif temperature > 70:
    score += 15

  if vibration > 8:
    score += 40
  elif vibration > 6:
    score += 20

  if current > 10:
    score += 25
  elif current > 8:
    score += 10

  if rpm < 1000 or rpm > 1800:
    score += 30
  elif rpm < 1200 or rpm > 1700:
    score += 10

  if score >= 50:
    status = "CRITICAL"
  elif score >= 20:
    status = "WARNING"
  else:
    status = "NORMAL"
  return score, status
  
