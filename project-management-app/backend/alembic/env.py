import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- CUSTOM PART ---
# Import your models' Base metadata object
# Make sure all models are imported so Base knows about them
from database import SQLALCHEMY_DATABASE_URL # Use your actual DB URL import
from models import Base # Import Base from the models package's __init__.py
# The __init__.py in models should import all individual model modules (user, project, etc.)
# This ensures Base.metadata contains all table definitions.

target_metadata = Base.metadata
# --- END CUSTOM PART ---

def run_migrations_offline() -> None:
    url = SQLALCHEMY_DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True, # Add compare_type for better Enum detection
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    from database import engine
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True, # Add compare_type for better Enum detection
            # Include rendering options for enums if needed by specific dialects
            # render_item=render_enum_for_sqlite if 'sqlite' in connectable.dialect.name else None
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
