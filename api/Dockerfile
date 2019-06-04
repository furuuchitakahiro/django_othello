FROM python:3.7.2
ENV PYTHONUNBUFFERED 1

# MySQL を直接操作したいときに api コンテナから操作するためにインストール
RUN apt-get update && apt-get install -y mysql-client

RUN mkdir -p /usr/src/app
ENV HOME=/usr/src/app
WORKDIR $HOME

ADD requirements.txt $HOME
RUN pip install -r requirements.txt
ADD . $HOME
