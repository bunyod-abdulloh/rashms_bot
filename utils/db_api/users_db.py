from utils.db_api.core import Database


class UsersDB:
    def __init__(self, db: Database):
        self.db = db

    # =========================== TABLE | USERS ==========================
    async def add_user(self, telegram_id):
        sql = "INSERT INTO users (telegram_id) VALUES($1) ON CONFLICT (telegram_id) DO NOTHING"
        return await self.db.execute(sql, telegram_id, execute=True)

    async def check_user(self, telegram_id):
        sql = """
            SELECT EXISTS (SELECT 1 FROM users WHERE telegram_id = $1)
            """
        return await self.db.execute(sql, telegram_id, fetchval=True)

    async def set_language(self, language, telegram_id):
        sql = """
            UPDATE users SET language = $1 WHERE telegram_id = $2
            """
        await self.db.execute(sql, language, telegram_id, execute=True)

    async def get_language(self, telegram_id):
        sql = """
            SELECT language FROM users WHERE telegram_id = $1
            """
        return await self.db.execute(sql, telegram_id, fetchval=True)

    async def get_users(self, limit=1000, offset=0):
        sql = """
            SELECT telegram_id
            FROM users
            LIMIT $1 OFFSET $2
        """
        return await self.db.execute(
            sql,
            limit,
            offset,
            fetch=True
        )

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users"
        return await self.db.execute(sql, fetchval=True)

    async def delete_user(self, telegram_id):
        await self.db.execute(f"DELETE FROM users WHERE telegram_id='{telegram_id}'", execute=True)

    async def drop_table_users(self):
        await self.db.execute("DROP TABLE users", execute=True)
