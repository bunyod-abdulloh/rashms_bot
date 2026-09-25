from utils.db_api.core import Database


class UsersDB:
    def __init__(self, db: Database):
        self.db = db

    # =========================== TABLE | USERS ==========================
    async def add_user(self, telegram_id):
        sql = "INSERT INTO users (telegram_id) VALUES($1) ON CONFLICT (telegram_id) DO NOTHING"
        return await self.db.execute(sql, telegram_id)

    async def check_user(self, telegram_id):
        sql = """
            SELECT EXISTS (SELECT 1 FROM users WHERE telegram_id = $1)
            """
        return await self.db.fetchval(sql, telegram_id)


    async def get_users(self, limit=1000, offset=0):
        sql = """
            SELECT telegram_id
            FROM users
            LIMIT $1 OFFSET $2
        """
        return await self.db.fetch(
            sql,
            limit,
            offset
        )

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users"
        return await self.db.fetchval(sql)

    async def delete_user(self, telegram_id):
        await self.db.execute(f"DELETE FROM users WHERE telegram_id='{telegram_id}'")

    async def drop_table_users(self):
        await self.db.execute("DROP TABLE users")

    async def get_all_users_dict(self):
        sql = "SELECT id, telegram_id, full_name, teacher_id FROM users"
        records = await self.db.fetch(sql)
        return {row["telegram_id"]: [row["full_name"], row['id'], row['teacher_id']] for row in records}
