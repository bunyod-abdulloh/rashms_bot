from utils.db_api.core import Database


class AdminDB:
    def __init__(self, db: Database):
        self.db = db

    # =========================== TABLE | SEND_STATUS ===========================
    async def add_send_status(self):
        sql = "INSERT INTO admin (send_post) VALUES (false)"
        return await self.db.execute(sql, execute=True)

    async def update_send_status(self, send_post):
        sql = "UPDATE admin SET send_post = $1"
        return await self.db.execute(sql, send_post, execute=True)

    async def get_send_status(self):
        sql = "SELECT send_post FROM admin"
        return await self.db.execute(sql, fetchval=True)
