from utils.db_api.core import Database


class RashDB:
    def __init__(self, db: Database):
        self.db = db

    async def bulk_add_rash_results(self, results: list[dict]):
        columns = ["test_id", "pupil_id", "t1", "t2", "rasch", "percent", "grade"]

        # dict -> tuple, aynan columns tartibida
        records = [tuple(row[col] for col in columns) for row in results]

        await self.db.bulk_upsert_ignore(
            table_name="rash_results",
            columns=columns,
            conflict_columns=["pupil_id", "test_id"],
            records=records,
        )

    # async def bulk_add_rash_results(self, results):
    #     """
    #     results = [
    #         (
    #             pupil_id,
    #             test_id,
    #             test_ball,
    #             rash_ball,
    #             percent,
    #             grade,
    #         ),
    #         ...
    #     ]
    #     """
    #
    #     await self.db.copy_records(
    #         table_name="rash_results",
    #         columns=[
    #             "test_id",
    #             "pupil_id",
    #             "t1",
    #             "t2",
    #             "rasch",
    #             "percent",
    #             "grade",
    #         ],
    #         records=results,
    #         chunk_size=10_000,
    #     )

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

    async def get_essay_ball(self, test_code_id):
        sql = """
            SELECT 
                rt.essay_ball,
                u.telegram_id
            FROM users u 
            JOIN rasch_tmp rt ON rt.pupil_id = u.id 
            WHERE rt.test_id = $1  
            """
        return await self.db.fetch(sql, test_code_id)

    async def get_results(self, test_code_id):
        sql = """
            SELECT * FROM pupil_testresult WHERE test_code_id = $1
            """
        return await self.db.fetch(sql, test_code_id)

    async def get_results_teacher(self, teacher_id, test_code_id):
        sql = """
            SELECT ptr.*
            FROM pupil_testresult ptr 
            JOIN users u 
            ON u.telegram_id = ptr.telegram_id 
            WHERE u.teacher_id = $1 AND rr.test_id = $2            
            """
        return await self.db.fetch(sql, teacher_id, test_code_id)

    async def get_test_code(self, test_code_id):
        sql = """
            SELECT test_code FROM admin_panel_teststatus WHERE id = $1
            """
        return await self.db.fetchval(sql, test_code_id)

    async def get_result_by_tch_id(self, teacher_id, test_code_id):
        sql = """
            SELECT 
                u.full_name,
                rr.t1,
                rr.t2,
                rr.rasch,
                rr.percent,
                rr.grade
            FROM rash_results rr 
            JOIN users u ON u.id = rr.pupil_id AND u.teacher_id = $1 
            WHERE rr.test_id = $2
            """
        return await self.db.fetch(sql, teacher_id, test_code_id)
