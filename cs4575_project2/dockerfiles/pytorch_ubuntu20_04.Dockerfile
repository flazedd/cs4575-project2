FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install torch==2.6.0

WORKDIR /app
COPY train_model.py .
CMD ["python3", "train_model.py"]
