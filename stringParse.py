speedOfLight = 3_000_000_000


# EXAMPLE MESSAGE: " f-1230123f-123-123Hello World!" 
"""
    TRANSLATION: 
        
        version: " ": str
        units: "feet": str
        coordinates: (-123, 123): (int, int)
        message: "Hello World!"



"""

def parse_message(message):
    # Extract x and y coordinates from the message
    x = int(message[15:18])
    y = int(message[18:21])
    return x, y

def trilaterate(inp1, t1, inp2, t2, inp3, t3): 
    x1, y1 = parse_message(inp1)
    x2, y2 = parse_message(inp2)
    x3, y3 = parse_message(inp3)
    
    r1 = t1 * speedOfLight
    r2 = t2 * speedOfLight
    r3 = t3 * speedOfLight
    
    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
    
    D = 2 * (x3 - x2)
    E = 2 * (y3 - y2)
    F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
    
    denominator = E * A - B * D
    if denominator == 0:
        print("Denominator is zero, cannot compute coordinates.")
    
    x = (C * E - F * B) / denominator
    y = (C * D - A * F) / (B * D - A * E)
    
    return x, y

if __name__ == "__main__":
    print(trilaterate("interspace1.1m123123", 0.21795, "interspace1.1m300123", 0.003, "interspace1.1m450223", 0.0001))