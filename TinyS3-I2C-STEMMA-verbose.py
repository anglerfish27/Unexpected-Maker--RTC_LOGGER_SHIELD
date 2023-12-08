from bme680 import *
from machine import I2C, Pin
import time

# Defining ports for I2C interface, these are the default pins for the second I2C interface
# Remember that the TinyS3 and other ESP32 variants from Unexpected maker have *2* hardware based I2C interfaces.
# The nice thing about these ESP32s is you can you almost any pin for I2C / SPI and it will re-reoute internally
# to the HW I2C interface. I'm going here with the defaults from the pinout card.

# However you may use any other set of pins that are not being used or otherwise unusable.
# Keep in mind that if you are using the RTC from the RTC Logger Shield that is communicating over I2C. So
# essentially the RTC is using the one of two I2C HW interfaces.

# This means you can only use the 2 STEMMA
# ports at the same time on the shield if you are not using the on board RTC, otherwise you will have to use
# a software based I2C instance to have all 3 devices communicating on I2C (2 on the STEMMAs and the internal RTC)
# in this example I am using a common BME688 sensor for testing. I am using the second set of I2C pins defined
# on the pin out card but again you are free to choose your own. Since its pre-defined I just might as well
# use them. I named my pins I2C2 to follow the pinout diagram that came with the card. The SD card communicates
# of SPI so there is no concern there with lack of connections.


# Just your basic usage of I2C. Again this is for beginners like myself who need a bit of a walk through.
# If you know this stuff super well there's little value here for you if any.

# Pins defined per the pinout card.
I2C2_SDA = Pin(5)  
I2C2_SCL = Pin(4)  

#create your I2C instance
i2c = I2C(0, sda=Pin(5), scl=Pin(4))
bme = BME680_I2C(i2c)


TempF = ((9/5) * bme.temperature) + 32 
Humidity = bme.humidity
Pressure = bme.pressure

# Simple conversion of the temperature to F from C. and prints it 5 times with a 2 second delay.
# Again this is just testing code to make sure I'm getting the right data back from the BME sensor.
# I chose NOT to upload the BME sensor driver module. It belongs to Adafruit and can be found on their webpage,
# or their non compressed (.py) download of Circuitpython. I figured you are likely using a different sensor
# or hardware for your project.

for i in range(5):
    print(TempF)
    print(Humidity)
    print(Pressure)
    time.sleep(2)
    
    
# All of this code can be added to the "tinys3_sd_card.py I have uploaded and it will work fine.
# For a challenge maybe start logging the BME data on the SD card instead of just printing it out!
# After all that's what the shield is for "Logger".  :)
# I will provide this file which is verbose in comments and then another that incorporates the SD card.



