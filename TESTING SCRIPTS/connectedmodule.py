import board
import busio
import digitalio
print("interspace1.0running")
import adafruit_rfm69
print("interspace1.0imported")
RADIO_FREQ_MHZ = 915.0

CS = digitalio.DigitalInOut(board.GP17)
RESET = digitalio.DigitalInOut(board.GP20)


LED = digitalio.DigitalInOut(board.LED)
LED.direction = digitalio.Direction.OUTPUT

spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
print("interspace1.0SPI Setup")
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)
print("interspace1.0radio setup")
rfm69.tx_power = 13



for j in range(100):
    rfm69.send(bytes("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\r\n", "utf-8"))
    count = 0
    while True:
        packet = rfm69.receive()
        if packet is None:
            count += 1
        else:
            break
        if count > 100:
            rfm69.send(bytes("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\r\n", "utf-8"))



print("interspace1.0all done!")
