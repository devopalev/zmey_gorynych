from environs import Env

env = Env()
env.read_env()

# SECURE
SECRET_KEY = env.str('SECRET_KEY', default='09d25e0953t54g2556c8181665g665b93f7099f6f0f54dsg3456')
ALGORITHM = env.str('ALGORITHM', default='HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = env.int('ACCESS_TOKEN_EXPIRE_MINUTES', default=24 * 60)

# DATABASE
POSTGRES_HOST = env.str('POSTGRES_HOST', default='localhost')
POSTGRES_PORT = env.int('POSTGRES_PORT', default=6434)
POSTGRES_USER = env.str('POSTGRES_USER', default='zmey')
POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD', default='rr9njBFklQX')
POSTGRES_DB = env.str('POSTGRES_DB', default='zmey_db')

DB_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
DB_POOL_MIN_SIZE = env.int('DB_POOL_MIN_SIZE', 1)
DB_POOL_MAX_SIZE = env.int('DB_POOL_MAX_SIZE', 10)
MIGRATIONS_PATH = env.str('MIGRATIONS_PATH', default='migrations')

# False - использует pg из settings (windows), True - использует локальный (mac, linux, docker)
TEST_DB_PROCESS_FACTORY = env.bool('TEST_DB_PROCESS_FACTORY', default=True)
