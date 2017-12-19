#  Circuit Playground Express Color Sensing Example
#  Use the NeoPixel RGB LED and light sensor on the Circuit Playground Express board to
#  do basic color detection.  By quickly flashing full red, green, and blue color
#  light from the NeoPixel the light sensor can read the intensity of the
#  reflected light and roughly approximate the color of the object.
#
#  You can press and release button A or button B to do a color sense and
#  print the red, green, blue component values to the REPL 
#  (Button B uses a verbose option and will also print out raw values).
#
#  In addition all the NeoPixels on
#  the board will be lit up to the detected color.  You should hold a brightly
#  colored object right above the light sensor and NeoPixel #1 (upper
#  left part of board, look for the eye symbol next to the color sensor) when
#  performing the color sense.
# 
# Author: David Boyd
# Adapted from color_sense.ino by (Limor Fried & Tony DiCola)
# https://github.com/adafruit/Adafruit_CircuitPlayground/tree/master/examples/color_sense
#
# License: MIT License (https://opensource.org/licenses/MIT)
from adafruit_circuitplayground.express import cpx
import time
from simpleio import map_range

LIGHT_SETTLE_MS = 0.1 # 100 ms
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CLEAR = (0, 0, 0)

def sense_color(verbose_out = False):
    """
    Flash the neopixel closest to the light sensor Red, Green and
    Blue and measure the amount of light reflected by each color
    """
    cpx.pixels.fill(CLEAR) # clear pixels so they don't interfere
    time.sleep(.5)
    # Save the current pixel brightness so it can later be restored.  Then bump
    # the brightness to max to make sure the LED is as bright as possible for
    # the color readings.
    old_brightness = cpx.pixels.brightness
    cpx.pixels.brightness = 1.0
    
    # Set pixel 1 (next to the light sensor) to full red, green, blue
    # color and grab a light sensor reading.  Make sure to wait a bit
    # after changing pixel colors to let the light sensor change
    # resistance!
    cpx.pixels[1] = RED
    time.sleep(LIGHT_SETTLE_MS)
    raw_red = cpx.light
    cpx.pixels[1] = CLEAR
    time.sleep(.01)
    if verbose_out:
        print("raw red = {}".format(raw_red))
    
    cpx.pixels[1] = GREEN
    time.sleep(LIGHT_SETTLE_MS)
    raw_green = cpx.light
    cpx.pixels[1] = CLEAR
    time.sleep(.01)
    if verbose_out:
        print("raw green = {}".format(raw_green))

    cpx.pixels[1] = BLUE
    time.sleep(LIGHT_SETTLE_MS)
    raw_blue = cpx.light
    cpx.pixels[1] = CLEAR
    time.sleep(.01)
    if verbose_out:
        print("raw blue = {}".format(raw_blue))

    # Turn off the pixel and restore brightness, we're done with readings.
    cpx.pixels.brightness = old_brightness

    # Now scale down each of the raw readings to be within 0 to 255.  
    red = map_range(raw_red, 0, 255, 0, 330)
    green = map_range(raw_green, 0, 255, 0, 330)
    blue = map_range(raw_blue, 0, 255, 0, 330)

    return int(red), int(green), int(blue)


try:
    cpx.pixels.brightness = .2
    verbose = False

    while True:
        if cpx.button_a or cpx.button_b:
            verbose = cpx.button_b
            time.sleep(.05) # debounce
            if verbose:
                print("button pressed")
            while cpx.button_a or cpx.button_b:
                time.sleep(.01)
            r, g, b = sense_color(verbose)
            
            print("({}, {}, {})".format(r, g, b))
            cpx.pixels.fill((r, g, b))


except:
    cpx.pixels.fill(CLEAR)
