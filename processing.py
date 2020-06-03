import matplotlib.pyplot as plt #add all to requirments
import cv2 as cv
import numpy as np
import os, sys
import subprocess
import time
import imutils
from face_blurring import anonymize_face_pixelate
from face_blurring import anonymize_face_simple

class Processing():

    def __init__(self):
        self.video_tags = ['']
        self.pic_tags = ['']
        self.prototxtPath =  "models/deploy.prototxt"
        self.weightsPath = "models/res10_300x300_ssd_iter_140000.caffemodel"

    def is_img(self, filename):
        return


    def get_img(self, filename):
        #maybe other stuff
        plt.imread(filename)

    def blur_video(self, filename):
        cap = cv.VideoCapture(filename=filename)
        time.sleep(2)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        print(frame_width, frame_height)


        out = cv.VideoWriter('outpy.mp4', cv.VideoWriter_fourcc(*'MP4V'), 20, (frame_width, frame_height))

        net = cv.dnn.readNet(self.prototxtPath, self.weightsPath)
        if (cap.isOpened() == False):
            print("Unable to read camera feed")
            return

        val = True
        while val:
            ret, frame = cap.read()
            if not val:
                break

            else:
                cv.imshow('frame', frame)
                frame = imutils.resize(frame, width=400)

                (h, w) = frame.shape[:2]
                blob = cv.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

                # pass the blob through the network and obtain the face detections
                net.setInput(blob)
                detections = net.forward()

                # loop over the detections
                for i in range(0, detections.shape[2]):
                    # extract the confidence (i.e., probability) associated with
                    # the detection
                    confidence = detections[0, 0, i, 2]

                    # filter out weak detections by ensuring the confidence is
                    # greater than the minimum confidence
                    if confidence > .2:
                        # compute the (x, y)-coordinates of the bounding box for
                        # the object
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")
                        # extract the face ROI
                        face = frame[startY:endY, startX:endX]
                        face = anonymize_face_pixelate(face)
                        # store the blurred face in the output image
                        frame[startY:endY, startX:endX] = face
                out.write(frame)

        cap.release()
        out.release()
        cv.destroyAllWindows()

def main():
    vid_path = "test_vid.mp4"
    pro = Processing()
    pro.blur_video(vid_path)

if __name__ == '__main__':
    main()


