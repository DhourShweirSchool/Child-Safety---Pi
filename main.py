import RPi.GPIO as GPIO
import dht11
import time
import datetime
import spidev
import os
from twilio.rest import TwilioRestClient

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

instance = dht11.DHT11(pin = 7)

k = 0


def temp():
    while True:
        result = instance.read()
        if result.is_valid():
            break
    print("Last valid input: " + str(datetime.datetime.now()))
    print("Temperature: %d C" % result.temperature )



GPIO.setup (13, GPIO.OUT)
GPIO.setup (15, GPIO.OUT)


spi = spidev.SpiDev()
spi.open(0,1)

def openwindow():
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(15,GPIO.LOW)
    time.sleep(1)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(15,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(15,GPIO.LOW)

def readadc(adcnum):
    if((adcnum > 7) or(adcnum < 0)):
        return -1
    r = spi.xfer2([1, (8+adcnum)<<4,0])
    adcout = ((r[1]&3) << 8 ) + r[2]
    return adcout



def convertVolts (data):
    volts = data*3.3 / 1024.0
    return volts

def convertToO2(data):
    value = data/121 * 10000
    value = value / 7.43
    return value


def sendsms(): 
# put your own credentials here
    ACCOUNT_SID = ""
    AUTH_TOKEN = ""
 
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
 
    client.messages.create(
        to="+961",
        from_="CarAlert",
        body="Oxygen Level is Below 19%",  
)


while True:
    p = readadc (0)
    v = convertVolts(p)
    o =  convertToO2(v)
    print 'Oxygen Level = ', o
    temp()
    result = instance.read()
    print '------------------------------------------------------------'

    
    if o < 19 and s == 0:
        print("Car is Low on Oxygen Contacting Help.")
        sendsms ()
        openwindow()
        s = 1
    if o > 19:
        s = 0
    
    if result.temperature > 28 and k == 0:
        print(" Temp too High")
        openwindow ()
        sendsms()
        k = 1
    if result.temperature < 28:
        k = 0
    time.sleep(3)
