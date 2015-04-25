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

class PrintData(object):
    # Setup Octopi API Interaction                               
    post_params = {}
    file_endpoint = 'http://octopi.local/api/files'
    job_endpoint = 'http://octopi.local/api/job'
    printer_endpoint = 'http://octopi.local/api/printer'
    
    remain = 0
    fileName = 'None'
    completion = 0.0
    printTime = 0
    colorR = 0.0
    colorG = 0.0
    colorB = 0.0
    message = 'No Message'
    printing = True
    toolTemp = 0.0
    bedTemp = 0.0

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
        
        # Get Printer Data, only works if printer is connected
        printer_response = requests.get(self.printer_endpoint, headers=self.query_headers)
        printer_data = printer_response.json()
        self.toolTemp = printer_data['temps']['tool0']['actual']
        self.toolTarget = printer_data['temps']['tool0']['target']
        self.bedTemp = printer_data['temps']['bed']['actual']
        self.bedTarget = printer_data['temps']['bed']['target']
        
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
    
    def getToolTemp(self):
        if isinstance(self.toolTemp, NoneType):
            return 'N/A'
        else:
            return "%0.1f" % (self.toolTemp) + '/' + "%0.1f" % (self.toolTarget)
            
    def getBedTemp(self):
        if isinstance(self.bedTemp, NoneType):
            return 'N/A'
        else:
            return "%0.1f" % (self.bedTemp) + '/' + "%0.1f" % (self.bedTarget)
            
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
    
    def setMessage3(self):
        self.message = "Tmp: " + self.getToolTemp() + '\n' + "Bed: " + self.getBedTemp()
        self.colorR = 0.0
        self.colorG = 0.0
        self.colorB = 1.0

pData = PrintData(key)
dLCD = DisplayLCD()
test = 0

while pData.checkPrinter():

    pData.updatePrintData()

    if test == 0:
        pData.setMessage1()
        test = 1
    elif test == 1:
        pData.setMessage2()
        test = 2
    else:
        pData.setMessage3()
        test = 0
    
    dLCD.updateDisplay(pData)
    sleep(5)

while (pData.toolTemp > 50.0) | (pData.bedTemp > 30.0):
    
    pData.updatePrintData()
    
    pData.setMessage3()
    
    dLCD.updateDisplay(pData)
    sleep(1)

dLCD.sayGoodbye()

