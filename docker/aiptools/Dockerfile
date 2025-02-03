FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt install build-essential -y

RUN apt-get update && apt-get install -y git

COPY app.py /app
COPY credentails.py /app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask

EXPOSE 5000

CMD ["python", "app.py"]
