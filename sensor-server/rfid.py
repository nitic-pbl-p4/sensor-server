import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from threading import Event
from typing import Dict
from logger import logging
from state import State, Book
import datetime


def rfid_worker(events: Dict[str, Event], state: State):
    reader = SimpleMFRC522()
    logging.info("RFIDタグの読み取り準備が完了しました。")
    while not events["stop"].is_set():
        # state.add_book(Book(id=f"{uuid.uuid4()}", readAt=datetime.datetime.now()))
        # ここで何かの処理を行う
        (status, TagType) = reader.READER.MFRC522_Request(reader.READER.PICC_REQIDL)
        if status != reader.READER.MI_OK:
            # logging.error(f"RFIDタグの読み取りに失敗しました。ステータス: {status}, タグタイプ: {TagType}")
            continue
        (status, read_possible_uid_bytes) = reader.READER.MFRC522_Anticoll()
        if status != reader.READER.MI_OK:
            # logging.error(f"RFIDタグの読み取りに失敗しました。ステータス: {status}, uid: {uid}")
            continue

        uid_length = 7 if len(read_possible_uid_bytes) >= 7 else 4
        uid_bytes = read_possible_uid_bytes[:uid_length]
        uid_hex_string = "".join(f"{byte:02x}" for byte in uid_bytes)

        state.add_book(Book(id=uid_hex_string, readAt=datetime.datetime.now()))
        logging.info(
            f"RFIDタグを読み取りました。 uid: {uid_hex_string} / {read_possible_uid_bytes}"
        )

    # 'stop'イベントを受け取ったらクリーンアップ処理を行う
    logging.info("RFIDスレッドを終了します")
    GPIO.cleanup()


if __name__ == "__main__":
    # スレッド間で共有できる状態オブジェクトを生成する
    state = State()
    events = {"stop": Event()}

    rfid_worker(events=events, state=state)
