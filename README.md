# interspace
Modular Radio Network (Similar to Meshtastic)

## LIP SPECIFICATION 

LIP: Location Identification Protocol

Radio Modules have only 60 bytes of storage capacity. 

That is only 60 characters! (no duh)

In order to save space per message WITHOUT packetization for the GPS portion of the project, we are going to use a protocol designed specifically for Interspace: LIP. 

LIP defines a unit, then provides a coordinate. 

This means that only one module can be placed at any given geographical location. 

The units

An LIP Address begins with a character: 

"f" - foot (positive, positive)
"m" - metre (positive, positive)
"M" - mile (positive, positive) 
"k" - kilometre (positive, positive)


"g" - foot (positive, negative)
"m" - metre (positive, negative)
"M" - mile (positive, negative)
"k" - kilometre (positive, negative)


"h" - foot (negative, positive)
"m" - metre (positive, negative)
"M" - mile (positive, negative) 
"k" - kilometre (positive, negative)


"i" - foot (positive, positive)
"m" - metre (positive, positive)
"M" - mile (positive, positive) 
"k" - kilometre (positive, positive)

An LIP Address is followed by TWO THREE DIGIT INTEGERS:
The first digit of each integer determines their sign: 

0: positive
-: negative 

ex. 

"f-1230321": This LP refers to (-123 feet, 321 feet). 

### Message Packetization Protocol: 


If a message is longer than 60 characters, it can be partitioned into a seperate message: the first message will end with the phrase "*&^" (cutting off the final three characters)

The consequent message will also begin with "*&^": 

Both of these will need to be "trimmed out". 

This also means that an application designed to interface with Interspace (alliteration sounds cool) will need to check messages in order to ensure that the phrase "*&^" is not at the end of a message. 