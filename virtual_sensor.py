def calculate_health(temperature,vibration,current,rpm):
  """
  Calculate machine health index from sensor parameters.
  Returns:
      health: 0-100
      status: NORMAL / WARNING / CRITICAL
  """
  health = 100.0
  if temperature <= 70:
    temperature_penalty = 0
  elif temperature <= 80:
    temperature_penalty = 10
  elif temperature <= 90:
    temperature_penalty = 25
  else:
    temperature_penalty = 45

  if vibration <= 4:
    vibration_penalty = 0
  elif vibration <= 6:
    vibration_penalty = 10
  elif vibration <= 8:
    vibration_penalty = 25
  else:
    vibration_penalty = 40

  if current <= 6:
    current_penalty = 0
  elif current <= 8:
    current_penalty = 10
  elif current <= 10:
    current_penalty = 20
  else:
    current_penalty = 35

  if 1300 <= rpm <= 1600:
    rpm_penalty = 0
  elif 1200 <= rpm < 1300 or 1600 < rpm <= 1700:
    rpm_penalty = 10
  elif 1000 <= rpm < 1200 or 1700 < rpm <= 1800:
    rpm_penalty = 25
  else:
    rpm_penalty = 40

  total_penalty = (
      temperature_penalty
      + vibration_penalty
      + current_penalty
      + rpm_penalty
  )
  health -= total_penalty

health = max(0, min(100, health))
if health >= 70:
  status = "NORMAL"
elif health >= 40:
  status - "WARNING"
else:
  status = "CRITICAL"
return round(health, 2), status
