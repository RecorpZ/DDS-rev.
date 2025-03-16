# Практическая работа №2

## Проект: Разработка системы поиска не нормативных дефектов на автомобильных дорогах с твердым покрытием по видеоданным авторегистраторов

## Задача 1. Определить API Вашей DSS

Я выбрал Асинхронный (Event-based), по скольку для обработки больших видеозаписей в фоновом режиму будет предпочтительнее иметь асинхронный метод
Я использую фреймворк FastAPI для создания RESTful API, который будет обрабатывать запросы на загрузку видео и получение отчетов.

## Задача 2.
Ранее я планировал сделать систему из 4 сервисов, но после анализа пришел к выводу, что можно оставить 3.
## Сервисы:
**Сервис загрузки видео** - принимает видеофайлы и сохраняет их на сервере.

**Сервис анализа видео** - обрабатывает видеофайлы, выявляет повреждения и генерирует отчеты.

**Сервис отчетов** - предоставляет доступ к сгенерированным отчетам и хранит их в базе данных.

На данный момент взаимодейтсвие планируется через запросы на внутренние IP, я реализую сервисы в разных образах, и внутри одного контейнера они смогу делать запросу друг другу.

**Пример взаимодейтствия**

    Сервис загрузки видео:
        POST /upload - загрузка видеофайла.
        
    Сервис анализа видео:
        POST /analyze - анализ видеофайла.
        
    Сервис отчетов:
        GET /reports/{id} - получение отчета по идентификатору.


## Задача 3. Dockerfile и обновить docker-compose
переделаны Dockerfile под эти 3 сервиса. 
Docker-compose имеет измененую структуру под интеграцию с postgres, на данный момент это заготовка под переход.

```
version: '3.8'

services:
  video-upload-service:
    build:
      context: ./video-upload-service
      dockerfile: Dockerfile
    ports:
      - "5001:5000"
    volumes:
      - ./video-upload-service:/app
    environment:
      - ENV_VAR_NAME=value
    depends_on:
      - db

  video-analysis-service:
    build:
      context: ./video-analysis-service
      dockerfile: Dockerfile
    ports:
      - "5002:5000"
    volumes:
      - ./video-analysis-service:/app
    environment:
      - ENV_VAR_NAME=value
    depends_on:
      - db

  report-service:
    build:
      context: ./report-service
      dockerfile: Dockerfile
    ports:
      - "5003:5000"
    volumes:
      - ./report-service:/app
    environment:
      - ENV_VAR_NAME=value
    depends_on:
      - db
  db:
    image: postgres:13
    restart: always
    environment:
      POSTGRES_USER: github_secret_username
      POSTGRES_PASSWORD: github_secret_password
      POSTGRES_DB: road_damage_db
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

```

## Задача 4.
Выявлены тесты для каждого из сервисов, запускаются через обращение к образу при запуске контейнера.
Далее планирую перенести все тесты для запуска из контейнера.
