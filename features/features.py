import json
import os
import random
import time

import pika
from sklearn.datasets import load_diabetes

HOST = os.environ["RABBIT_HOST"]


def get_random_data():
    X, y = load_diabetes(return_X_y=True)
    random_idx = random.randint(0, X.shape[0] - 1)
    timestamp = time.time_ns()
    messages = (X[random_idx].tolist(), y[random_idx])
    return ((timestamp, message) for message in messages)


def send_message_to_channel(channel, queue_name, data):

    # Создадим очередь, с которой будем работать:
    channel.queue_declare(queue=queue_name)

    # Опубликуем сообщение
    # exchange определяет, в какую очередь отправляется сообщение. Если мы используем дефолтную точку обмена, то значение можно оставить пустым.
    # параметр routing_key указывает имя очереди,
    # параметр body тело самого сообщения,
    channel.basic_publish(exchange="", routing_key=queue_name, body=json.dumps(data))


def sent_messages_to_rabbit():

    x, y = get_random_data()

    # Подключение к серверу на хосте:
    connection = pika.BlockingConnection(pika.ConnectionParameters(HOST))
    channel = connection.channel()

    send_message_to_channel(channel, "y_true", y)
    print("Сообщение с правильным ответом, отправлено в очередь")

    send_message_to_channel(channel, "features", x)
    print("Сообщение с данными отправлено в очередь")

    # Закроем подключение
    connection.close()


if __name__ == "__main__":
    while True:
        try:
            sent_messages_to_rabbit()
            time.sleep(3)
        except:
            print("Не удалось отправить сообщение в очередь")
