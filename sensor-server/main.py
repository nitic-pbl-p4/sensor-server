import face_recognition
import os
import cv2
import numpy as np
import time

# assets/[personId]/[imageId].(png|jpg)


# 顔識別器を訓練する
def train_face_recognizer(root_dir):
    known_face_encodings = []
    known_face_ids = []

    for person_id in os.listdir(root_dir):
        person_dir = os.path.join(root_dir, person_id)

        if os.path.isdir(person_dir):
            for image_name in os.listdir(person_dir):
                image_path = os.path.join(person_dir, image_name)
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)

                if len(face_encodings) > 0:
                    known_face_encodings.append(face_encodings[0])
                    known_face_ids.append(person_id)

    return known_face_encodings, known_face_ids


# 与えられた判断材料の顔写真から、顔識別器を訓練する
known_face_encodings, known_face_ids = train_face_recognizer("assets")

# FPS計算用の変数
fps = 0
frame_counter = 0
start_time = time.time()

# カメラからの映像を取得する
# カメラの設定を行います。0は通常、システムのデフォルトのカメラを指します。
cap = cv2.VideoCapture(0)

while True:
    # カメラからフレームを読み込みます。retはフレームが正しく読み込まれたかどうかを示すブール値で、
    # frameは読み込まれたフレーム（numpy配列）です。
    ret, frame = cap.read()
    if not ret:
        break

    # 顔を検出する
    # OpenCVはBGRで画像を読み込むので、face_recognitionが期待するRGB形式に変換します。
    # Refer: https://github.com/ageitgey/face_recognition/issues/1497#issuecomment-1529567951
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 顔の位置を検出します。
    face_locations = face_recognition.face_locations(rgb_frame)
    if len(face_locations) == 0:
        print("No faces were detected in the frame.")
    else:
        print(f"Detected {len(face_locations)} face(s) in the frame.")
        # Print face locations
        for top, right, bottom, left in face_locations:
            print(f"({top}, {right}, {bottom}, {left})")

    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(
        face_locations, face_encodings
    ):
        # 全ての既知の顔に対して、顔の距離を計算する
        # その際、判定の厳しさを、デフォルトより厳しい0.45に設定する
        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding, 0.45
        )
        distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        print(f"matches: {matches}")
        print(f"distances: {distances}")

        # 最も距離が近いものを選ぶ
        best_match_index = np.argmin(distances)
        best_match_distance = distances[best_match_index]
        if matches[best_match_index]:
            person_id = known_face_ids[best_match_index]
        else:
            person_id = "Unknown"

        # 顔の領域とそのIDを表示する
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(
            frame,
            f"{person_id} ({best_match_distance:.4f})",
            (left + 6, bottom - 6),
            cv2.FONT_HERSHEY_DUPLEX,
            1.0,
            (255, 255, 255),
            1,
        )

    # FPSと入力画像の解像度を計算して表示する
    frame_counter += 1
    elapsed_time = time.time() - start_time
    if elapsed_time >= 1:
        fps = frame_counter / elapsed_time
        frame_counter = 0
        start_time = time.time()
    cv2.putText(
        frame,
        f"FPS: {fps:.2f}, Source: {frame.shape[1]}x{frame.shape[0]}",
        (10, 30),
        cv2.FONT_HERSHEY_DUPLEX,
        1.0,
        (0, 255, 0),
        1,
    )

    # 最終的な画像を表示する
    cv2.imshow("Video", frame)

    # キーボードの'q'キーまたは'esc'キーを押すと終了する
    if cv2.waitKey(1) & 0xFF in [27, ord("q")]:
        break

# Webカメラへのアクセスを解放する
cap.release()
cv2.destroyAllWindows()
