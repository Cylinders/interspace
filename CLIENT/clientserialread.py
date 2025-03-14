import serial
import serial.tools.list_ports


potentialPorts = []
def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        potentialPorts.append(port.device)
        print(f"Port: {port.device} - {port.description}")

list_serial_ports()
finalPort = ""
print(potentialPorts)
for port in potentialPorts:
    ser = serial.Serial(port, 115200)
    check = ""
    while check == "":
        check = ser.readline().decode().strip()
    if check[0:13] == "interspace1.0": 
        finalPort = port
        print("Interspace module detected.")
        break
    else: 
        print("This was not the module.")

print(finalPort)
        
if (finalPort != ""):
    while True:
        # print(ser.readline().decode().strip())
        serIn = ser.readline().decode().strip()
        print(serIn)
else: 
    print("The module was not detected. ")