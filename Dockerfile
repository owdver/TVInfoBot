FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -U pip && pip3 install -U -r requirements.txt

COPY . .

CMD ["python3", "bot.py"]
