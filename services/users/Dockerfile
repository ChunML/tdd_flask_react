FROM python:3.7.4-slim

RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh ./
RUN chmod +x ./entrypoint.sh

COPY . .

CMD ["./entrypoint.sh"]
