from fastapi import FastAPI

from peewee_async import (
    Manager,
    PostgresqlDatabase
)

app = FastAPI()

database = PostgresqlDatabase(
    database='postgres',
    user='postgres',
    host='db',
    port='5432',
    password='',
)

db_manager = Manager(database)
