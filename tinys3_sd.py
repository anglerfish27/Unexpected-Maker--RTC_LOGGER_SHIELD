#No point in trying to make functions when everything is already defined. Same script with minimal comments in it. Enjoy! RTC Portion coming next.

import machine
from machine import Pin

# Pin Setup per the pinout card for the TinyS3/RTC Logger Shield.
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
