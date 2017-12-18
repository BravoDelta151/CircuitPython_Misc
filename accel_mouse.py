# Circuit Playground Express Accelerometer Mouse Example using Circuit Python
# Tilt Circuit Playground Express left/right and up/down to move your mouse, and
# press the left and right push buttons to click the mouse buttons!  Make sure
# the slide switch is in the on (+) position to enable the mouse, or slide into
# the off (-) position to disable it.  By default this assumes you hold
# Circuit Playground with the USB cable coming out the top.
# Author: David Boyd (adapted from Arduino sketch by Tony DiCola)
# License: MIT License (https://opensource.org/licenses/MIT)
from adafruit_circuitplayground.express import cpx
from adafruit_hid.mouse import Mouse
import time, math

mouse = Mouse()

# Configuration values to adjust the sensitivity and speed of the mouse.

# Minimum range of axis acceleration, values below this won't move the mouse at all.
# Maximum range of axis acceleration, values above this will move the mouse as fast as possible.
# Range of velocity for mouse movements.  The higher this value the faster the mouse will move.
# Scaling value to apply to mouse movement, this is useful to set to -1 to flip the axis movement.

# X axis (left/right)configuration:
XACCEL_MIN = 0.5 # 0.1  
XACCEL_MAX = 4.0 # 8.0   
XMOUSE_RANGE = 12.0 # 25.0 
XMOUSE_SCALE = -1 # CHANGE THIS IF DIRECTION IS OPPOSITE WHAT YOU WANT

# Y axis  (up/down) configuration:
# Note that the meaning of these values is exactly the same as the X axis above,
# just applied to the Y axis and up/down mouse movement.  You probably want to
# keep these values the same as for the X axis (which is the default, they just
# read the X axis values but you can override with custom values).
YACCEL_MIN = XACCEL_MIN
YACCEL_MAX = XACCEL_MAX
YMOUSE_RANGE = XMOUSE_RANGE
YMOUSE_SCALE = 1 # CHANGE THIS IF DIRECTION IS OPPOSITE WHAT YOU WANT

# Set False if holding Circuit Playground Express with USB cable facing up
# Set True to swap the X/Y axis.  If USB cable is to the right or left 
SWAP_AXES = False
# Interestingly, axes is the only word in English that can be the plural 
# of three different singular noun forms--ax, axe, and AXIS.

# Floating point linear interpolation function that takes a value inside one
# range and maps it to a new value inside another range.  This is used to transform
# each axis of acceleration to mouse velocity/speed. See this page for details
# on the equation: https://en.wikipedia.org/wiki/Linear_interpolation
def lerp(value, v_min, v_max, d_min, d_max):
    """
    Check if the input value is outside its value range (v_min < value > v_max) 
    and clamp to desired min/max values (d_min < value > d_max).
    """
    if value <= v_min:
        return d_min
    elif value > v_max:
        return d_max
    else:
        # compute the return value based on val's position within its range and
        #  the desired min & max.
        return d_min + (d_max - d_min)*((value-v_min)/(v_max-v_min))

def get_button_press():
    """
    Using a function to handle button press, this makes it easier to add
    additional debounce, sound or led indications to a button press
    """
    left = cpx.button_a
    right = cpx.button_b

    return left, right

def main():
    """
    Check if the slide switch is enabled (on +) and if not then just exit out
    and run the loop again.  This lets you turn on/off the mouse movement with
    the slide switch.
    """
    if cpx.switch:
            
        # Grab initial left & right button states to later check if they are pressed
        # or released.  Do this early in the loop so other processing can take some
        # time and the button state change can be detected.
        left_first, right_first = get_button_press()

        # Grab x, y acceleration values, z is ignored 
        x, y, z = cpx.acceleration
        
        # Use the magnitude of acceleration to interpolate the mouse velocity.
        x_mag = abs(x)
        x_mouse = lerp(x_mag, XACCEL_MIN, XACCEL_MAX, 0.0, XMOUSE_RANGE)

        y_mag = abs(y)
        y_mouse = lerp(y_mag, YACCEL_MIN, YACCEL_MAX, 0.0, YMOUSE_RANGE)

        # Change the mouse direction based on the direction of the acceleration.
        if x < 0:
            x_mouse *= -1.0
        if y < 0:
            y_mouse *= -1.0

        # Apply any global scaling to the axis (to flip it for example) and truncate
        # to an integer value.
        x_mouse = math.floor(x_mouse*XMOUSE_SCALE)
        y_mouse = math.floor(y_mouse*YMOUSE_SCALE)

        # Move mouse.
        if not SWAP_AXES:
            # Non-flipped axes, just map board X/Y to mouse X/Y.
            mouse.move(x = x_mouse, y = y_mouse)
        else:
            # Flipped axes, swap them around.
            mouse.move(x = y_mouse, y = x_mouse)

        # Small delay to wait for button state changes and slow down processing a bit.
        time.sleep(.01) 

        # Grab a second button state reading to check if the buttons were pressed or
        # released.
        left_second, right_second = get_button_press()

        # Check for left button pressed / released.
        if not left_first and left_second:
            # button was pressed
            mouse.press(Mouse.LEFT_BUTTON)
            pass
        elif left_first and not left_second:
            # button was released
            mouse.release(Mouse.LEFT_BUTTON)
            pass

        # Check for right button pressed / released.
        if not right_first and right_second:
            # button was pressed!
            mouse.press(Mouse.RIGHT_BUTTON)
        elif right_first and not right_second:
            # button was released!
            mouse.release(Mouse.RIGHT_BUTTON)


try:    
    # print one tme at the beginning if switch is off 
    if not cpx.switch:
        print("*****************************************************")
        print("*** mouse movement is off, slide switch to enable ***")
        print("*****************************************************")
    # Loop
    while True:
        main()

except KeyboardInterrupt:
    # perform any cleanup if ctrl-c is hit
    pass 
except Exception as e:    
    print("Exception:", str(e))
