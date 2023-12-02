FROM ubuntu:latest
LABEL authors="data_day_life"

ENTRYPOINT ["top", "-b"]

FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]