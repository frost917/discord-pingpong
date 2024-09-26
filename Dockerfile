FROM alpine/git AS clone

RUN git clone https://github.com/frost917/discord-pingpong.git

FROM python:3.12.6alpine3.19 AS flask

COPY --from=clone /discord-pingpong /apps

EXPOSE 80 443
CMD ["python", "/apps/source/main.py"]