from flask import Flask


import json
import rsa
import hashlib
import pendulum

app = Flask(__name__)

pub_key_path = "pub_key.pem"
private_key_path = "private_key.pem"

with open(pub_key_path, mode='rb') as f:
    pub_str = f.read()
    pub_key = rsa.PublicKey.load_pkcs1(pub_str)
 
with open(private_key_path, mode='rb') as f:
    private_str = f.read()
    private_key = rsa.PrivateKey.load_pkcs1(private_str)

@app.route('/')
def hello():
    # ここで顔認証とRFIDのデータを取得する処理を実装する
    face_data = get_face_data()
    rfid_data = get_rfid_data()
    # データを辞書形式で返す
    data = {
        "person": {
            "id": face_data,
            "timestamp": pendulum.now().isoformat()
        },
        "book": rfid_data,
    }
    
    # JSONデータを文字列に変換する
    json_str = json.dumps(data, sort_keys=True)
    
    # データのハッシュ値を計算する
    hash = hashlib.sha256(json_str.encode()).digest()
    
    # 秘密鍵でハッシュ値を署名する
    signature = rsa.sign(hash, private_key, 'SHA-256')
    
    # 署名をBase64形式の文字列に変換する
    import base64
    signature_str = base64.b64encode(signature).decode()

    # 署名をJSONデータに追加する
    data['signature'] = signature_str

    # 署名付きのJSONデータを表示する
    print(json.dumps(data, indent=4))

    return data



def get_face_data():
    # 顔認証データを取得する処理を実装する
    return "a"
    
def get_rfid_data():
    # RFIDデータを取得する処理を実装する
    return "a"
    
if __name__ == '__main__':
    app.run()
