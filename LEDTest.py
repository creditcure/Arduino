import RPi.GPIO as GPIO
import time

LedPin11, LedPin13, LedPin15 = 11, 13, 15

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(LedPin11, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setup(LedPin13, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setup(LedPin15, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.output(LedPin11, GPIO.HIGH) # Set LedPin high(+3.3V) to turn on led
    GPIO.output(LedPin13, GPIO.HIGH)  # led on
    GPIO.output(LedPin15, GPIO.HIGH)  # led on

def blink():
  while True:
    GPIO.output(LedPin11, GPIO.HIGH)  # led on
    GPIO.output(LedPin13, GPIO.HIGH)  # led on
    GPIO.output(LedPin15, GPIO.HIGH)  # led on
    time.sleep(1)
    GPIO.output(LedPin11, GPIO.LOW) # led off
    GPIO.output(LedPin13, GPIO.LOW)  # led off
    GPIO.output(LedPin15, GPIO.LOW)  # led off
    time.sleep(1)
def destroy():
    GPIO.output(LedPin11, GPIO.LOW) # led off
    GPIO.output(LedPin13, GPIO.LOW)  # led off
    GPIO.output(LedPin15, GPIO.LOW)  # led off
    GPIO.cleanup()                  # Release resource

if __name__ == '__main__':     # Program start from here
  setup()
  try:
    blink()
  except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    destroy()