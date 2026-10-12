from virtual_sensor import calculate_health
health, status = calculate_health(
  temp = 85,
  vibration = 5.8,
  current = 6.2,
  rpm = 1250
)

print("Health:", health)
print("Status:", status)
