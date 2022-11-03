import torch
import numpy as np
import cv2

CONFIDENCE = 0.60
MARGIN = 100

model = torch.hub.load(
    "ultralytics/yolov5",
    "custom",
    path="./model/train/exp/weights/last.pt",
)


def runFaceDetection(name):
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        results = model(frame)
        getFaces(results, frame, name, cap)

        frameWithFaces = results.render()

        center = (
            int(frameWithFaces[0].shape[1] / 2),
            int(frameWithFaces[0].shape[0] / 2),
        )

        p1 = (
            center[0] - 100,
            center[1] - 100,
        )

        p2 = (
            center[0] + 100,
            center[1] + 100,
        )

        frameWithRect = cv2.rectangle(
            np.squeeze(frameWithFaces), p1, p2, (0, 255, 0), 2
        )

        frameWithText = cv2.putText(
            frameWithRect,
            "Trata de cercarte al marco y pulsa S para tomar foto.",
            (30, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            2,
        )

        frameWithText = cv2.putText(
            frameWithRect,
            "La ventana se cerrara automaticamente",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            2,
        )

        cv2.imshow("YOLO", frameWithText)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


def getFaces(results, frame, name, cap):
    faces = []
    for i, dets in enumerate(results.xyxy[0]):
        if dets[4] > CONFIDENCE and dets[5] == 0:
            xMin = int(dets[0].numpy())
            yMin = int(dets[1].numpy())
            xMax = int(dets[2].numpy())
            yMax = int(dets[3].numpy())

            height = yMax - yMin
            width = xMax - xMin

            if cv2.waitKey(10) & 0xFF == ord("s"):
                print("Guardando imagen")
                cropped_image = frame[
                    yMin - int(MARGIN * 1.5) : yMin + height + MARGIN,
                    xMin - MARGIN : xMin + width + MARGIN,
                ]
                cv2.imwrite("./public/images/" + name + ".jpg", cropped_image)
                cap.release()
                cv2.destroyAllWindows()


if __name__ == "__main__":
    runFaceDetection()

# python detect.py --weights runs/train/exp/weights/best.pt --img 416 --conf 0.1 --source 0
