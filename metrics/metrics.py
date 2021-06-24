import json
import os

from loguru import logger
import pika

HOST = os.environ["RABBIT_HOST"]
COUNTER_OF_MESSAGES = 0
logger.add(r"logs/labels_log.txt", encoding="utf8")

collected_labels = {"y_true": {}, "y_pred": {}}


def calculate_rmse():
    """Анализирует собранные значения, реальные и предсказанные и вычисляет RMSE. Вводить ее в лог"""
    errors = ((collected_labels["y_true"][timestamp] - collected_labels["y_pred"][timestamp])**2
              for timestamp in collected_labels["y_pred"])
    mse = sum(errors)/len(collected_labels["y_pred"])
    rmse = mse ** 0.5
    logger.info(f"MSE {mse:02} RMSE: {rmse:02}")


def callback(channel, method, properties, body):
    """Обрабатывает сообщение от rabbitmq
    Собирает дщанные в collected_labels
    Каждые 20 сообщений вычисляет среднюю ошибку и выводит в лог"""

    timestamp, label = json.loads(body)

    collected_labels[method.routing_key][timestamp] = float(label)

    logger.info(f"Из очереди {method.routing_key} пришло значение {timestamp}: {label}")

    global COUNTER_OF_MESSAGES
    COUNTER_OF_MESSAGES += 1

    if COUNTER_OF_MESSAGES % 20 == 0:
        calculate_rmse()


def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))

    channel = connection.channel()
    channel.queue_declare("y_pred")
    channel.queue_declare("y_true")

    # on_message_callback показывает какую функцию вызвать при получении сообщения
    channel.basic_consume(queue="y_pred", on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue="y_true", on_message_callback=callback, auto_ack=True)

    print("...Ожидание сообщений, для выхода нажмите CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    while True:
        try:
            start_consuming()
        except:
            print("Не удалось отправить сообщение в очередь")
