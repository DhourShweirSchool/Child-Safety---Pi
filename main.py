import spidev
import time
import os
from twilio.rest import TwilioRestClient
import RPi.GPIO as GPIO
import commands


GPIO.setmode(GPIO.BOARD)
GPIO.setup (13, GPIO.OUT)
GPIO.setup (15, GPIO.OUT)


spi = spidev.SpiDev()
spi.open(0,1)
output = commands.getoutput("sudo python /home/pi/Adafruit_Python_DHT/examples/AdafruitDHT.py 11 4")


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

# opening the window
def openwindow():
    GPIO.output(13,GPIO.LOW)
    GPIO.output(15,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(15,GPIO.LOW)
    time.sleep(1)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(15,GPIO.LOW)

def sendsms(): 
# put your own credentials here
#enter your details of twilio here with the message and number and from
    ACCOUNT_SID = ""
    AUTH_TOKEN = ""
 
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
 
    client.messages.create(
        to="+961",
        from_="CarAlert",
        body="Oxygen Level is Below 19%",  
)

s = 0


#here is our main loop where we print the percentage of O2 the sensor is give us and the temperature along with the humid when the temp reaches below 19% it will send an sms using function we defined earlier

while 1==1:
    

    p = readadc(0)
    v = convertVolts(p)
    o = convertToO2(v)


    print o
    print output
    time.sleep(1)
    if o < 19 and s == 0:
        print("Car is Low on Oxygen Contacting Help.")
        sendsms()
        openwindow()
        s = 1
    if o > 19:
        s = 0
        
    
