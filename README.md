# API для Yatube

## Описание проекта

REST API социальной платформы Yatube. Проект позволяет получать публикации и сообщества, создавать и редактировать собственные посты и комментарии, а также подписываться на других пользователей.

## Установка

```bash
git clone https://github.com/frion13/api-final-yatube-new.git
cd api-final-yatube-new
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd yatube_api
python manage.py migrate
python manage.py runserver
```

Документация API доступна по адресу `http://127.0.0.1:8000/redoc/`.

## Аутентификация

Получите JWT-токены запросом `POST /api/v1/jwt/create/` с полями `username` и `password`, затем передавайте access-токен в заголовке:

```text
Authorization: Bearer <access-token>
```

## Примеры запросов

```bash
curl http://127.0.0.1:8000/api/v1/posts/
curl -X POST http://127.0.0.1:8000/api/v1/posts/ \
  -H 'Authorization: Bearer <access-token>' \
  -H 'Content-Type: application/json' \
  -d '{"text": "Мой первый пост"}'
curl -X POST http://127.0.0.1:8000/api/v1/follow/ \
  -H 'Authorization: Bearer <access-token>' \
  -H 'Content-Type: application/json' \
  -d '{"following": "username"}'
```

## Автор

[frion13](https://github.com/frion13)
