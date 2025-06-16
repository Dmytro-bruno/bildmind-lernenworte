Generic single-database configuration.

## Alembic Configuration

This repository does **not** include a real `alembic.ini` with database passwords for security reasons.

- Use the provided `alembic.ini.example` as a template.
- Copy it to `alembic.ini` in the project root.
- Enter your own database connection credentials in the `sqlalchemy.url` line.

**Never commit your personal `alembic.ini` with secrets to any public repository.**

# Alembic
Для запуску міграцій скопіюйте alembic.ini.example у alembic.ini та вкажіть свої дані підключення.

# Запуск Alembic Upgrade / Умова: знаходитись у корені проєкту
- $env:PYTHONPATH = "."
- alembic -c openapi/alembic.ini upgrade head

# Важливі пояснення:
PYTHONPATH=.	Щоб openapi. був імпортований як пакет
-c openapi/alembic.ini	Вказує Alembic, де шукати script_location
upgrade head	Застосовує найсвіжішу міграцію

# Якщо потрібно створити нову міграцію:
alembic -c openapi/alembic.ini revision --autogenerate -m "short message"

# Перевірити чи alembic бачить БД та чи міграції застосовані:
alembic current

Очікувано — ти побачиш щось на кшталт:
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
<revision_id> (head)
# Якщо потрібно ВИПРАВИТИ тільки-но створену (невдалу) міграцію:
Відкрий відповідний міграційний файл у openapi/db/alembic/versions/ і внеси зміни (наприклад, додай server_default='0').

Відкоти цю міграцію:

alembic downgrade <revision_id_попередньої_міграції>
або, якщо це остання міграція:

alembic downgrade -1
Потім знову застосуй:

alembic upgrade head
