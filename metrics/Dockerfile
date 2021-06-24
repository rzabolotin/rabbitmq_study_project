FROM python:3.9-slim
WORKDIR /app
RUN pip install loguru pika
COPY metrics.py  ./
CMD ["python", "metrics.py"]
