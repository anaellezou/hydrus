# Python image
FROM python:3.12.4

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 5000
CMD ["python", "app.py"]

