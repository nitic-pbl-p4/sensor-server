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
            try:
                # ステータスコードが200の場合は何もしない
                response = requests.get(
                    f"https://shelfree-web.vercel.app/api/book/{rfid_tag}/status",
                    timeout=10,
                )
                if response.status_code == 200:
                    logging.info("status code is 200. Do something here.")
                # ステータスコードが404の場合は返却の処理を行う
                elif response.status_code == 404:
                    logging.info("Status code is 404. Do something here")

                    message.append(rfid_tag)
                    ser.write(b"1")
                    logging.info('テキスト "1" をUARTで送信しました。')
                # それ以外のステータスコードの場合の処理
                else:
                    logging.info(
                        f"Recieved unexpected status code: {response.status_code}"
                    )
            except requests.Timeout:
                logging.info("request timed out.")
            except requests.RequestException as e:
                logging.info(f"An rttot occurred: {e}")
    ser.close()


def send_message(message):
    load_dotenv("/home/pi/repos/sensor-server/return-box/token.env")
    line_notify_token = os.getenv("LINE_TOKEN")

    logging.info(f"LINE Token: {line_notify_token}")
    while True:
        if message:
            result_data = "\n".join(
                [
                    f"{result}\nhttps://shelfree-web.vercel.app/book/{result}"
                    for result in message
                ]
            )
            line_notify_api = "https://notify-api.line.me/api/notify"
            headers = {"Authorization": f"Bearer {line_notify_token}"}
            data = {"message": f"\n以下の本が返却ボックスに届きました：\n{result_data}"}
            logging.info(f"LINEで以下のメッセージを通知します: {data}")
            requests.post(line_notify_api, headers=headers, data=data)
            message = []
        else:
            logging.info("未通知の返却された本がないため、通知を行いません")
            # message.append("123456ab")
        time.sleep(10)  # 通知の送信間隔
