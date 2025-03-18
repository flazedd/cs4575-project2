FROM python:3.11.11-bookworm

WORKDIR /app

COPY volume.py ./

CMD ["sh", "-c", "python volume.py"]