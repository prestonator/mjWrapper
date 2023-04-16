FROM python:3.11.2-slim

WORKDIR /bot

COPY requirements.txt /bot/

RUN apt update && apt install -y git

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /bot

# Set environment variables from build arguments
ARG STRAPI_API_TOKEN
ARG STRAPI_API_UPLOAD_URL
ARG USER_TOKEN
ARG SERVER_ID
ARG CHANNEL_ID
ARG PROXY


ENV STRAPI_API_TOKEN=$STRAPI_API_TOKEN
ENV STRAPI_API_UPLOAD_URL=$STRAPI_API_UPLOAD_URL
ENV USER_TOKEN=$USER_TOKEN
ENV SERVER_ID=$SERVER_ID
ENV CHANNEL_ID=$CHANNEL_ID
ENV PROXY=$PROXY


EXPOSE 5000

CMD python example.py