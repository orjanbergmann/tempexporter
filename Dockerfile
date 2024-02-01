FROM python:3.7-slim
WORKDIR /opt/exporter.temp
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY temp.py .

ENTRYPOINT ["python3", "temp.py"]
