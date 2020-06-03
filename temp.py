import cv2
import time
import matplotlib.pyplot as plt
# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('test_vid.mp4')

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")

# Read until video is completed
time.sleep(2)
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        p = frame
        # Display the resulting frame
        cv2.imshow('Frame', frame)


    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release()
plt.imshow(p)
# Closes all the frames
cv2.destroyAllWindows()