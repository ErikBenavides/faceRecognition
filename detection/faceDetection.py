import torch
import numpy as np
import cv2

CONFIDENCE = 0.60

model = torch.hub.load(
    "ultralytics/yolov5",
    "custom",
    path="./model/train/exp/weights/last.pt",
)


def getFaces(frame):

    # Make detections
    results = model(frame)

    faces = []
    for i, dets in enumerate(results.xyxy[0]):
        print(
            "persona "
            + str(i)
            + " confianza: "
            + str(dets[4])
            + " clase: "
            + str(dets[5])
        )
        if dets[4] > CONFIDENCE and dets[5] == 0:
            xMin = int(dets[0].numpy())
            yMin = int(dets[1].numpy())
            xMax = int(dets[2].numpy())
            yMax = int(dets[3].numpy())

            height = yMax - yMin
            width = xMax - xMin
            # print(height)
            # print(width)
            cropped_image = frame[yMin : yMin + height, xMin : xMin + width]
            cv2.imwrite("./contour" + str(i) + ".png", cropped_image)

            faces.append((xMin, yMin, xMax, yMax))
    print(faces)


# python detect.py --weights runs/train/exp/weights/best.pt --img 416 --conf 0.1 --source 0
