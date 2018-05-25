import bluetooth
import time
import RPi.GPIO as GPIO
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
LedPin11, LedPin13, LedPin15 = 11, 13, 15
pushButton29, pushButton31, pushButton33 = 29, 31, 33
expenseValue = 0 # Expense Value to Display on LCD
def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(LedPin11, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setup(LedPin13, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setup(LedPin15, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.output(LedPin11, GPIO.LOW) # Set LedPin high(+3.3V) to turn on led
    GPIO.output(LedPin13, GPIO.LOW)  # led on
    GPIO.output(LedPin15, GPIO.LOW)  # led on
    GPIO.setup(pushButton29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(pushButton31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(pushButton33, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def blink(led):
  while True:
    GPIO.output(led, GPIO.HIGH)  # led on
    time.sleep(1)
    GPIO.output(led, GPIO.LOW) # led off
    time.sleep(1)
def destroy():
    GPIO.output(LedPin11, GPIO.LOW) # led off
    GPIO.output(LedPin13, GPIO.LOW)  # led off
    GPIO.output(LedPin15, GPIO.LOW)  # led off
    GPIO.cleanup()                  # Release resource
def expense():
    while True:
    onesDigit = GPIO.input(pushButton29)
    tensDigit = GPIO.input(pushButton31)
    send = GPIO.input(pushButton33)
    if (onesDigit == False):
        expenseValue += 1
        refreshCardImage()
    if (tensDigit == False):
        expenseValue += 10
        refreshCardImage()
    if (send == False):
        refreshCardImage()
        break
    time.sleep(0.3)
    
# Create TFT LCD display class.
disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))

# Initialize display.
disp.begin()

# Clear the display to a red background.
# Can pass any tuple of red, green, blue values (from 0 to 255 each).
disp.clear((102, 153, 204))

# Alternatively can clear to a black screen by calling:
# disp.clear()

# Load default font.
font = ImageFont.load_default()

# Alternative Font
font = ImageFont.truetype('/home/pi/Desktop/verdana.ttf', 20)

# Get a PIL Draw object to start drawing on the display buffer.
draw = disp.draw()

def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimagedestroy = Image.new('RGBA', (width, height), (0,0,0,0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0,0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the image, using it as a mask for transparency.
    image.paste(rotated, position, rotated)
    
def refreshCardImage():
    disp.clear((102, 153, 204))
    # Virtual Credit Card number
    draw_rotated_text(disp.buffer, data, (35, 35), 90, font, fill=(255,255,255))
    # Expiration Date
    draw_rotated_text(disp.buffer, '01/24', (70, 180), 90, font, fill=(255,255,255))
    # Special Code
    draw_rotated_text(disp.buffer, '123', (70, 80), 90, font, fill=(255,255,255))
    # Expense
    draw_rotated_text(disp.buffer, 'Expense: ' + str(sendValue), (100, 80), 90, font, fill=(255,255,255))
    
name='CreditCureDemo'
target_name='Pixel XL'
uuid='00001101-0000-1000-8000-012321232123'

def runServer():
    serverSocket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    port = bluetooth.PORT_ANY
    serverSocket.bind(("",port))
    print ('Listening...')
    blink(LedPin11)
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
    blink(LedPin13)
    # Virtual Credit Card number
    draw_rotated_text(disp.buffer, data, (35, 35), 90, font, fill=(255,255,255))
    # Expiration Date
    draw_rotated_text(disp.buffer, '01/24', (70, 180), 90, font, fill=(255,255,255))
    # Special Code
    draw_rotated_text(disp.buffer, '123', (70, 80), 90, font, fill=(255,255,255))
    # Expense
    draw_rotated_text(disp.buffer, 'Expense: ' + str(sendValue), (100, 80), 90, font, fill=(255,255,255))
    blink(LedPin15)
    expense()
    disp.display()
    inputSocket.close()
    serverSocket.close()
    destroy()
setup()
runServer()
