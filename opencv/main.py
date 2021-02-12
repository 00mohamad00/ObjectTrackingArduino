import cv2
import numpy as np
import serial

ser = serial.Serial('/dev/tty.usbserial-0001')

lower = np.array([100, 150, 150], np.uint8)
upper = np.array([130, 255, 255], np.uint8)

# video = cv2.VideoCapture(1)

ip = 'http://192.168.1.100:8080/video'
video = cv2.VideoCapture(ip)

check, frame = video.read()
height = frame.shape[0]
width = frame.shape[1]
start_point = (width//2, 0)
end_point = (width//2, height)
color = (0, 255, 0)
thickness = 5

counter = 0

while True:
    check, frame = video.read()

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    mask = cv2.inRange(hsv_frame, lower, upper)

    output = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.line(output, start_point, end_point, color, thickness)

    M = cv2.moments(mask)
    if M['m00']:
        counter+=1
        print(counter)
        x = round(M['m10'] / M['m00'])
        y = round(M['m01'] / M['m00'])
        # print("center X : '{}'".format(x))
        # print("center Y : '{}'".format(y))
        dx = x - (width//2)
        dx = -dx

        dx = int((dx/(width//2)) * 90)

        print('dx is :', dx)

        if abs(dx) < 15:
            dx = 0

        if counter == 30:
            counter=0
            ser.write(str(90+dx).encode())

        cv2.line(output, (x, 0), (x, height), (255, 0, 0), thickness)



    # cv2.imshow('video', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('output', output)


    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
video.release()
