from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool, MetaData
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

config = context.config
fileConfig(config.config_file_name)

try:
    from app.db.database import Base
    try:
        from app.core.config import settings
    except Exception:
        from app.core import settings
    config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
    target_metadata = Base.metadata
except Exception:
    target_metadata = MetaData()

def run_migrations_offline():
    url = config.get_main_option('sqlalchemy.url')
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
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
