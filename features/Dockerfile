FROM python:3.9
WORKDIR /app
RUN pip install numpy pika sklearn
COPY features.py .
CMD ["python", "features.py"]
