from predictive_maintenance import (
    predict_condition,
    estimate_rul,
    maintenance_advice
)
prediction = predict_condition(
  92,
  9,
  11,
  1100
)

rul = estimate_rul(
  0
)
advice = maintenance_advice(
  0
)
print("=" * 60)
print(
  "Predicted Condition:",
  prediction
)

print(
  "Remaining Useful Life:",
  rul,
  "days"
)

print(
  "Maintenance Advice:",
  advice
)

print("=" * 60)
  
