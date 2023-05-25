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

そして、顔認証用ライブラリ`face_recognition`のために、`dlib`をインストールしましょう。
詳しく (MacOS or Ubuntu): https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf
詳しく (他の環境): https://github.com/ageitgey/face_recognition#installation

最後に、`poetry`でこのプロジェクト用の Python の仮想環境を作成して、その後必要な依存関係をインストールします。

```bash
poetry shell
poetry install
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

## 訓練用の顔画像の置き方

プロジェクトルート以下に、`assets/<個人のId>/<任意の名前>.(png|jpg|jpeg)`の形式で配置して下さい。

```bash
.
├── assets
│  ├── aung
│  │  └── IMG_6B07A8732E02-1.jpeg
│  ├── maririhakuta
│  │  └── IMG_1314.jpg
│  ├── reohakuta
│  │  └── IMG_1311.jpg
│  └── yutoinoue
│     └── IMG_1317.jpg
├── poetry.lock
├── pyproject.toml
├── README.md
├── sensor-server
│  ├── __init__.py
│  └── main.py
└── tests
   └── __init__.py
```
