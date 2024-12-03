from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context
from app.database import DATABASE_URL, Base  # Verilənlər bazası URL və metadata

# Alembic konfiqurasiyası
config = context.config

# Log faylları üçün konfiqurasiya
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Sinxronlaşdırılmış mühərrik yaratmaq
def sync_engine():
    from sqlalchemy.engine import create_engine
    return create_engine(DATABASE_URL.replace("asyncpg", "psycopg2"))

def run_migrations_offline():
    """Offline rejimdə migration işlədir."""
    url = config.get_main_option("sqlalchemy.url", DATABASE_URL)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Online rejimdə migration işlədir."""
    connectable = sync_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
