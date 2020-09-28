# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time, math
from pyb import UART

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.


#两个舵机同一时间只动一个，动一个停下来另一个

def moveX(x):
    global moveFlag
    moveFlag = True
    uart.write(stopUpAndDown)
    if x < leftX:
        uart.write(turnRight)
    else:
        uart.write(turnLeft)

def moveY(y):
    global moveFlag
    moveFlag = True
    uart.write(stopLeftAndRight)
    if y < downY:
        uart.write(turnDown)
    else:
        uart.write(turnUp)

def findMaxBlob(blobs):
    maxBlob = blobs[0]
    for i in blobs:
        if (i.area() > maxBlob.area()):
            maxBlob = i
    return maxBlob

def imgAnalysis(img):
    global moveFlag
    blobs = img.find_blobs(redThreshold)
    if (len(blobs) > 0):
        maxBlob = findMaxBlob(blobs)
        centerPointX = maxBlob.cx()
        centerPointY = maxBlob.cy()
        img.draw_keypoints([(centerPointX, centerPointY, 0)])
        #两个都不在范围内，让X和Y中距离远的靠近
        a = centerPointX < leftX or centerPointX > rightX
        b = centerPointY < downY or centerPointY > upY
        if (a and b):
            XDistance = min(abs(centerPointX - leftX), abs(centerPointX - rightX))
            YDistance = min(abs(centerPointY - upY), abs(centerPointY - downY))
            if (XDistance > YDistance):
                moveX(centerPointX)
            else:
                moveY(centerPointY)
        elif a:
            moveX(centerPointX)
        elif b:
            moveY(centerPointY)
        else:
            if moveFlag:
                moveFlag = False
                uart.write(stopLeftAndRight)
                uart.write(stopUpAndDown)

redThreshold = [(0, 100, 18, 127, -16, 127)]

img = sensor.snapshot()

leftX = img.width() * 2 / 5
rightX = img.width() * 3 / 5
downY = img.height() * 2 / 5
upY = img.height() * 3 / 5

start = bytearray()
turnLeft = bytearray()
turnRight = bytearray()
turnUp = bytearray()
turnDown = bytearray()
stopLeftAndRight = bytearray()
stopUpAndDown = bytearray()

moveFlag = False

startWorkingFlag = False

uart = UART(3, 19200)

while(True):
    if startWorkingFlag:
        clock.tick()                    # Update the FPS clock.
        img = sensor.snapshot()         # Take a picture and return the image.
        imgAnalysis(img)
        img.binary(redThreshold)
    else:
        uart.write(start)
        readArray = uart.read()
        if 1:   #判断下位机返回的数组
            startWorkingFlag = True

