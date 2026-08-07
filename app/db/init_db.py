from __future__ import annotations

from sqlalchemy import inspect, text
from sqlalchemy.engine import Connection

from app.db.base import Base
from app.db.session import engine
from app.models import Review, Task, User  # noqa: F401


def _migrate_legacy_schema(connection: Connection) -> None:
    inspector = inspect(connection)
    tables = set(inspector.get_table_names())

    if "tasks" in tables:
        task_columns = {column["name"] for column in inspector.get_columns("tasks")}
        if "user" in task_columns and "user_id" not in task_columns:
            connection.execute(text("ALTER TABLE tasks RENAME TO tasks_legacy"))
            connection.execute(
                text(
                    """
                    CREATE TABLE tasks (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(128) NOT NULL,
                        phone VARCHAR(32) NOT NULL,
                        work_type VARCHAR(128) NOT NULL,
                        address VARCHAR(256),
                        arrival_time VARCHAR(128) NOT NULL,
                        status VARCHAR(32) NOT NULL DEFAULT 'new',
                        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
                    )
                    """
                )
            )
            connection.execute(
                text(
                    """
                    INSERT INTO tasks (id, name, phone, work_type, address, arrival_time, status, created_at, user_id)
                    SELECT
                        id,
                        name,
                        SUBSTR(phone, 1, 32),
                        work_type,
                        address,
                        COALESCE(CAST(arrival_time AS TEXT), ''),
                        'new',
                        COALESCE(created_at, CURRENT_TIMESTAMP),
                        user
                    FROM tasks_legacy
                    """
                )
            )
            connection.execute(text("DROP TABLE tasks_legacy"))

    inspector = inspect(connection)
    tables = set(inspector.get_table_names())

    if "review" in tables:
        reviews_count = connection.execute(text("SELECT COUNT(*) FROM reviews")).scalar_one()
        legacy_reviews_count = connection.execute(text("SELECT COUNT(*) FROM review")).scalar_one()
        if reviews_count == 0 and legacy_reviews_count > 0:
            connection.execute(
                text(
                    """
                    INSERT INTO reviews (name, title, stars, created_at, user_id)
                    SELECT
                        COALESCE(name, 'Без имени'),
                        title,
                        CAST(stars AS INTEGER),
                        CURRENT_TIMESTAMP,
                        user
                    FROM review
                    """
                )
            )
        connection.execute(text("DROP TABLE review"))

    connection.execute(text("CREATE INDEX IF NOT EXISTS ix_tasks_created_at ON tasks (created_at)"))
    connection.execute(text("CREATE INDEX IF NOT EXISTS ix_tasks_status ON tasks (status)"))
    connection.execute(text("CREATE INDEX IF NOT EXISTS ix_tasks_user_id ON tasks (user_id)"))
    connection.execute(text("CREATE INDEX IF NOT EXISTS ix_reviews_created_at ON reviews (created_at)"))
    connection.execute(text("CREATE INDEX IF NOT EXISTS ix_reviews_user_id ON reviews (user_id)"))
    connection.execute(text("CREATE INDEX IF NOT EXISTS ix_users_tg_id ON users (tg_id)"))


async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.run_sync(_migrate_legacy_schema)
        await connection.run_sync(Base.metadata.create_all)
