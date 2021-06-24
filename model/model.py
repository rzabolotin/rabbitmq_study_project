import json
import os
import pickle

import numpy as np
import pika

HOST = os.environ["RABBIT_HOST"]
model = None


def load_model():
    global model

    if model:
        return model

    model_file = "model.pkl"
    with open(model_file, "rb") as f:
        model = pickle.load(f)

    return model


def make_prediction(data):
    model = load_model()
    timestamp, row = json.loads(data)
    row = np.array(row).reshape(1, -1)
    return timestamp, model.predict(row)[0]


def new_features_callback(channel, method, properties, body):
    print(f"Получен вектор {body}")

    message = make_prediction(body)

    channel.queue_declare(queue="y_pred")
    channel.basic_publish(exchange="", routing_key="y_pred", body=json.dumps(message))


def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))

    channel = connection.channel()
    channel.queue_declare("features")
    # on_message_callback показывает какую функцию вызвать при получении сообщения
    channel.basic_consume(
        queue="features", on_message_callback=new_features_callback, auto_ack=True
    )

    print("...Ожидание сообщений, для выхода нажмите CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    while True:
        try:
            start_consuming()
        except:
            print("Не удалось отправить сообщение в очередь")
