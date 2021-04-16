FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev \
    apt-get install tesseract-ocr \
    apt-get installl tesseract-ocr-deu \
    apt-get installl tesseract-ocr-eng \
    apt-get installl tesseract-ocr-ocd \
    apt-get install imagemagick

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
