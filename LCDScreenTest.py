from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import time
import RPi.GPIO as gpio

pushButton3, pushButton5, pushButton18 = 3, 5, 40
sendValue = 0
# Raspberry Pi configuration.
DC = 18
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Create TFT LCD display class.
disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
# Setup board and pins
gpio.setup(pushButton18, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(pushButton3, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(pushButton5, gpio.IN, pull_up_down=gpio.PUD_UP)
# Initialize display.
disp.begin()

# Clear the display to a red background.
# Can pass any tuple of red, green, blue values (from 0 to 255 each).
disp.clear((102, 153, 204))

# Alternatively can clear to a black screen by calling:
# disp.clear()

# Get a PIL Draw object to start drawing on the display buffer.
draw = disp.draw()

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('verdana.ttf', 20)

# Define a function to create rotated text.  Unfortunately PIL doesn't have good
# native support for rotated fonts, but this function can be used to make a
# text image and rotate it so it's easy to paste in the buffer.
def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0,0,0,0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0,0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the image, using it as a mask for transparency.
    image.paste(rotated, position, rotated)

# Write two lines of white text on the buffer, rotated 90 degrees counter clockwise. 240x320 LCD

# Real Credit Card number
draw_rotated_text(disp.buffer, '1234-1234-1234-1234', (35, 35), 90, font, fill=(255,255,255))
# Expiration Date
draw_rotated_text(disp.buffer, '01/24', (70, 180), 90, font, fill=(255,255,255))
# Special Code
draw_rotated_text(disp.buffer, '123', (70, 80), 90, font, fill=(255,255,255))
draw_rotated_text(disp.buffer, 'Expense: ' + str(sendValue), (110, 90), 90, font, fill=(255,255,255))
disp.display()
# Write buffer to display hardware, must be called to make things visible on the
# display!

### refresh image
while True:
    onesDigit = gpio.input(pushButton18)
    tensDigit = gpio.input(pushButton5)
    send = gpio.input(pushButton3)
    print "in whike loo"
    if (onesDigit == False):
        sendValue += 1
        print(sendValue)
        disp.clear((102, 153, 204))
        # Virtual Credit Card number
        draw_rotated_text(disp.buffer, '1234-5678-9012-3456', (35, 35), 90, font, fill=(255,255,255))
        # Expiration Date
        draw_rotated_text(disp.buffer, '11/05', (70, 180), 90, font, fill=(255,255,255))
        # Special Code
        draw_rotated_text(disp.buffer, '567', (70, 80), 90, font, fill=(255,255,255))
        draw_rotated_text(disp.buffer, 'Expense: ' + str(sendValue), (110, 90), 90, font, fill=(255,255,255))
        disp.display()
    if (tensDigit == False):
        sendValue += 10
        print(sendValue)
        disp.clear((102, 153, 204))
        # Virtual Credit Card number
        draw_rotated_text(disp.buffer, '1234-1234-1234-1234', (35, 35), 90, font, fill=(255,255,255))
        # Expiration Date
        draw_rotated_text(disp.buffer, '01/24', (70, 180), 90, font, fill=(255,255,255))
        # Special Code
        draw_rotated_text(disp.buffer, '123', (70, 80), 90, font, fill=(255,255,255))
        draw_rotated_text(disp.buffer, 'Expense: ' + str(sendValue), (110, 90), 90, font, fill=(255,255,255))
        disp.display()
    if (send == False):
        break
    time.sleep(0.3)



