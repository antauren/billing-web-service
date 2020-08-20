import aiopg.sa
import sqlalchemy as sa
from sqlalchemy.schema import CreateTable
import psycopg2

metadata = sa.MetaData()

accounts = sa.Table(
    'account', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(255)),
    sa.Column('amount', sa.Float, default=0),
    sa.Column('overdraft', sa.Boolean),
)


async def init_pg(app, db_url):
    app['db'] = await aiopg.sa.create_engine(db_url)


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def create_sa_transaction_tables(conn):
    try:
        await conn.execute(CreateTable(accounts))
    except psycopg2.errors.DuplicateTable:
        pass
