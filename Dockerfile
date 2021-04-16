FROM ubuntu:latest

MAINTAINER fnndsc "dev@babymri.org"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get update \
  && apt-get install tesseract-ocr -y \
  tesseract-ocr-deu \
  tesseract-ocr-eng \
  python3 \
  #python-setuptools \
  python3-pip \
  && apt-get clean \
  && apt-get autoremove

RUN apt-get update \
   && apt-get install libgl1-mesa-glx -y \
   && apt-get clean \
   %% apt-get autoremove


# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
