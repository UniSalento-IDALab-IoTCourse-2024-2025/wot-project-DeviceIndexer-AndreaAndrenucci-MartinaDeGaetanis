FROM python:3.10.12

# ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY requirements.txt .
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

#CMD ["python", "./app.py"]