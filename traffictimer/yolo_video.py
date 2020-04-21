
import os
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import dlib
import cv2
maximumTotal=[0]
trackers = []
trackableObjects = {}
def count(vd):
    # load the COCO class labels our YOLO model was trained on
    labelsPath = os.path.sep.join(["yolo", "coco.names"])
    LABELS = open(labelsPath).read().strip().split("\n")
    totalFrames = 0
    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
                               dtype="uint8")

    # derive the paths to the YOLO weights and model configuration
    weightsPath = os.path.sep.join(["yolo", "yolov3.weights"])
    configPath = os.path.sep.join(["yolo", "yolov3.cfg"])

    # load our YOLO object detector trained on COCO dataset (80 classes)
    # and determine only the *output* layer names that we need from YOLO
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # initialize the video stream, pointer to output video file, and
    # frame dimensions
    vs = cv2.VideoCapture(vd)
    writer = None
    (W, H) = (None, None)

    # try to determine the total number of frames in the video file
    try:
        prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
            else cv2.CAP_PROP_FRAME_COUNT
        total = int(vs.get(prop))
        print("[INFO] {} total frames in video".format(total))

    # an error occurred while trying to determine the total
    # number of frames in the video file
    except:
        print("[INFO] could not determine # of frames in video")
        print("[INFO] no approx. completion time can be provided")
        total = -1

    # loop over frames from the video file stream
    while True:
        car = 0
        truck = 0
        person = 0
        bus = 0
        motorbike = 0
        bicycle = 0
        # read the next frame from the file
        (grabbed, frame) = vs.read()

        # if the frame was not grabbed, then we have reached the end
        # of the stream
        if not grabbed:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if totalFrames % 12 != 0:

            totalFrames += 1
        else:
            # if the frame dimensions are empty, grab them
            if W is None or H is None:
                (H, W) = frame.shape[:2]

            # construct a blob from the input frame and then perform a forward
            # pass of the YOLO object detector, giving us our bounding boxes
            # and associated probabilities
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
            net.setInput(blob)
            start = time.time()
            layerOutputs = net.forward(ln)

            end = time.time()

            # initialize our lists of detected bounding boxes, confidences,
            # and class IDs, respectively
            boxes = []
            confidences = []
            classIDs = []
            dsa = []
            rects = []

            # loop over each of the layer outputs
            for output in layerOutputs:
                # loop over each of the detections
                for detection in output:
                    # extract the class ID and confidence (i.e., probability)
                    # of the current object detection

                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]

                    # filter out weak predictions by ensuring the detected
                    # probability is greater than the minimum probability
                    if confidence > 0.6:
                        # scale the bounding box coordinates back relative to
                        # the size of the image, keeping in mind that YOLO
                        # actually returns the center (x, y)-coordinates of
                        # the bounding box followed by the boxes' width and
                        # height
                        box = detection[0:4] * np.array([W, H, W, H])

                        (centerX, centerY, width, height) = box.astype("int")

                        # use the center (x, y)-coordinates to derive the top
                        # and and left corner of the bounding box
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))
                        tracker = dlib.correlation_tracker()
                        rect = dlib.rectangle(x, y, x + width, y + height)

                        tracker.start_track(rgb, rect)

                        # add the tracker to our list of trackers so we can
                        # utilize it during skip frames
                        trackers.append(tracker)

                        # update our list of bounding box coordinates,
                        # confidences, and class IDs
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.6,0.3)

                        dsa.append((tracker, classID))
                        classIDs.append(idxs[0])
                        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 1)
                        cv2.putText(frame, str(LABELS[classID] + str(confidence)), (int(x) + 10, int(y) - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                        # cv2.circle(frame, (int((startX+endX)/2) - 10, int((startY+endY)/2 - 10)), 2, (0, 255, 0), -1)

                        rects.append((x, y, x + width, y + height))

                        if (LABELS[classID] == "car"):
                            car += 1
                        elif (LABELS[classID] == "truck"):
                            truck += 1
                        elif (LABELS[classID] == "person"):
                            person += 1
                        elif (LABELS[classID] == "bus"):
                            bus += 1
                        elif (LABELS[classID] == "bicycle"):
                            bicycle += 1
                        else:
                            motorbike += 1

            if maximumTotal[0] > (bicycle+car+truck+person+bus+motorbike):
                maximumTotal[0]=maximumTotal[0]
            else:
                maximumTotal[0] =bicycle+car+truck+person+bus+motorbike

            cv2.putText(frame, "TOTAL" + str(maximumTotal[0]), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255),2)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            totalFrames += 1

    print("[INFO] cleaning up...")

    vs.release()
    return maximumTotal[0]


lane1 = [20]
lane2 = [20]
lane3 = [20]
lane4 = [20]

for i in range(1):
    lane10 = [1]
    for i in lane10:

        a=count(r"lane1/{}.mp4".format(i))
        print(a)
        if a <= 10:
            signaltimer = 10
            print("this is signal timer for lane1 {}".format(signaltimer))
            lane1.clear()
            lane1.append(signaltimer)
        elif a <=20:
            signaltimer = 15
            print("this is signal timer for lane1 {}".format(signaltimer))
            lane1.clear()
            lane1.append(signaltimer)
        elif a <=30:
            signaltimer = 25
            print("this is signal timer for lane1 {}".format(signaltimer))
            lane1.clear()
            lane1.append(signaltimer)
        else:
            signaltimer = 30
            print("this is signal timer for lane1 {}".format(signaltimer))
            lane1.clear()
            lane1.append(signaltimer)

        waitingtime = lane2[0] + lane3[0] + lane4[0]
        print("this is waiting time for lane 1 {}".format(waitingtime))
        print(lane1)

    lane20 = [2]
    for i in lane20:

        a=count(r"lane2/{}.mp4".format(i))
        print(a)
        if a <= 10:
            signaltimer = 10
            print("this is signal timer for lane2 {}".format(signaltimer))
            lane2.clear()
            lane2.append(signaltimer)
        elif a <=20:
            signaltimer = 15
            print("this is signal timer for lane2 {}".format(signaltimer))
            lane2.clear()
            lane2.append(signaltimer)
        elif a <=30:
            signaltimer = 25
            print("this is signal timer for lane2 {}".format(signaltimer))
            lane2.clear()
            lane2.append(signaltimer)
        else:
            signaltimer = 30
            print("this is signal timerfor lane2 {}".format(signaltimer))
            lane2.clear()
            lane2.append(signaltimer)

            waitingtime = lane1[0] + lane3[0] + lane4[0]
        print("this is waiting time for lane 2 {}".format(waitingtime))
        print(lane2)

    lane30 = [3]
    for i in lane30:

        a=count(r"lane3/{}.mp4".format(i))
        print(a)
        if a <= 10:
            signaltimer = 10
            print("this is signal timer for lane3 {}".format(signaltimer))
            lane3.clear()
            lane3.append(signaltimer)
        elif a <=20:
            signaltimer = 15
            print("this is signal timer lane3 {}".format(signaltimer))
            lane3.clear()
            lane3.append(signaltimer)
        elif a <=30:
            signaltimer = 25
            print("this is signal timer lane3 {}".format(signaltimer))
            lane3.clear()
            lane3.append(signaltimer)
        else:
            signaltimer = 30
            print("this is signal timer lane3 {}".format(signaltimer))
            lane3.clear()
            lane3.append(signaltimer)

            waitingtime = lane2[0] + lane1[0] + lane4[0]
        print("this is waiting time for lane 3 {}".format(waitingtime))
        print(lane3)

    lane40 = [1]
    for i in lane40:

        a=count(r"lane4/{}.mp4".format(i))
        print(a)
        if a <= 10:
            signaltimer = 10
            print("this is signal timer for lane4 {}".format(signaltimer))
            lane4.clear()
            lane4.append(signaltimer)
        elif a <=20:
            signaltimer = 15
            print("this is signal timer for lane4 {}".format(signaltimer))
            lane4.clear()
            lane4.append(signaltimer)
        elif a <=30:
            signaltimer = 25
            print("this is signal timer for lane4 {}".format(signaltimer))
            lane4.clear()
            lane4.append(signaltimer)
        else:
            signaltimer = 30
            print("this is signal timer for lane4 {}".format(signaltimer))
            lane4.clear()
            lane4.append(signaltimer)

        waitingtime = lane2[0] + lane3[0] + lane1[0]
        print("this is waiting time for lane 4 {}".format(waitingtime))
        print(lane4)
