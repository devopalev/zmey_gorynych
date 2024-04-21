from environs import Env

env = Env()
env.read_env()

# SYSTEM
ENVIRONMENT = env.str('ENVIRONMENT', default='local')

# SECURE
SECRET_KEY = env.str('SECRET_KEY', default='09d25e0953t54g2556c8181665g665b93f7099f6f0f54dsg3456')
ALGORITHM = env.str('ALGORITHM', default='HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = env.int('ACCESS_TOKEN_EXPIRE_MINUTES', default=24 * 60)

# DATABASE
DB_DSN = env.str('DSN', default='')
DB_POOL_MIN_SIZE = env.int('DB_POOL_MIN_SIZE', 1)
DB_POOL_MAX_SIZE = env.int('DB_POOL_MAX_SIZE', 10)
