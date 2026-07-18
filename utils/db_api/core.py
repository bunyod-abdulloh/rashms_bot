from typing import Iterable, Sequence, Union

import asyncpg
from asyncpg import Connection, Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        """Create the connection pool for database."""
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(self, command, *args):
        async with self.pool.acquire() as connection:
            return await connection.execute(command, *args)

    async def executemany(self, command, args: Sequence[tuple]):
        async with self.pool.acquire() as connection:
            await connection.executemany(command, args)

    async def fetch(self, command, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(command, *args)

    async def fetchrow(self, command, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(command, *args)

    async def fetchval(self, command, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetchval(command, *args)

    async def copy_records(
            self,
            table_name: str,
            columns: list[str],
            records: Iterable[tuple],
            chunk_size: int = 10_000,
    ):
        """
        PostgreSQL COPY.

        Juda katta hajmdagi ma'lumotlarni tez insert qilish uchun.

        Args:
            table_name: Jadval nomi.
            columns: Ustunlar.
            records: tuple lar iterable'i.
            chunk_size: Har safar COPY qilinadigan yozuvlar soni.
        """
        async with self.pool.acquire() as connection:
            connection: Connection

            batch = []

            for row in records:
                batch.append(row)

                if len(batch) >= chunk_size:
                    await connection.copy_records_to_table(
                        table_name=table_name,
                        columns=columns,
                        records=batch,
                    )
                    batch.clear()

            if batch:
                await connection.copy_records_to_table(
                    table_name=table_name,
                    columns=columns,
                    records=batch,
                )

    async def create_tables(self):
        """Create the required tables in the database."""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,                
                telegram_id BIGINT NOT NULL UNIQUE,
                full_name VARCHAR(255) NOT NULL,
                teacher_id INTEGER NULL,
                is_paid BOOLEAN NOT NULL DEFAULT FALSE                                                
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS admin (
                id SERIAL PRIMARY KEY,
                send_post BOOLEAN DEFAULT FALSE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS rash_results (
                id SERIAL PRIMARY KEY,
                pupil_id INTEGER NOT NULL,
                test_id INTEGER NOT NULL,
                test_ball FLOAT NULL,
                essay_ball FLOAT NULL,
                rash_ball FLOAT NULL,
                percent INTEGER NOT NULL DEFAULT 0,
                grade VARCHAR(5) NULL,
                UNIQUE(pupil_id, test_id)
            )
            """
        ]
        # Execute each table creation query
        for query in queries:
            await self.execute(query)
