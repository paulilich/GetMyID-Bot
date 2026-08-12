import sqlite3
from pathlib import Path

from logs.record_log import log_info, log_error

# resolve DB relative to this file, not the process cwd
_DEFAULT_DB_PATH = Path(__file__).resolve().parent / 'users.db'


class Users:
    def __init__(self, db_path=None):
        self.db_path = str(db_path) if db_path else str(_DEFAULT_DB_PATH)


    def get_connection(self):
        return sqlite3.connect(self.db_path)


    def init_db(self):
        try:

            log_info('DB | init_db')


            with self.get_connection() as conn:
                cursor = conn.cursor()



                cursor.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS Users (
                        user_id INTEGER PRIMARY KEY,
                        language TEXT
                    )
                    '''
                )


                conn.commit()

        except Exception as e:
            log_error(f'DB | error during db initialization: {e}')


    def add_user(self, user_id):
        try:
            log_info('DB | add_user')

            with self.get_connection() as conn:
                cursor = conn.cursor()


                cursor.execute('SELECT user_id FROM Users WHERE user_id = ?', (user_id,))
                user = cursor.fetchone()


                if user is None:
                    cursor.execute(
                        '''INSERT INTO Users (user_id)
                           VALUES (?)''',
                        (user_id, )
                    )

                conn.commit()

        except Exception as e:
            log_error(f'DB | error when adding a user: {e}')



    def set_language(self, user_id, language):
        try:
            log_info('DB | set_language')

            with self.get_connection() as conn:
                cursor = conn.cursor()



                cursor.execute('UPDATE Users SET language = ? WHERE user_id = ?', (language, user_id))


                conn.commit()

        except Exception as e:
            log_error(f'DB | error in set_language: {e}')




    def get_language(self, user_id):
        try:
            log_info('DB | get_language')

            with self.get_connection() as conn:
                cursor = conn.cursor()


                cursor.execute('SELECT language FROM Users WHERE user_id = ?', (user_id, ))
                language = cursor.fetchone()


                return language[0]


        except Exception as e:
            log_error(f'DB | error in get_language: {e}')