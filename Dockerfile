FROM python:3.10

RUN mkdir /bot
WORKDIR /bot

COPY . .

RUN pip install -r req.txt

CMD ["python", "main.py"]
