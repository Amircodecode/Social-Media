## Запуск

1. Установи Docker и Docker Compose
2. Клонируй репозиторий
3. Скопируй `.env.example` в `.env` и заполни своими значениями:
```bash
   cp .env.example .env
```
4. Подними базу данных:
```bash
   docker compose up -d db
```
5. Установи зависимости и примени миграции (нужен [uv](https://docs.astral.sh/uv/)):
```bash
   uv sync
   uv run alembic upgrade head
```
6. Подними остальной стек:
```bash
   docker compose up --build
```
7. Открой:
   - API-документация: http://localhost:8000/docs
   - MailHog (письма верификации): http://localhost:8025