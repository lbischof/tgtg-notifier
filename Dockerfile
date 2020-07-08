FROM python:slim

WORKDIR /usr/src/app

RUN apt-get update \
 && apt-get install gcc -y \
 && apt-get clean

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./notifier.py" ]
