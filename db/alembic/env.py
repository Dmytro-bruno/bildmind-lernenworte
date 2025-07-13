import os
import sys
from logging.config import fileConfig

from alembic import context

# 🔽 Додаємо підтримку .env
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

load_dotenv()

# 🔽 Додаємо шлях до проєкту, щоб імпорти моделей працювали
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# 🔽 Імпортуємо всі моделі для Alembic
import openapi.db.models.daily_progress  # noqa: F401
import openapi.db.models.gpt_logs  # noqa: F401
import openapi.db.models.level_progress  # noqa: F401
import openapi.db.models.test_session  # noqa: F401
import openapi.db.models.token_blacklist  # noqa: F401
import openapi.db.models.user  # noqa: F401
import openapi.db.models.user_settings  # noqa: F401
import openapi.db.models.user_stats  # noqa: F401
import openapi.db.models.user_word  # noqa: F401
import openapi.db.models.word  # noqa: F401

# 🔽 Імпортуємо settings і метадані
from openapi.config.settings import Settings
from openapi.db.base import Base

# 🔧 Завантажуємо налаштування
settings = Settings()

# 🔧 Отримуємо URL для підключення до БД
database_url = settings.DATABASE_URL
print(">>> Alembic підключається до:", database_url)

# 🔧 Встановлюємо URL у конфіг
config = context.config
config.set_main_option("sqlalchemy.url", database_url)

# 🔧 Логування з alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 📦 SQLAlchemy metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
