FROM debian:11
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    gunicorn3 \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /service
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r requirements.txt
COPY /src/* /service/