from threading import Thread, Event
from logger import logging
from state import State
from face import face_recognition_worker
from worker import worker_sample2

if __name__ == "__main__":
    # スレッド間で共有できる状態オブジェクトを生成する
    state = State()
    events = {"stop": Event()}

    # サブスレッドを生成する
    worker_sample2_thread = Thread(target=worker_sample2, args=(events, state))
    worker_sample2_thread.daemon = True  # メインスレッドが終了したら、このスレッドも終了するようデーモン化する

    # サブスレッドを開始する
    worker_sample2_thread.start()

    # 顔認識スレッドはメインスレッドで実行する
    # GUIアプリケーションの場合は、メインスレッドで実行する必要がある
    face_recognition_worker(events, state)

    logging.info("終了シグナルを送信します")
    events["stop"].set()
    worker_sample2_thread.join()
    logging.info("worker_sample2スレッドが終了しました")
