import board
import busio
import digitalio
import time
import adafruit_rfm69

RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.GP17)
RESET = digitalio.DigitalInOut(board.GP20)
LED = digitalio.DigitalInOut(board.LED)
LED.direction = digitalio.Direction.OUTPUT
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)


rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm69.tx_power = 13



def routeMessage():
    pass

### CONSTANTS
inpList = []
LP = ""
with open("comms.txt", "r") as f:
    inpList = f.read().split("\n")
with open("self.txt", "r") as f:
    LP = f.read().split("\n")[0]


command = inpList[0]
if command == "m":
    rfm69.send(bytes(inpList[1] + LP  + inpList[2] + "\r\n", "utf-8")) # this works?
elif command == "g":
    rfm69.send(bytes("$\r\n", "utf-8"))
    receiveList = []
    while len(receiveList) < 2:
        packet = rfm69.receive()
        if packet is None or packet == "":
            pass
        else:
            packet = str(packet, "ascii")
            if packet.startswith("$"):
                receiveList.append(packet[1:])
    print(receiveList)
    #
elif command == "c":
    pass
elif command == "d":
    pass


# read loop
target = ""
sender = ""
content = ""
while True:
    print("success")
    rfm69.send(bytes("f102313this is a test message!\r\n", "utf-8"))
    
    packet = rfm69.receive()

    if packet is None or packet == "":
        pass
    else:
        LED.value = True
        packet = str(packet, "ascii")

        if packet.startswith("$"):
            rfm69.send(bytes("$" + LP + "\r\n", "utf-8"))
        target = packet[0:7]
        sender = packet[7:14]
        content = packet[15:]
        print("interspace1.0" + packet)
        print("interspaceg1.0" + rfm69.last_rssi)


        if content == "ruthvikvenkatesan":
            time.sleep(3)
            rfm69.send(bytes(sender + target + content + "\r\n", "utf-8"))
    # packet = rfm9x.receive(timeout=5.0)
    time.sleep(2)
    LED.value = not LED.value
