from pydantic_settings import BaseSettings
from typing import ClassVar


class Settings(BaseSettings):
    DATABASE_URL: ClassVar[str] = "postgresql+asyncpg://postgres:admin123@localhost:5432/postgres"

    class config:
        env_file = ".env"


settings = Settings()


# sqlalchemy.exc.IntegrityError: (sqlalchemy.dialects.postgresql.asyncpg.IntegrityError) <class 'asyncpg.exceptions.ForeignKeyViolationError'>: insert or update on table "event_slots" violates foreign key constraint "event_slots_user_id_fkey"
# DETAIL:  Key (user_id)=(2) is not present in table "users".
# [SQL: INSERT INTO event_slots (start_time, end_time, week, is_booked, category_id, user_id) VALUES ($1::TIMESTAMP WITH TIME ZONE, $2::TIMESTAMP WITH TIME ZONE, $3::INTEGER, $4::BOOLEAN, $5::INTEGER, $6::INTEGER) RETURNING event_slots.id]
# [parameters: (datetime.datetime(2026, 3, 8, 12, 55, 26, 218000, tzinfo=TzInfo(0)), datetime.datetime(2026, 3, 8, 12, 55, 26, 218000, tzinfo=TzInfo(0)), 1, False, 1, 2)]