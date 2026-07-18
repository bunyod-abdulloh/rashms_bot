from utils.db_api.core import Database


class RashDB:
    def __init__(self, db: Database):
        self.db = db

    async def bulk_add_rash_results(self, results):
        """
        results = [
            (
                pupil_id,
                test_id,
                test_ball,
                essay_ball,
                rash_ball,
                percent,
                grade,
            ),
            ...
        ]
        """

        await self.db.copy_records(
            table_name="rash_results",
            columns=[
                "pupil_id",
                "test_id",
                "test_ball",
                "essay_ball",
                "rash_ball",
                "percent",
                "grade",
            ],
            records=results,
            chunk_size=10_000,
        )

    async def get_tests(self):
        sql = """
            SELECT
                ts.id,
                ts.subject,
                ts.test_code
            FROM admin_panel_teststatus ts
            WHERE ts.id IN (
                SELECT DISTINCT test_code_id
                FROM pupil_testresult
            )
            ORDER BY ts.id DESC;
        """
        return await self.db.fetch(sql)

    async def get_subject(self, test_code_id):
        sql = """
            SELECT subject FROM admin_panel_teststatus WHERE id = $1
            """
        return await self.db.fetch(sql, test_code_id)

    async def get_results(self, test_code_id):
        sql = """
            SELECT * FROM pupil_testresult WHERE test_code_id = $1
            """
        return await self.db.fetch(sql, test_code_id)
