FROM ubuntu

WORKDIR /usr/src/app

COPY requirements.txt .

RUN apt-get update && apt-get upgrade && apt-get install -y pip && pip install --no-cache-dir -r requirements.txt

COPY /app .