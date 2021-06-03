FROM python:3.8

RUN pip3 install -U xlrd==1.2.0 pytelegrambotapi bs4 flask && apt update && apt install sqlite3
ADD . /home/project/
WORKDIR /home/project/src

CMD [ "python", "server.py" ]
