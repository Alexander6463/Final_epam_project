from python:3.8.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/Final_task

COPY ./requirements.txt /usr/src/req.txt
RUN pip install -r /usr/src/req.txt

COPY . /usr/src/Final_task

EXPOSE 8000
