from utils.db_api.core import Database


class AppDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_pupil(self, telegram_id, full_name, teacher_id):
        sql = """
            INSERT INTO users (telegram_id, full_name, teacher_id) VALUES ($1, $2, $3) ON CONFLICT (telegram_id) DO NOTHING
            """
        await self.db.execute(sql, telegram_id, full_name, teacher_id)

    async def get_teachers(self):
        sql = """
            SELECT id, first_name, last_name FROM admin_panel_user WHERE role = 'teacher' 
            """
        return await self.db.fetch(sql)

    async def get_teacher_by_id(self, teacher_id: int):
        sql = """
            SELECT telegram_id, first_name, last_name FROM admin_panel_user WHERE id = $1
            """
        return await self.db.fetchrow(sql, teacher_id)

    async def check_teacher(self, tg_id):
        sql = """
            SELECT id FROM users_user WHERE telegram_id = $1
            """
        return await self.db.fetchval(sql, tg_id)

    async def get_tch_test_code(self, teacher_id, test_code_id):
        sql = """
            SELECT
                tch.telegram_id,
                tch.first_name,
                tch.last_name,
                tt.test_code
            FROM admin_panel_user AS tch
            CROSS JOIN admin_panel_teststatus AS tt
            WHERE tch.id = $1
              AND tt.id = $2
        """
        return await self.db.fetchrow(sql, teacher_id, test_code_id)
