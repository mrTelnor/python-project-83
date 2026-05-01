### Анализатор страниц

[![Hexlet tests](https://github.com/mrTelnor/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/mrTelnor/python-project-83/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mrTelnor_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mrTelnor_python-project-83)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=mrTelnor_python-project-83&metric=coverage)](https://sonarcloud.io/summary/new_code?id=mrTelnor_python-project-83)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=mrTelnor_python-project-83&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=mrTelnor_python-project-83)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=mrTelnor_python-project-83&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=mrTelnor_python-project-83)

Веб-приложение для базового SEO-анализа сайтов: добавляешь URL, запускаешь проверку — приложение делает HTTP-запрос, извлекает код ответа, `<h1>`, `<title>` и `<meta name="description">`, и сохраняет результаты в БД. История проверок видна на странице каждого сайта.

### Demo

https://python-project-83-vbzz.onrender.com

### Стек

Python 3.12, Flask, Jinja2, PostgreSQL, HTML, Bootstrap 5, gunicorn, uv.

### Локальный запуск

```bash
git clone https://github.com/mrTelnor/python-project-83.git
cd python-project-83
cp .env.example .env
# в .env: задать SECRET_KEY (любая случайная строка) и DATABASE_URL
make install
psql -d "$DATABASE_URL" -f database.sql   # одноразовая миграция
make dev
```

Откроется на `http://127.0.0.1:5000`.

### Тесты и линтер

```bash
make lint   # ruff
make test   # pytest + coverage
```
