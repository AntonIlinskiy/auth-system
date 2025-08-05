import os
import sys
from logging.config import fileConfig

# ✅ Добавляем корень проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alembic import context
from sqlalchemy import engine_from_config, pool
from app.database import Base
from app import models  # важно импортировать все модели до миграции
from app.config import settings

# ✅ Настраиваем alembic config
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# ✅ Логгирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Метаданные моделей
target_metadata = Base.metadata

print("✅ ENV LOADED:", settings.DATABASE_URL)
