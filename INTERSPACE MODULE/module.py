import time

#Location Protocol Identifier
LP = "f0123-456"
#Computer verification of serial inputs. 
ser = "interspace1.0"

def serialOut(message): 
    print(ser + LP + message)
def GPSOut(): 
    serialOut("$")
    
while True: 
    serialOut("Ruthvik Venkatesan Test Message")
    time.sleep(1)
    GPSOut()
    time.sleep(1)
    
