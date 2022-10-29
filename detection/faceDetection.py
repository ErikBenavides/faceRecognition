import numpy as np
import cv2

CONFIDENCE = 0.60
MARGIN = 100


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
            # print(height)
            # print(width)
            if cv2.waitKey(10) & 0xFF == ord("s"):
                print("Guardando imagen")
                cropped_image = frame[
                    yMin - int(MARGIN * 1.5) : yMin + height + MARGIN,
                    xMin - MARGIN : xMin + width + MARGIN,
                ]
                cv2.imwrite("./public/images/" + name + ".jpg", cropped_image)
                cap.release()
                cv2.destroyAllWindows()
