﻿FROM alpine/git AS clone

RUN git clone https://github.com/frost917/discord-pingpong.git /discord-pingpong

FROM python:3.11-alpine3.19 AS flask

COPY --from=clone /discord-pingpong /apps

WORKDIR /apps/source

RUN python3 -m pip install -r requirements.txt

EXPOSE 80 443
CMD ["python", "./main.py"]