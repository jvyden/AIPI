FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get -y install wget
RUN mkdir -p /app/ai/eva_model
RUN wget https://huggingface.co/Thouph/eva02-vit-large-448-8046/resolve/main/model.pth?download=true -O /app/ai/eva_model/model.pth
RUN wget https://huggingface.co/Thouph/eva02-vit-large-448-8046/resolve/main/tags_8041.json?download=true -O /app/ai/eva_model/tags_8041.json
RUN apt-get -y purge wget && apt-get -y autoremove
RUN apt-get clean

ENV PYTHONDONTWRITEBYTECODE=1

COPY ./pytorch-requirements.txt /app
RUN pip install -r /app/pytorch-requirements.txt --no-cache-dir
COPY ./requirements.txt /app
RUN pip install -r /app/requirements.txt --no-cache-dir

RUN rm -fv /app/requirements.txt /app/pytorch-requirements.txt

COPY ./src/ /app/

ENTRYPOINT ["python", "/app/main.py"]
