# import serial
import time
import requests
import serial
from logger import logging
from dotenv import load_dotenv

import os


def set_message(message):
    ser = serial.Serial(port="/dev/serial0", baudrate=9600, timeout=1)

    logging.info("UART通信の準備が完了しました")

    while True:
        if ser.in_waiting:
            logging.info("UART通信からデータを受信しました")
            read_text = ser.readline().decode().strip()
            rfid_tag = read_text
            logging.info(f"RFIDタグを受信しました。: {rfid_tag}")
            message.append(rfid_tag)
            ser.write(b"1")
            logging.info('テキスト "1" をUARTで送信しました。')

    ser.close()


def send_message(message):
    load_dotenv("/home/pi/repos/sensor-server/return-box/token.env")
    line_notify_token = os.getenv("LINE_TOKEN")

    logging.info(f"LINE Token: {line_notify_token}")
    while True:
        if message:
            result_data = "\n".join(message)
            line_notify_api = "https://notify-api.line.me/api/notify"
            headers = {"Authorization": f"Bearer {line_notify_token}"}
            data = {"message": f"\n以下の本が返却されました\n {result_data}"}
            logging.info(f"LINEで以下のメッセージを通知します: {data}")
            requests.post(line_notify_api, headers=headers, data=data)
            message = []
        else:
            logging.info("未通知の返却された本がないため、通知を行いません")
        time.sleep(10)  # 通知の送信間隔
