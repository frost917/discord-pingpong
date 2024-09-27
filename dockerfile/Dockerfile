FROM alpine/git AS clone

RUN git clone https://github.com/frost917/discord-pingpong.git /discord-pingpong

FROM python:3.11-alpine3.19 AS flask

ENV LISTEN_IP="0.0.0.0" \
    PORT="80" \
    DEBUG_MODE="False"

COPY --from=clone /discord-pingpong /apps

WORKDIR /apps/source

RUN python3 -m pip install -r requirements.txt

EXPOSE 80 443
CMD ["python", "./main.py"]