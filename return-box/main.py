from threading import Thread
from uart import set_message, send_message

if __name__ == "__main__":
    message = []

    set_message_thread = Thread(target=set_message, args=(message,))
    set_message_thread.daemon = True
    # send_message_thread = Thread(target=send_message, args=(message,))
    # send_message_thread.daemon = True

    set_message_thread.start()
    # send_message_thread.start()

    send_message(message=message)
    # send_message_thread.join()
