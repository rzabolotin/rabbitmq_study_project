FROM python:3.9
WORKDIR /app
RUN pip install numpy pika scikit-learn==0.23.2
COPY model.py model.pkl ./
CMD ["python", "model.py"]
