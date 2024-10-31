from environs import Env

env = Env()
env.read_env()

MIRO_ACCESS_TOKEN= env.str('MIRO_ACCESS_TOKEN')
BOARD_ID = env.str('BOARD_ID')

DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_HOST = env.str('DB_HOST')
DB_PORT = env.str('DB_PORT')

SQL_DIALECT = 'postgresql'
DRIVER = 'psycopg2'
DATABASE = 'Duolingo'

CONNECTION_URL = f'{SQL_DIALECT}+{DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE}'


class Config:
    SQLALCHEMY_DATABASE_URI = CONNECTION_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
