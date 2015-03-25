# OctopiLcd
Basic LCD Display Plugin for OctoPrint

Simple Python script to update a LCD display with print data from OctoPrint on a raspberry PI

I wanted to have a read out on the OctoPrint setup so when I go out to the garage where the printer is I can see things like progress of the print. THis assumes you already have a Raspberry Pi running OctoPrint

These are the things I got from Adafruit.com to set this up:
  Half-size breadboard PID: 64
  Premium Male/Male Jumper Wires - 40 x 6" (150mm) PID: 758
  RGB backlight positive LCD 16x2 + extras - black on RGB PID: 398
  Assembled Pi Cobbler Plus - Breakout Cable for Pi B+/A+/Pi 2 PID: 2029

Here are the steps to set it up:

Step 1:
  Wire up the LCD according to these instructions:
  https://learn.adafruit.com/character-lcd-with-raspberry-pi-or-beaglebone-black/usage
  Install AdaFruit CHAR_LCD libraries as shown in tutorial as well.
  
Step 2:
  Open octoprint web interface.  
  Select Settings->API
  Select enable
  Copy the Key

Step 3:
  On PI
  Edit OctoPiLCD.py ( from shell: nano OctoPiLCD.py)
  On line 10 paste the value from above into key = 'Your key here'
  in nano: ^X to exit, Y to save, Enter to confirm name

Step 4:
  Edit ~/.octoprint/config.yaml 
  If you don't have events add the following to the end of the file:
  Otherwise just add the PrintStarted Event
  
  events:
    enabled: True
    subscriptions:
    - event: PrintStarted
      command: python ~/OctoPiLCD/OctoPiLCD.py
      type: system

