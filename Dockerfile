# Use the Confluent Kafka image
FROM confluentinc/cp-kafka:latest

FROM ubuntu:latest
LABEL authors="data_day_life"

ENTRYPOINT ["top", "-b"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

FROM python:3.11
WORKDIR /discord_bot_app
COPY src/ .

# Setup docker python venv from local venv definition
#RUN python -m venv /opt/venv
#ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]