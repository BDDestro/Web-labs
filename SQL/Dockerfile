FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir Flask

EXPOSE 6001

CMD ["python", "app.py"]
