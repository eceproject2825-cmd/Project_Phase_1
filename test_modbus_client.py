from pymodbus.client import ModbusTcpClient
HOST = "localhost"
PORT = 5020

client = ModbusTcpClient(HOST, port = PORT)
print("=" * 50)
print("MODBUS TCP CLIENT TEST")
print("=" * 50)

if client.connect():
  print("Connected to Modbus Server\n")
  result = client.read_holding_registers(
    address=0,
    count=8,
    device_id=1
  )
  if result.isError():
    print("Read failed")
  else:
    registers = result.registers
    print("Register 0:", register[0], "(Temperature x100)")
    print("Register 1:", register[1], "(Vibration x100)")
    print("Register 2:", register[2], "(Current x100)")
    print("Register 3:", register[3], "(RPM)")
    print("Register 4:", register[4], "(Health)")
    print("Register 5:", register[5], "(Status)")
    print("Register 6:", register[6], "(Anomaly Score)")
    print("Register 7:", register[7], "(Anomaly Status)")
    print("\nDecoded Values")

    print("Temperature:", registers[0]/100)
    print("Vibration:", registers[1]/100)
    print("Current:", registers[2]/100)
    print("RPM:", registers[3])

  client.close()

else:
  print("Unable to connect")
