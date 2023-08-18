import os
import argparse
import numpy as np
import cv2

def main():
    # 引数をパースする
    parser = argparse.ArgumentParser("generate aligned face images from an image")
    parser.add_argument("image", help="input image file path (./image.jpg)")
    args = parser.parse_args()

    # 引数から画像ファイルのパスを取得
    path = "images/{}".format(args.image)
    
    # 画像を開く
    image = cv2.imread(path)
    if image is None:
        exit()

    gamma22LUT = np.array([pow(x/255.0 , 2.2) for x in range(256)],
                         dtype='float32')
    image = cv2.LUT(image, gamma22LUT)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = pow(image, 1.0/2.2) * 255

    # 画像が3チャンネル以外の場合は3チャンネルに変換する
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    if channels == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    # モデルを読み込む
    face_detector = cv2.FaceDetectorYN_create("face_detection_yunet_2023mar.onnx", "", (0, 0))
    face_recognizer = cv2.FaceRecognizerSF_create("face_recognition_sface_2021dec.onnx", "")

    # 入力サイズを指定する
    height, width, _ = image.shape
    face_detector.setInputSize((width, height))

    # 顔を検出する
    _, faces = face_detector.detect(image)
    # 検出された顔を切り抜く
    if type(faces) != type(None):
        aligned_face = face_recognizer.alignCrop(image, faces[0])
    else:
        aligned_face = image
    # 画像を表示、保存する
    cv2.imwrite("images_aligned/{}".format(args.image),aligned_face)

if __name__ == '__main__':
    main()