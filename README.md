# interspace
Modular Radio Network (Similar to Meshtastic)

## LIP SPECIFICATION 

LIP: Location Identification Protocol

Radio Modules have only 60 bytes of storage capacity. 

That is only 60 characters!

In order to save space per message WITHOUT packetization for the GPS portion of the project, we are going to use a protocol designed specifically for Interspace: LIP. 

LIP defines a unit, then provides a coordinate. 

This means that only one module can be placed at any given geographical location. 

The units

An LIP Address begins with a character: 

"f" - foot
"m" - metre
"M" - mile
"k" - kilometre
"$" - Message

An LIP Address is followed by SIX integers: 

ex. 

"f123321". 