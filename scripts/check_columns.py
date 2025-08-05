from sqlalchemy import create_engine, inspect
from app.config import settings

engine = create_engine(settings.DATABASE_URL)
insp = inspect(engine)

columns = insp.get_columns("users")
print("Таблица users содержит следующие поля:")
for col in columns:
    print(f"- {col['name']} ({col['type']})")
