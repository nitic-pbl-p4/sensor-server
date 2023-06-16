from threading import Thread, Event
import time
from typing import Dict
from logger import *
from state import State, Person, Book
import datetime
import uuid
import cv2


def worker_sample1(events: Dict[str, Event], state: State):
    while not events["stop"].is_set():
        logging.info("状態を変更します")
        state.person = Person(id="Reo", timestamp=datetime.datetime.now())
        state.add_book(Book(id=f"{uuid.uuid4()}", timestamp=datetime.datetime.now()))
        # ここで何かの処理を行う
        time.sleep(1)

    # 'stop'イベントを受け取ったらクリーンアップ処理を行う
    logging.info("sample1スレッドを終了します")


def worker_sample2(events: Dict[str, Event], state: State):
    while not events["stop"].is_set():
        logging.info("状態を出力します")
        console.log(f"state: {highlighter(repr(state))}")
        # ここで何かの処理を行う
        time.sleep(1)

    # 'stop'イベントを受け取ったらクリーンアップ処理を行う
    logging.info("sample2スレッドを終了します")


if __name__ == "__main__":
    # スレッド間で共有できる状態オブジェクトを生成する
    state = State()
    events = {"stop": Event()}

    # スレッドを生成する
    t1 = Thread(target=worker_sample1, args=(events, state))
    t2 = Thread(target=worker_sample2, args=(events, state))

    # スレッドを開始する
    t1.start()
    t2.start()

    # 5秒間まつ
    time.sleep(5)
    logging.info("5秒経過しました")

    # 'stop'イベントを送信
    events["stop"].set()
    # スレッドが終了するまで待つ join
    t1.join()
    logging.info("t1が終了しました")
    t2.join()
    logging.info("t2が終了しました")
