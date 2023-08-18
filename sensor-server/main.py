from threading import Thread, Event
from logger import logging
from state import State
from face.recognize import *
from server import server_worker
from rfid import rfid_worker

if __name__ == "__main__":
    # スレッド間で共有できる状態オブジェクトを生成する
    state = State()
    events = {"stop": Event()}

    # サブスレッドを生成する
    server_worker_thread = Thread(target=server_worker, args=(events, state))
    server_worker_thread.daemon = True  # メインスレッドが終了したら、このスレッドも終了するようデーモン化する
    rfid_worker_thread = Thread(target=rfid_worker, args=(events, state))
    rfid_worker_thread.daemon = True  # メインスレッドが終了したら、このスレッドも終了するようデーモン化する

    # サブスレッドを開始する
    server_worker_thread.start()
    rfid_worker_thread.start()

    # while True:
    #     sleep(1000)

    # 顔認識スレッドはメインスレッドで実行する
    # GUIアプリケーションの場合は、メインスレッドで実行する必要がある
    recognizer(events, state)

    logging.info("終了シグナルを送信します")
    events["stop"].set()
    # TODO: Flaskサーバーのスレッドがstopイベントを受け取るようにする
    server_worker_thread.join()
    logging.info("Flaskサーバースレッドが終了しました")
