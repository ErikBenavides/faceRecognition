import torch
import numpy as np
import cv2

import faceDetection

model = torch.hub.load(
    "ultralytics/yolov5",
    "custom",
    path="./model/train/exp/weights/last.pt",
)


def main():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        results = model(frame)
        faceDetection.getFaces(results, frame, "erik")
        framwWithRect = cv2.rectangle(
            np.squeeze(results.render()), (40, 40), (200, 200), (255, 0, 0), 2
        )
        cv2.imshow("YOLO", framwWithRect)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

# python detect.py --weights runs/train/exp/weights/best.pt --img 416 --conf 0.1 --source 0
