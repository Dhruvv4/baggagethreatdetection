FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt /app

RUN apt-get update \
    && apt-get install -y libglib2.0-0 libgl1-mesa-glx libsm6 libxext6 libxrender-dev libcurl4-openssl-dev libssl-dev gcc\
    && apt-get clean
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app