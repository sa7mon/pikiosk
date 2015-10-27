import time
from neopixel import *

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# Define functions which animate LEDs in various ways.
def whitePulse(strip, ceiling, wait_ms=20):
    for j in range(ceiling): 
        for i in range(strip.numPixels()):
            strip.setPixelColorRGB(i, 127, 127, 127)
        strip.show()
        time.sleep(wait_ms/1000.0)
        # Change the strips brightness
        strip.setBrightness(j)
        # Once we get to the top of the brightness, start fading down instead of up
        if j == (ceiling - 1):
            print "Hit the top!"
            for j in range((ceiling - 2), 0, -1):
                for i in range(strip.numPixels()):
                    strip.setPixelColorRGB(i, 127, 127, 127)
                strip.show()
                time.sleep(wait_ms/1000.0)
                # Change the strips brightness
                strip.setBrightness(j)

def solidColor(strip, brightness, R, G, B):
    for i in range(strip.numPixels()):
        strip.setPixelColorRGB(i,R,G,B)
    strip.setBrightness(brightness)
    strip.show()

# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print 'Press Ctrl-C to quit.'
    '''
    while True:
        whitePulse(strip, 150, 15)
    '''
    solidColor(strip,100,0,0,128)
