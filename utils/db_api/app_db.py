from utils.db_api.core import Database


class AppDB:
    def __init__(self, db: Database):
        self.db = db

    async def get_teachers(self):
        sql = """
            SELECT id, first_name, last_name FROM users_user WHERE role = 'teacher'
            """
        return await self.db.execute(sql, fetch=True)

    async def get_teacher_by_id(self, teacher_id: int):
        sql = """
            SELECT telegram_id, first_name, last_name FROM users_user WHERE id = $1
            """
        return await self.db.execute(sql, teacher_id, fetchrow=True)

    async def check_user(self, telegram_id):
        sql = """
            SELECT EXISTS (SELECT 1 FROM users_user WHERE telegram_id = $1)
            """
        return await self.db.execute(sql, telegram_id, fetchval=True)

    async def get_athlete_full(self, telegram_id: int):
        sql = """
            SELECT 
                uu.full_name, 
                uu.phone_number,
                uu.id AS user_id, 
                pp.sport_type, 
                pp.sport_experience_years AS sport_years,
                pp.hobbies
            FROM users_user AS uu
            JOIN profiles_athleteprofile AS pp 
                ON pp.user_id = uu.id 
            WHERE uu.telegram_id = $1                 
        """
        return await self.db.execute(sql, telegram_id, fetchrow=True)

    async def get_last_test_results(self, test_type, user_id: int):
        sql = """
            SELECT ur.scores 
            FROM core_userresult AS ur 
            JOIN core_test ct ON ct.id = ur.test_id 
            WHERE ct.code = $1 AND ur.user_id = $2  
            ORDER BY ur.id DESC 
            LIMIT 1
        """
        return await self.db.execute(sql, test_type, user_id, fetchrow=True)

    async def get_all_athlets(self):
        sql = """
             SELECT id, full_name FROM users_user 
             """
        return await self.db.execute(sql, fetch=True)

    async def get_count_athlets(self):
        sql = """
            SELECT COUNT(id) FROM users_user WHERE phone_number IS NOT NULL            
            """
        return await self.db.execute(sql, fetchval=True)

    async def get_users_page(self, limit: int, offset: int) -> list:
        query = """
            SELECT telegram_id, full_name
            FROM users_user WHERE phone_number IS NOT NULL AND telegram_id IS NOT NULL
            ORDER BY full_name ASC
            LIMIT $1 OFFSET $2
        """
        return await self.db.execute(query, limit, offset, fetch=True)

    # async def add_demo_athlets(self, telegram_id: int, phone_number: str, password: str, email: str):
    #     sql = """
    #         INSERT INTO users_user (
    #         telegram_id,
    #         phone_number,
    #         password,
    #         is_superuser,
    #         email,
    #         is_staff,
    #         is_active,
    #         date_joined)
    #         VALUES (
    #         $1, $2, $3, False, $4, False, False, now() AT TIME ZONE 'UTC'
    #         )
    #         """
    #     await self.db.execute(sql, telegram_id, phone_number, password, email, execute=True)
    #
    # async def add_demo_profile(self, user_id):
    #     sql = """
    #         INSERT INTO profiles_athleteprofile(
    #         sport_type,
    #         sport_experience_years,
    #         hobbies,
    #         is_completed,
    #         created_at,
    #         updated_at,
    #         user_id)
    #         VALUES ('Boks', 10, 'Not', True, now(), now(), $1)
    #     """
    #     await self.db.execute(sql, user_id, execute=True)

    async def get_athlete_by_phone(self, phone_number: str):
        sql = """
            SELECT telegram_id FROM users_user WHERE phone_number = $1 AND telegram_id IS NOT NULL
            """
        return await self.db.execute(sql, phone_number, fetchrow=True)

    async def get_athlete_to_xlsx(self):
        sql = """
            SELECT                
                uu.full_name,
                uu.phone_number,

                pa.sport_type,
                pa.sport_experience_years,
                pa.hobbies,

                jsonb_object_agg(
                    ct.code,
                    ur.scores
                ) AS tests

            FROM core_userresult AS ur

            INNER JOIN users_user AS uu
                ON uu.id = ur.user_id

            INNER JOIN profiles_athleteprofile AS pa
                ON pa.user_id = uu.id

            INNER JOIN core_test AS ct
                ON ct.id = ur.test_id

            GROUP BY
                uu.id,
                pa.id
            ORDER BY uu.id
        """
        return await self.db.execute(sql, fetch=True)

    async def on_tests(self):
        sql = "UPDATE core_test SET is_active = TRUE"

        await self.db.execute(sql, execute=True)

    async def off_tests(self):
        sql = """
            UPDATE core_test SET is_active = False
            """
        await self.db.execute(sql, execute=True)

    async def check_test_status(self):
        sql = """
            SELECT code, is_active FROM core_test 
            """
        return await self.db.execute(sql, fetch=True)
