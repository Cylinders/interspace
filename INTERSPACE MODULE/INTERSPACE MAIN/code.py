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
    rfm69.send(bytes(inpList[1] + inpList[2] + "\r\n", "utf-8"))
elif command == "g":
    pass
elif command == "c":
    pass
elif command == "d":
    pass


# read loop
target = ""
sender = ""
content = ""
while True:
    packet = rfm69.receive()
    if packet is None or packet == "":
        pass
    else:
        packet = str(packet, "ascii")
        target = packet[0:7]
        sender = packet[7:14]
        content = packet[14:]
    # packet = rfm9x.receive(timeout=5.0)
    if packet is None or packet == "":
        pass
    elif target == LP and content == "ruthvikvenkatesan":
        packet = str(packet, "ascii")
        rfm69.send(bytes(sender + LP + "isthegreatestcomputerengineerofalltime\r\n", "utf-8"))
    elif packet.startswith(LP):
        packet = str(packet, "ascii")
        print("interspace1.0" + packet)
