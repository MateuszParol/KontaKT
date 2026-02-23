
from peewee import SqliteDatabase
from kontakt import config

# Initialize database with foreign keys enabled
# deferred definition allows usage before initialization if needed, but here we init directly
database = SqliteDatabase(config.DB_FILE, pragmas={'foreign_keys': 1})
