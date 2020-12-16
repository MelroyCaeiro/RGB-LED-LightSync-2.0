# RGB-LED-LightSync-2.0
Python script that extracts two dominant colours (RGB colour codes) in an album art from Spotify to be displayed on WS2812B LED strips wirelessly, using an ESP32 microcontroller as a webserver


.py script - run on a device with support for the Python interpreter (PC, Raspberry Pi)

.ino code  - compiled onto an ESP32/Arduino via the Arduino IDE

Update 1.0: Added SpotifyRGB.py (uses RGB colour model to identify most commonly occuring colour; calculates distance score between each colour to find colours with smallest standard deviation among one another, and sends RGB value to a webserver's IP address hosted on an ESP32)

Update 1.1: Added SpotifyHSV.py (uses HSV colour model to identify dominant hue; modal HSV value is selected, process done twice with options to set deviation between hues, as well as to reject colours below a certain saturation and value/lightness. HSV values are then converted to RGB values to be sent to the ESP32's webserver)

