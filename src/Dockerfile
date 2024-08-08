FROM python:3.9-slim

RUN mkdir -p /usr/src/app/

# Установите рабочую директорию в /usr/src/app/
WORKDIR /usr/src/app/

# Установка необходимых пакетов для MySQL
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Сделайте порт 8080 доступным снаружи контейнера
EXPOSE 8080

# Переменная окружения для установки нудного часового пояса
ENV TZ=Europe/Minsk

# CMD ["python", "app_booklist.py"]
ENTRYPOINT ["python", "app_booklist.py"]