import board
import busio
import digitalio
print("interspace1.0running")
import adafruit_rfm69
print("interspace1.0imported")
LP = "1e2a"
RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.GP17)
RESET = digitalio.DigitalInOut(board.GP20)

LED = digitalio.DigitalInOut(board.LED)
LED.direction = digitalio.Direction.OUTPUT
LED.value = True

spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
print("interspace1.0SPI Setup")

rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)
print("interspace1.0radio setup")
rfm69.tx_power = 13
print("interspace1.0power")
try:
    while True:
        packet = rfm69.receive()
        if packet is None:
            print("gps request")

        else:
            x = str(packet, "ascii")
            if x == LP:
                rfm69.send(bytes("$\r\n", "utf-8"))
except:
    while True:
        LED.value = not LED.value
        time.sleep(0.5)
