FROM python:3.11.2-slim

WORKDIR /bot

COPY requirements.txt /bot/

RUN apt update && apt install -y git

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /bot

# Set environment variables from build arguments
ARG USER_TOKEN
ARG SERVER_ID
ARG CHANNEL_ID
ARG WEBHOOK_URL

ENV USER_TOKEN=$USER_TOKEN
ENV SERVER_ID=$SERVER_ID
ENV CHANNEL_ID=$CHANNEL_ID
ENV WEBHOOK_URL=$WEBHOOK_URL

EXPOSE 5000

CMD python main.py