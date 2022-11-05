import cv2
from detection.simple_facerec import SimpleFacerec


def detectFace():
    # Encode faces from a folder
    sfr = SimpleFacerec()
    sfr.load_encoding_images("./public/images")

    # Load Camera
    cap = cv2.VideoCapture(0)
    print("leyendo")
    while True:
        ret, frame = cap.read()
        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            cv2.putText(
                frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2
            )
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

            if name == "Unknown":
                cv2.putText(
                    frame,
                    "No puedes pasar",
                    (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )
            else:
                cv2.putText(
                    frame,
                    "Puedes pasar",
                    (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

        center = (
            int(frame.shape[1] / 2),
            int(frame.shape[0] / 2),
        )

        p1 = (
            center[0] - 100,
            center[1] - 100,
        )

        p2 = (
            center[0] + 100,
            center[1] + 100,
        )
        cv2.rectangle(frame, p1, p2, (0, 255, 0), 2)

        cv2.putText(
            frame,
            "Trata de cercarte al marco para una mejor deteccion.",
            (30, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            2,
        )

        cv2.putText(
            frame,
            "Pulsa q para cerrar la ventana",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            2,
        )

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


# detectFace()
