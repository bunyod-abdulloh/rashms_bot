from utils.db_api.core import Database


class TeachersDB:
    def __init__(self, db: Database):
        self.db = db

    async def check_teacher(self, teacher_telegram_id: int):
        sql = """
            SELECT EXISTS (SELECT 1 FROM admin_panel_user WHERE telegram_id = $1)
            """
        return await self.db.fetchval(sql, teacher_telegram_id)

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

    async def get_teacher_tests(self, teacher_telegram_id: int):
        sql = """
              SELECT DISTINCT ON (rr.test_id) ts.id,
                ts.test_code,
                                              rr.created_at
              FROM rash_results rr
                       JOIN admin_panel_teststatus ts ON ts.id = rr.test_id
              WHERE teacher_id = (SELECT id FROM admin_panel_user WHERE telegram_id = $1) \
              """
        return await self.db.fetch(sql, teacher_telegram_id)

    async def get_teacher_by_tg_id(self, teacher_tg_id: int):
        sql = """
              SELECT id
              FROM admin_panel_user
              WHERE telegram_id = $1 \
              """
        return await self.db.fetchval(sql, teacher_tg_id)
