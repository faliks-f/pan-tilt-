# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time, math
from pyb import UART
from pyb import LED

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

def moveX(x):
    global moveFlag
    moveFlag = True
    if x < leftX:
        moveArray[2] = TURNRIGHT
    else:
        moveArray[2] = TURNLEFT

def moveY(y):
    global moveFlag
    global moveArray
    moveFlag = True
    if y < downY:
        moveArray[1] = TURNDOWN
    else:
        moveArray[1] = TURNUP

def findMaxBlob(blobs):
    maxBlob = blobs[0]
    for i in blobs:
        #img.draw_rectangle(i.rect(), color = (0, 0, 255),thickness = 3)
        if (i.area() > maxBlob.area() and i.area() > 1500 and i.area() < 5000):
            maxBlob = i
    return maxBlob

def imgAnalysis(img):
    global moveFlag
    global moveArray
    moveArray = bytearray([0x75, 0x00, 0x00, 0x00])
    blobs = img.find_blobs(redThreshold)
    if (len(blobs) > 0):
        maxBlob = findMaxBlob(blobs)
        if maxBlob.area() > 1500 and maxBlob.area() < 5000:
            print(maxBlob.area())
            img.draw_rectangle(maxBlob.rect(), color = (0, 0, 255),thickness = 3)
            centerPointX = maxBlob.cx()
            centerPointY = maxBlob.cy()
            img.draw_keypoints([(centerPointX, centerPointY, 0)])
            #两个都不在范围内，让X和Y中距离远的靠近
            a = centerPointX < leftX or centerPointX > rightX
            b = centerPointY < downY or centerPointY > upY
            if (a and b):
                moveX(centerPointX)
                moveY(centerPointY)
            elif a:
                moveX(centerPointX)
            elif b:
                moveY(centerPointY)
            else:
                if moveFlag:
                    moveFlag = False
            uart.write(moveArray)
            delay()

def delay():
    sum = 0
    for i in range(1, 100000):
        sum += 1

redThreshold = [(14, 38, 20, 64, -4, 46)]

img = sensor.snapshot()

leftX = img.width() * 2 / 5
rightX = img.width() * 3 / 5
downY = img.height() * 2 / 5
upY = img.height() * 3 / 5

TURNUP = 0x01
TURNDOWN = 0x02
TURNLEFT = 0x01
TURNRIGHT = 0x02

moveArray = bytearray([0x75, 0x00, 0x00, 0x00])
start = bytearray()

moveFlag = False

startWorkingFlag = False

uart = UART(3, 115200)
uart.init(115200, bits = 8, parity = None, stop = 1)

redLed = LED(1)

while(True):
    if startWorkingFlag:
        read = uart.read()
        print(read)
        clock.tick()                    # Update the FPS clock.
        img = sensor.snapshot()         # Take a picture and return the image.
        imgAnalysis(img)
        #img.binary(redThreshold)
    else:
        uart.write(start)
        readArray = uart.read()
        if 1:   #判断下位机返回的数组
            startWorkingFlag = True
            redLed.on()

