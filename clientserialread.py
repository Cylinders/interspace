import serial
import serial.tools.list_ports



def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Port: {port.device} - {port.description}")

list_serial_ports()

x = input("What serial port are you going to be using: ")

ser = serial.Serial(x, 115200)  # Replace COMx with the correct port (Linux/Mac: /dev/ttyACM0)
while True:
    # print(ser.readline().decode().strip())
    serIn = ser.readline().decode().strip()
    match (serIn[0]): 
        case "f": 
            print("Units: Feet")
        case "m": 
            print("Units: Metres")
        case "M": 
            print("Units: Miles")
        case "y": 
            print("Units: Yards")
        case "k": 
            print("Units: Kilometres")
    print("Location: (" + serIn[1:4] + ", " + serIn[4:7] + ")")
    if not serIn[7] == "$":
        print("Message: " + serIn[7:])
    else: 
        print("$GPS request.")