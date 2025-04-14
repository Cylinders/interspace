
import board
import busio
import digitalio
import time
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value=True
print("interspace1.0running")
import adafruit_rfm69
print("interspace1.0imported")
RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.GP17)
RESET = digitalio.DigitalInOut(board.GP20)

spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
print("interspace1.0SPI Setup")
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)
print("interspace1.0radio setup")
rfm69.tx_power = 13
print("interspace1.0power")
while True:
    print("loop")
    start = time.monotonic_ns()
    a = 0
    adjust = 0
    print(a)
    iterations = 40
    waitTime = 0.75
    rfm69.send(bytes("$\r\n", "utf-8"))
    b = 0
    packet = None
    c = time.monotonic()
    while packet is None:
        packet = rfm69.receive()
        print("packet: " + str(packet))
        a += 1
        print(a)
        if a > 1000:
            b = b + 1
            rfm69.send(bytes("1e2a\r\n", "utf-8"))
        if b > 100:
            print("Fail")
            break

    print(rfm69.rssi)

    print("interspace1.0distance in meters: " + str(-.65*rfm69.rssi - 88.4) )
