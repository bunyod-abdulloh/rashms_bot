from utils.db_api.core import Database


class AppDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_pupil(self, telegram_id, full_name, teacher_id):
        sql = """
            INSERT INTO users (telegram_id, full_name, teacher_id) VALUES ($1, $2, $3) ON CONFLICT (telegram_id) DO NOTHING
            """
        await self.db.execute(sql, telegram_id, full_name, teacher_id)
