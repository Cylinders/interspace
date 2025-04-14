import board
import busio
import digitalio
print("interspace1.0running")
import adafruit_rfm69
print("interspace1.0imported")
RADIO_FREQ_MHZ = 915.0  

CS = digitalio.DigitalInOut(board.GP17)
RESET = digitalio.DigitalInOut(board.GP20)

#TODO: Are these right lmao? !

# Define the onboard LED
LED = digitalio.DigitalInOut(board.LED)
LED.direction = digitalio.Direction.OUTPUT

# Initialize SPI bus.
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
print("interspace1.0SPI Setup")
# Initialze RFM radio
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)
print("interspace1.0radio setup")
# Note that the radio is configured in LoRa mode so you can't control sync
# word, encryption, frequency deviation, or other settings!

# You can however adjust the transmit power (in dB).  The default is 13 dB but
# high power radios like the RFM95 can go up to 23 dB:
rfm69.tx_power = 13

print("interspace1.0power")

# Send a packet.  Note you can only send a packet up to 60 bytes in length.
rfm69.send(bytes("Hello world!\r\n", "utf-8"))

print("interspace1.0Sent Hello World message!")
print("interspace1.0Waiting for packets...")

while True:
    packet = rfm69.receive()
    # packet = rfm9x.receive(timeout=5.0)
    if packet is None:
        # Packet has not been received
        LED.value = False
        print("interspace1.0Received nothing! Listening again...")
    else:
        
        # Received a packet!
        LED.value = True
        # Print out the raw bytes of the packet:
        print("interspace1.0Received (raw bytes): {0}".format(packet))
        packet_text = str(packet, "ascii")
        print("interspace1.0Received (ASCII): {0}".format(packet_text))
        # Also read the RSSI (signal strength) of the last received message and
        # print it.
        rssi = rfm69.last_rssi
        print("interspace1.0Received signal strength: {0} dB".format(rssi))
