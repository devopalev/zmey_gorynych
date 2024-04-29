from backend.apps.users.handlers.api import auth
from backend.apps.users.handlers.api import users

routers = (auth.router, users.router)
