FROM python:3.11-slim

WORKDIR /app

COPY requerimientos.txt .
RUN pip install --no-cache-dir -r requerimientos.txt

COPY app/ .

CMD ["python", "main.py"]
