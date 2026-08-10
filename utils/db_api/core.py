from typing import Iterable, Sequence, Union

import asyncpg
from asyncpg import Pool

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

    async def bulk_upsert_ignore(
            self,
            table_name: str,
            columns: list[str],
            conflict_columns: list[str],
            records: Iterable[tuple],
    ):
        """
        Ommaviy INSERT, duplicate (conflict_columns bo'yicha) uchrasa — pass qilinadi.
        """
        cols_str = ", ".join(columns)
        placeholders = ", ".join(f"${i + 1}" for i in range(len(columns)))
        conflict_str = ", ".join(conflict_columns)

        query = f"""
            INSERT INTO {table_name} ({cols_str})
            VALUES ({placeholders})
            ON CONFLICT ({conflict_str}) DO NOTHING
        """

        async with self.pool.acquire() as connection:
            await connection.executemany(query, records)

    async def copy_records(
            self,
            table_name: str,
            columns: list[str],
            records: Iterable[dict],
            chunk_size: int = 10_000,
    ):
        async with self.pool.acquire() as connection:
            batch = []

            for row in records:
                batch.append(tuple(row.get(col) for col in columns))

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
            CREATE TABLE IF NOT EXISTS rasch_tmp(            
                id SERIAL PRIMARY KEY,
                teacher_id INTEGER NULL,
                pupil_id INTEGER NOT NULL,
                test_id INTEGER NOT NULL,
                essay_ball FLOAT NULL,
                UNIQUE(pupil_id, test_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS rash_results (
                id SERIAL PRIMARY KEY,
                teacher_id INTEGER NULL,
                pupil_id INTEGER NOT NULL,
                test_id INTEGER NOT NULL,
                t1 FLOAT NULL,
                t2 FLOAT NULL,
                rasch FLOAT NULL,
                percent INTEGER NOT NULL DEFAULT 0,
                grade VARCHAR(5) NULL,
                created_at DATE NOT NULL DEFAULT NOW(),                
                UNIQUE(pupil_id, test_id)
            )
            """
        ]
        # Execute each table creation query
        for query in queries:
            await self.execute(query)
