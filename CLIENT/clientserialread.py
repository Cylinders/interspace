import serial
import serial.tools.list_ports
import win32api

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

for letter in letters: 
    print("we are checking these drives")
    try: 
        if(win32api.GetVolumeInformation(letter + ":\\")[0] == "INTERSPACE"): 
            break
    except:
        pass





potentialPorts = []
def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        potentialPorts.append(port.device)
        print(f"Port: {port.device} - {port.description}")

list_serial_ports()
finalPort = ""
print(potentialPorts)
print("entering loop iteration")
"""
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
print("I am here")
print("final port:" + finalPort)
"""

ser = serial.Serial("COM5", 115200)
finalPort = "FUCK"
serIn = "dumass"
if (finalPort != ""):
    while True:
        print("reading again")
        print(serIn)
        print("going to write")
        print("finished writing")
        print(serIn)
        
else: 
    print("The module was not detected. ")



class interspaceAPI():
    def __init__(self):
        self.
