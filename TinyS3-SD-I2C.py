import machine
from machine import I2C, Pin
import time
from bme680 import *  # This will be device specific to your sensor.


# Pin Setup per the pinout card for the TinyS3/RTC Logger Shield SD-Card portion(SPI).
SPI_SS = Pin(34)
SPI_MOSI = Pin(35, Pin.OUT)
SPI_SCK = Pin(36)
SPI_MISO = Pin(37, Pin.IN)


sd = machine.SDCard(slot=2, sck=SPI_SCK, miso=SPI_MISO, mosi=SPI_MOSI, cs=SPI_SS)

print(sd.info())

# Mount the card with a name of 'sd'
os.mount(sd, '/sd')

print(os.listdir('/sd'))
# Writing to the SD card: in this case we tell the system to store the file in our new 'sd' folder with a file
# named sd_card_test_file.py
card = open('/sd/sd_card_test_file.py', 'w')
card.write("This data is being written to your SD card!\n")
card.close() # IMPORTANT--Always ensure you close your operation regardless of its read/write to avoid corruption.

# Reading the SD card.
card = open('/sd/sd_card_test_file.py', 'r')
print(card.read()) #You show now get a printout of the statement above or whatever you set it to do.
card.close()

# List SD card contents, you should see the file you created listed within the 'sd' folder.
print(os.listdir('/sd'))

# Append data to your existing file.
card = open('/sd/sd_card_test_file.py', 'a')
card.write("This data has been appended to your file name above on your SD card filesystem!\n")
card.close()

# read again
card = open('/sd/sd_card_test_file.py', 'r')
print(card.read()) # You should see your original statment + the appended statement.
card.close()

# Remove the file. Your 'sd' partition still exists of course, this is just a file delete.
os.remove('/sd/sd_card_test_file.py') # You can use: print(os.listdir()) to confirm your file is gone.

# Once you are all done reading/writing we want to shut down the SD card nicely with an unmount/de-init.

# Unmount / de-init once finished completely.
os.umount('/sd')  # You can confirm its gone with print(os.listdir())
sd.deinit()

print(sd.info()) # This will print again the size of your SD card and sector size.

# You CANNOT remount the drive at this point. You need to reinit and then mount it for use again.

# Reinit
sd = sd = machine.SDCard(slot=2, sck=SPI_SCK, miso=SPI_MISO, mosi=SPI_MOSI, cs=SPI_SS)

# Mount the SD card again.
os.mount(sd, '/sd')
print(os.listdir())
print(os.listdir('/sd'))  #At this point you should see your card listed as 'sd' or whatever name you used.

# Unmount and de-init once you have finished completely.
os.umount('/sd')
sd.deinit()

# All SD-Card related operations/code are done at this point, now we just move on to a simple short
# loop to test the BME68x sensor to ensure its working with the shield and SD-Card.
# This code is crude and its just for ensuring I'm getting good data back via I2C STEMMA.
# Ideally this code should be in line with standard python practices but for learning I wanted the data
# easily visible in your IDE on what you are working on.

# Pins Setup for I2C STEMMA port(s)
I2C2_SDA = Pin(5)  
I2C2_SCL = Pin(4)  


# Create your I2C STEMMA instance
i2c = I2C(0, sda=Pin(5), scl=Pin(4))
bme = BME680_I2C(i2c)

# Setup of some test objects needed to test the BME68X sensor
TempF = ((9/5) * bme.temperature) + 32 
Humidity = bme.humidity
Pressure = bme.pressure

# Print BME data 10x sleeping for 2 seconds in between interations.
for i in range(10):
    print(TempF)
    print(Humidity)
    print(Pressure)
    time.sleep(2)

