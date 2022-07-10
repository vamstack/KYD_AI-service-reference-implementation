FROM debian:11
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    gunicorn3 \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /service
COPY requirements.txt /src/* /service/
RUN pip3 install -r requirements.txt