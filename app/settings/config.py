from dotenvironment import DotEnvironment
from urllib.parse import quote

env = DotEnvironment('OBLIVION_GRID_')

class CONFIG:
    DATABASE_DRIVER = "postgresql+psycopg"
    DATABASE_USER = env.variable("DATABASE_USER", lambda arg: quote(arg, safe= ""))
    DATABASE_PASSWORD = env.variable("DATABASE_PASSWORD", lambda arg: quote(arg, safe= ""))
    DATABASE_HOST = env.variable("DATABASE_HOST")
    DATABASE_PORT = env.variable("DATABASE_PORT")
    DATABASE_NAME = env.variable("DATABASE_NAME")
