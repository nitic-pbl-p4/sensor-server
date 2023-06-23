import face_recognition
import os
import cv2
import numpy as np
import time
from logger import logging, track, highlighter
import pickle

# assets/[personId]/[imageId].(png|jpg)


# 顔識別器を訓練する
def train_face_recognizer(asset_dir="assets", cache_dir="cache"):
    cache_file_path = os.path.join(cache_dir, "face_recognizer.pkl")

    logging.info("顔識別器の学習を開始します")

    known_face_encodings = []
    known_face_ids = []

    for person_id in track(
        os.listdir(asset_dir), description=f"全顔画像ディレクトリ {asset_dir} を読み込み中..."
    ):
        person_dir = os.path.join(asset_dir, person_id)

        if os.path.isdir(person_dir):
            for image_name in os.listdir(person_dir):
                image_path = os.path.join(person_dir, image_name)
                logging.debug(f"画像 {image_path} を読み込み中...")
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)

                if len(face_encodings) > 0:
                    known_face_encodings.append(face_encodings[0])
                    known_face_ids.append(person_id)

    logging.info("顔識別器の学習が完了しました")

    # キャッシュするPythonオブジェクトを辞書にまとめる
    logging.info(f"学習した顔識別器をキャッシュファイル {cache_file_path} に保存します")
    cache_data = {
        "known_face_encodings": known_face_encodings,
        "known_face_ids": known_face_ids,
    }
    with open(cache_file_path, "wb") as f:
        pickle.dump(cache_data, f)
    return known_face_encodings, known_face_ids


# 顔識別器を読み込む
def load_face_recognizer(cache_dir="cache"):
    cache_file_path = os.path.join(cache_dir, "face_recognizer.pkl")

    logging.info(f"キャッシュファイル {cache_file_path} から顔識別器を読み込みます")
    # もしキャッシュファイルが存在しない場合は、学習する
    if not os.path.exists(cache_file_path):
        logging.info("キャッシュファイルが存在しないため、顔識別器を学習します")
        return train_face_recognizer()

    with open(cache_file_path, "rb") as f:
        cache_data = pickle.load(f)
    return cache_data["known_face_encodings"], cache_data["known_face_ids"]


# 与えられた判断材料の顔写真から、顔識別器を訓練する
known_face_encodings, known_face_ids = load_face_recognizer()

# 推論高速化のための定数
resize_factor = 0.25  # フレームをリサイズする際にかける係数
reverse_resize_factor = int(1 / resize_factor)

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

    # 処理の高速化のために、フレームをリサイズする
    resized_frame = cv2.resize(frame, (0, 0), fx=resize_factor, fy=resize_factor)

    # 顔を検出する
    # OpenCVはBGRで画像を読み込むので、face_recognitionが期待するRGB形式に変換します。
    # Refer: https://github.com/ageitgey/face_recognition/issues/1497#issuecomment-1529567951
    rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    # 顔の位置を検出します。
    face_locations = face_recognition.face_locations(rgb_frame)
    if len(face_locations) == 0:
        logging.info("フレーム内に顔が検出されませんでした")
    else:
        logging.info(f"{len(face_locations)} 個の顔をフレーム内に検出しました")
        # Print face locations
        # for top, right, bottom, left in face_locations:
        # print(f"({top}, {right}, {bottom}, {left})")

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

        logging.debug(f"合致結果: {highlighter(repr(matches))}", extra={"markup": True})
        logging.debug(
            f"参考画像との距離: {highlighter(repr(distances))}", extra={"markup": True}
        )

        # 最も距離が近いものを選ぶ
        best_match_index = np.argmin(distances)
        best_match_distance = distances[best_match_index]
        if matches[best_match_index]:
            person_id = known_face_ids[best_match_index]
        else:
            person_id = "Unknown"

        # 顔の領域とそのIDを表示する
        cv2.rectangle(
            frame,
            (left * reverse_resize_factor, top * reverse_resize_factor),
            (right * reverse_resize_factor, bottom * reverse_resize_factor),
            (0, 255, 0),
            2,
        )
        cv2.putText(
            frame,
            f"{person_id} ({best_match_distance:.4f})",
            (left * reverse_resize_factor + 6, bottom * reverse_resize_factor - 6),
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
        f"fps: {fps:.2f}, src: {frame.shape[1]}x{frame.shape[0]}, resize: x{resize_factor}",
        (10, 30),
        cv2.FONT_HERSHEY_DUPLEX,
        0.75,
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
