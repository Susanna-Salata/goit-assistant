FROM python:3.9.13-slim-buster

MAINTAINER Susanna Salata "susanna.kiev@gmail.com"

COPY ./goit-assistant /goit-assistant

WORKDIR /goit-assistant

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]
