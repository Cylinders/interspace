import serial
import serial.tools.list_ports
import win32api
import time
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
driveLetter = ""
for letter in letters:
    print("we are checking these drives")
    try:
        if(win32api.GetVolumeInformation(letter + ":\\")[0] == "INTERSPACE"):
            driveLetter = letter
            break
    except:
        pass

print("finding serial port")
potentialPorts = serial.tools.list_ports.comports()
print(potentialPorts)
finalPort = potentialPorts[0].device
print("device selected")
"""
for p in potentialPorts:
    port = p.device  # Get the port name as a string like "COM5"
    ser = serial.Serial(port, 115200)u
    check = ""
    while check == "":
        check = ser.readline().decode().strip()
    if check[0:13] == "interspace1.0":
        finalPort = port
        break
print("final port: " + finalPort)
"""
print("beginning testing process")
with open(driveLetter + ":\\comms.txt", "w") as f:
    f.write("testing")

start = 999999999999

ser = serial.Serial(finalPort, 115200)



if (finalPort != ""):
    while True:
        serIn = ser.readline().decode().strip()
        if serIn == "0":
            start = time.perf_counter()
            print(start)
        if serIn == "interspace1.0all done!":
            break
        else:
            print(serIn)
    end = time.perf_counter()
    print(end)
    timeComp = end - start
    print(timeComp)
    print (((timeComp/ 750) * 1000))


else:
    print("The module was not detected. The module must not be connected to the device. Please reconnect and try to run this program again.")




