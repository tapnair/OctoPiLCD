# OctoPiLCD
# Script for connecting an LCD display to Octoprint

import requests
from time import sleep
import time
import Adafruit_CharLCD as LCD
from types import NoneType

# Get your API KEy from Octoprint Settings panel
key = '21F625DE287F42A2879C9BEBFCFBDEE2'

class DisplayLCD(object):
    
    # Raspberry Pi configuration:
    lcd_rs = 27  # Change this to pin 21 on older revision Raspberry Pi's
    lcd_en = 22
    lcd_d4 = 25
    lcd_d5 = 24
    lcd_d6 = 23
    lcd_d7 = 18
    lcd_red = 4
    lcd_green = 17
    lcd_blue = 7  # Pin 7 is CE1
    
    # Define LCD column and row size for 16x2 LCD.
    lcd_columns = 16
    lcd_rows = 2
    
    # Initialize the LCD using the pins above.
    lcd = LCD.Adafruit_RGBCharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                                  lcd_columns, lcd_rows, lcd_red, lcd_green, lcd_blue)
    
    def updateDisplay(self, pData):
        self.lcd.clear()
        self.lcd.set_color(pData.colorR, pData.colorG, pData.colorB)
        self.lcd.message(pData.message)
    
    def sayGoodbye(self):
        self.lcd.clear()
        self.lcd.set_color(0,0,0)
        self.lcd.message("Done Printing")

class PrintData(object):
    # Setup Octopi API Interaction                               
    post_params = {}
    file_endpoint = 'http://octopi.local/api/files'
    job_endpoint = 'http://octopi.local/api/job'
    
    remain = 0
    fileName = 'None'
    completion = 0.0
    printTime = 0
    colorR = 0.0
    colorG = 0.0
    colorB = 0.0
    message = 'No Message'
    printing = True

    def __init__(self, key):
        # Nothing to do
        self.query_headers = {'X-Api-Key': key,
                              'Content-Type': 'application/json'}

    def updatePrintData(self):
        #file_response = requests.get(self.file_endpoint, headers=self.query_headers)
        #file_data = file_response.json()
        job_response = requests.get(self.job_endpoint, headers=self.query_headers)
        job_data = job_response.json()

        # Relevant paramters for simple retrieving
        self.remain = job_data['progress']['printTimeLeft']
        self.fileName = job_data['job']['file']['name']
        self.printTime = job_data['progress']['printTime']
        self.completion = job_data['progress']['completion']
    def checkPrinter(self):
        if isinstance(self.completion, NoneType):
            return False
        if self.completion < 100.0:
            return True
        
    def getRemain(self):
        if isinstance(self.remain, int):
            return time.strftime("%H:%M:%S", time.gmtime(self.remain))
        else:
            return 'None'

    def getPrintTime(self):
        if isinstance(self.printTime, int):
            return time.strftime("%H:%M:%S", time.gmtime(self.printTime))
        else:
            return 'None'

    def getCompletion(self):
        if isinstance(self.completion, NoneType):
            return 'None'
        else:
            return "%0.2f" % (self.completion)

    def setMessage1(self):
        self.message = "File: " + self.fileName + '\n' + "Cmpltd: " + self.getCompletion() + '%'
        self.colorR = 1.0
        self.colorG = 0.0
        self.colorB = 1.0

    def setMessage2(self):
        self.message = "Elpsd: " + self.getPrintTime() + '\n' + "Rmn: " + self.getRemain()
        self.colorR = 0.0
        self.colorG = 1.0
        self.colorB = 1.0


pData = PrintData(key)
dLCD = DisplayLCD()
test = True

while pData.checkPrinter():

    pData.updatePrintData()

    if test:
        pData.setMessage1()
        test = False
    else:
        pData.setMessage2()
        test = True

    dLCD.updateDisplay(pData)
    sleep(5)

dLCD.sayGoodbye()


