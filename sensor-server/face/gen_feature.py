import os
import sys
import argparse
import numpy as np
import cv2
import json

def main():
    # 引数をパースする
    with open('data/id.json') as f:
        ids = json.load(f)
    parser = argparse.ArgumentParser("generate face feature dictionary from an face image")
    parser.add_argument("image", help="input face image file path (./face.jpg)")
    parser.add_argument("id", help="input face image file path (./face.jpg)")
    args = parser.parse_args()
    basename_without_ext = os.path.splitext(args.image)[0]
    ids[basename_without_ext] = args.id
    with open('data/id.json', 'w') as f:
        json.dump(ids, f, indent=4)
    # 引数から画像ファイルのパスを取得
    path = args.image
    directory = os.path.dirname(args.image)
    if not directory:
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, args.image)

    # 画像を開く
    image = cv2.imread("images_aligned/{}".format(args.image))
    if image is None:
        exit()

    # 画像が3チャンネル以外の場合は3チャンネルに変換する
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    if channels == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    # モデルを読み込む
    weights = os.path.join(directory, "face_recognition_sface_2021dec.onnx")
    face_recognizer = cv2.FaceRecognizerSF_create(weights, "")

    # 特徴を抽出する
    face_feature = face_recognizer.feature(image)
    print(face_feature)
    print(type(face_feature))

    # 特徴を保存する
    basename = os.path.splitext(os.path.basename(args.image))[0]
    dictionary = os.path.join(directory, "feature")
    print(basename)
    np.save("{}/{}".format(dictionary, basename), face_feature)

if __name__ == '__main__':
    main()