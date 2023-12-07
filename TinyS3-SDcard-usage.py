# SD-Card Reader code for the 'Unexpected Maker RTC Logger Shield for TinyPico and TinyS2/S3'
# This code has the pin configurate for the TinyS3, different models may require different pin configurations.
# See the pinout card that you recieved when you purchased your device.
# This code example has been modified from the IO Expander module SD card example from Unexpected Maker.
# My portions of the code can be copied/modified and used in any fashion you desire.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND!
'''
Copyright 2019 Unexpected Maker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import machine
import os
from machine import Pin


# Pin Setup per the pinout card for the TinyS3/RTC Logger Shield.
SPI_SS = Pin(34)
SPI_MOSI = Pin(35, Pin.OUT)
SPI_SCK = Pin(36)
SPI_MISO = Pin(37, Pin.IN)


# Check to see if no SD card is active/inserted. Should just print whatever files you have in / along
# with any subfolder names such as /lib will show as 'lib'. You you should at least have a boot.py file show up.
print(os.listdir())


# Create SPI instance of SD card using the pinouts from the card.
sd = machine.SDCard(slot=2, sck=SPI_SCK, miso=SPI_MISO, mosi=SPI_MOSI, cs=SPI_SS)
# The TinyS3 has a total of 4 slots (0-3) however the first two are used up by the ESP32 leaving slot 2 and 3 for use.


print(sd.info())
# At this point if you get an error is likely pin configuration or perhaps an incompatible SD card.
# I have tried many brands and sizes of cards and they all work fine. Make sure they are MS-DOS FAT32 formatted prior!
# Assuming everything is working besides seeing any files you may have on the TinyS3 you should see two sets of
# numbers in parenthesis such as (4026531840, 512) which for this
# particular SD card means its a 4GB card with 512 byets per sector (default).


# Mount the card with a name of 'sd'
os.mount(sd, '/sd')


# This command has be nested into a print statement for the purpose of displaying the contents of the TinyS3. To
# ensure you are seeing what you expect. If everything works you should see a folder named 'sd' along with your files.
# you can comment out the sd.info() if you want once its working so you do not see the file size/sector size.
print(os.listdir())
print("-------Line Break-------")
# Everything above this line is from the listdir() and info() functions. Below shows the SD card contents if any.
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

# Unmount
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

# At this point you can use the SD card for storage again. Remember close() your read/write/appends!
# And once fully done with the SD unmount and de-init the card. AKA like "safely removing" a USB drive from a computer.


# unmount and de-init once you have finished completely.
os.umount('/sd')
sd.deinit()

# This ends the code for the SD card. Obvisouly this is heavily commented for folks out there that are still learning
# the basics and need a little help, I'm no expert and doing this actually helps me as well!
# I have tested SD cards as large as 256GB. There is always a possible some SD card doesn't work. I ran into this issue
# on another board (Raspberry Pico) so have a few cards to try if you are unable to get the sd.info() working right.
# Make sure its formatted MSDOS-FAT32. If you own a Apple computer the native built disk utility does a great job.
# Remember this code is specific to the Unexpected Maker TinyS3 MCU. If you are using an S2 or TinyPico
# the configuratinon on the pins is different. Follow the pinout card that came with the RTC Logger Shield.

# This code is obvisouly very rough around the edges, I am going to work on putting together a version that can be
# called as a class or maybe a series of functions to streamline your code. I wanted to upload this just in case
# you are still learning MicroPython and need a little help getting started. Feel free to use whatever
# portions of this code that help you out. As always a huge thanks to the owner of Unexpected Maker - Seon.
# He is a great person and has always been helpful. I'm going to clean up this code so stay tuned to an updated version.
# After I clean up the code I am going to work on the RTC as well as the two I2C STEMMA interfaces so that everything
# is nice and streamlined. If this code makes you role your eyes well its probaly not for you, its for beginners such
# as myself and many others. I invite any UM hardware owner to join us on the UM discord channel. It is very helpful.
# I am an independant party and have no ties to Unexpected Maker. I'm just a fan, and slowly becoming a programmer!
# Happy logging!!


