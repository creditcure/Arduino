import RPi.GPIO as GPIO
import time

pushButton29, pushButton31, pushButton33 = 29, 31, 33
# Setup board and pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pushButton29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pushButton31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pushButton33, GPIO.IN, pull_up_down=GPIO.PUD_UP)
sendValue = 0
while True:
    onesDigit = GPIO.input(pushButton29)
    tensDigit = GPIO.input(pushButton31)
    send = GPIO.input(pushButton33)
    if (onesDigit == False):
        sendValue += 1
        print(sendValue)
    if (tensDigit == False):
        sendValue += 10
        print(sendValue)
    if (send == False):
        break
    time.sleep(0.3)




