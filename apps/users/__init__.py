from apps.users.handlers.api import auth
from apps.users.handlers.api import users

routers = (auth.router, users.router)
