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
with f as open("comm.txt", "r"):
    inpList = f.read().split("\n")

match inpList[0]:
    case "message":


while True:
