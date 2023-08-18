# 📚 Sensor-server

顔認証と RFID による本の識別を使った無人図書貸出システムのための、Python で記述された推論用サーバーです。

## 実行の仕方

まず、`python`本体と Python 用の依存関係マネージャ`poetry`が導入済みなことを確認して下さい。

```bash
python --version # Python 3.11.3
poetry --version # Poetry (version 1.4.2)
```

次に、このリポジトリをクローンしましょう。

```bash
git clone https://github.com/nitic-pbl-p4/sensor-server.git
cd sensor-server
```


最後に、`poetry`でこのプロジェクト用の Python の仮想環境を作成して、その後必要な依存関係をインストールします。

```bash
poetry shell
poetry install
```

最後に、実行しましょう。

```bash
python sensor-server/main.py
```

---

### VSCode 向けの設定

Poetry が作成した仮想環境を VSCode の Python 拡張機能に認識させるために、以下の設定を追加して下さい。詳しく: https://zenn.dev/pesuchin/articles/4c128aeb60cb42204311

このコマンドで出力されるパスを、VSCode の`settings.json`に追加しましょう。

```bash
poetry config virtualenvs.path # /Users/ReoHakase/Library/Caches/pypoetry/virtualenvs
```

```json
{
  "python.venvPath": "/Users/ReoHakase/Library/Caches/pypoetry/virtualenvs"
}
```

## 訓練の方法

sensor-server/face/images以下に、`<任意の名前>.(png|jpg|jpeg)`の形式で配置して下さい。

```bash
.
├── sensor-server
│   └── face
│       ├── images
│       │    ├── aung.jpeg
│       │    ├── maririhakuta.jpg  
│       │    ├── reohakuta.jpg
│       │    └── yutoinoue.jpg
│       ├── feature  
│       ├── images_aligned
│       ├── __init__.py
│       └── main.py
├── poetry.lock
├── pyproject.toml
├── README.md
├── sensor-server
└── tests
   └── __init__.py
```

画像を配置したら、以下のコマンドでfaceディレクトリに移動する。
```bash
cd sensor-server/face
```
#### 手順１：顔画像の切り取り
以下のコマンドで、sensor-server/faceは以下のimagesディレクトリに保存されている画像から顔部分のみを切り取って、images_alignedに同じ名前で保存する。
```bash
python gen_aligned.py <任意の名前>.(png|jpg|jpeg)
```
また、上記のコマンドで画像名のみを引数として与えるものとする。

例）

```bash
python gen_aligned.py aung.jpeg
```

#### 手順2：切り取った顔画像から特徴を抽出する
以下のコマンドで、sensor-server/faceは以下のimages_alignedディレクトリに保存されている画像からから特徴量を抽出し、第２引数にはユーザのIDを指定する。

```bash
python gen_feature.py <任意の名前>.(png|jpg|jpeg)　ID
```

上記のようにすることで、sensor-server/face/feature配下に特徴量を保存したファイルが生成されまた、sensor-server/face/data配下のid.jsonにユーザー名とIDが紐づけられて保存される。

例）

```bash
python gen_feature.py aung.jpeg IMG_6B07A8732E02-1
```


## HTTP GET /

```json
{"book":{"7663cf25":"2023-08-08T13:00:28.181921"},"person":{"id":"reohakuta","seenAt":"2023-08-08T13:00:26.958482"},"signature":"dvYOdXIZp9bOSm7o0gaPUEWfP96S5zWyJi2ZzQxUjhRgp4KktJy2Xx/sUtRn3hMkRjn3kb2qVz3DI+ePsOrYerrVa9j45dGvsra0P2dxXtd9gc9ifK43dL8Ku96LUIeNFj7jcVsRJ4qfLtR+Z3QADCt0uFFl+bG6eQr7+dYnfzbJV9e6ia2t+IZwYJ/fZrwgMa9xRZq2mfTrzYXlUDKiTbKitN7uNxT2oklaR2sMdLB/vNHsMt06uf/JtJZQxA5Cs4N4gEcLFlMrhqeBHuQRvj/3VsnJUWvHqJauXureTWOMaPuEfXMl42D+5e8I2FeHxm5AnPnE96T+SpihOZX4cQ==","timestamp":"2023-08-08T13:00:35.371409+09:00"}
```