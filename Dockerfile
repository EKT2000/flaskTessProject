FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7


MAINTAINER fnndsc "elias@kadiri.de"


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
   && apt-get autoremove


# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./app /app
