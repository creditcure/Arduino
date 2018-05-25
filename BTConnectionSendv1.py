import bluetooth
import time
import RPi.GPIO as gpio
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

# Raspberry Pi configuration.
DC = 18
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Create TFT LCD display class.
disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
pushButton3, pushButton5, pushButton18 = 3, 5, 40
gpio.setup(pushButton18, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(pushButton3, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(pushButton5, gpio.IN, pull_up_down=gpio.PUD_UP)
# Initialize display.
disp.begin()

# Clear the display to a red background.
# Can pass any tuple of red, green, blue values (from 0 to 255 each).
sendValue = 0

# Alternatively can clear to a black screen by calling:
# disp.clear()

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('Minecraftia.ttf', 46)
font = ImageFont.truetype('/home/pi/Desktop/Hardware/verdana.ttf', 20)
# Get a PIL Draw object to start drawing on the display buffer.
draw = disp.draw()

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

name='CreditCureDemo'
target_name='Pixel XL'
uuid='00001101-0000-1000-8000-012321232123'
# Display original card
disp.clear((102, 153, 204))
# Real Credit Card number
draw_rotated_text(disp.buffer, '4257-3362-0891-2361', (35, 35), 90, font, fill=(255,255,255))
# Expiration Date
draw_rotated_text(disp.buffer, '06/23', (70, 180), 90, font, fill=(255,255,255))
# Special Code
draw_rotated_text(disp.buffer, '834', (70, 80), 90, font, fill=(255,255,255))
draw_rotated_text(disp.buffer, "Waiting for Connection...", (200, 30), 90, font, fill=(255,255,255))
disp.display()
def refresh(data=[], sendValue=0):
    disp.clear((102, 153, 204))
    # Virtual Credit Card number
    draw_rotated_text(disp.buffer, data[0], (35, 35), 90, font, fill=(255,255,255))
    # Expiration Date
    draw_rotated_text(disp.buffer, data[1], (70, 180), 90, font, fill=(255,255,255))
    # Special Code
    draw_rotated_text(disp.buffer, data[2], (70, 80), 90, font, fill=(255,255,255))
    draw_rotated_text(disp.buffer, 'Expense: ' + str(sendValue), (110, 90), 90, font, fill=(255,255,255))
    disp.display() 
def expense(data, sendValue):
    ### refresh image
    refresh(data)
    while True:
        onesDigit = gpio.input(pushButton18)
        tensDigit = gpio.input(pushButton5)
        send = gpio.input(pushButton3)
        print "in while loop"
        if (onesDigit == False):
            sendValue += 1
            print(sendValue)
            refresh(data, sendValue)
        if (tensDigit == False):
            sendValue += 10
            print(sendValue)
            refresh(data, sendValue)
        if (send == False):
            return sendValue
            break
        time.sleep(0.3)
        
def runServer():
    sendValue=0
    serverSocket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    port = bluetooth.PORT_ANY
    serverSocket.bind(("",port))
    print ('Listening...')
    serverSocket.listen(1)
    port = serverSocket.getsockname()[1]
    bluetooth.advertise_service(serverSocket,
                      "CreditCureDemo",
                      service_id = uuid,
                      service_classes = [uuid, bluetooth.SERIAL_PORT_CLASS],
                      profiles = [bluetooth.SERIAL_PORT_PROFILE])
    inputSocket, address=serverSocket.accept()
    print("Accepted connection from ",address)
    data = inputSocket.recv(1024)
    print("received [%s] " % data)
    data=data.split()
    print(data)
    disp.clear((102, 153, 204))
    disp.display() 
    # Virtual Credit Card number
    draw_rotated_text(disp.buffer, data[0], (35, 35), 90, font, fill=(255,255,255))
    # Expiration Date
    draw_rotated_text(disp.buffer, data[1], (70, 180), 90, font, fill=(255,255,255))
    # Special Code
    draw_rotated_text(disp.buffer, data[2], (70, 80), 90, font, fill=(255,255,255))
    draw_rotated_text(disp.buffer, 'Expense: ' + str(sendValue), (110, 90), 90, font, fill=(255,255,255))
    exp = expense(data, 0)
    disp.display()
    print(exp)
    inputSocket.send(str(exp).encode())
    serverSocket.close()
runServer()