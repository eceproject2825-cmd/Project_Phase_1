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
    print("Register 1:", register[0], "(Temperature x100)")
    print("Register 2:", register[0], "(Temperature x100)")
    print("Register 3:", register[0], "(Temperature x100)")
    print("Register 4:", register[0], "(Temperature x100)")
    print("Register 5:", register[0], "(Temperature x100)")
    print("Register 6:", register[0], "(Temperature x100)")
    print("Register 7:", register[0], "(Temperature x100)")
