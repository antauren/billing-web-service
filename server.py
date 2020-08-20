import json
import os
from functools import partial

from aiohttp import web
from dotenv import load_dotenv
import sqlalchemy as sa

from db import accounts, close_pg, init_pg, create_sa_transaction_tables
from handlers import (PARAMS_ERROR, PARSE_ERROR, UNIDENTIFIED_ERROR,
                      handle_request)
from validators import validator


@validator
async def create_account(conn, name: str, overdraft: bool, amount=0):
    cursor = await conn.execute(sa.insert(accounts).values(name=name, overdraft=overdraft, amount=amount))
    account = await cursor.fetchone()

    return account.id


@validator
async def transfer_money(conn, donor_id: int, recipient_id: int, amount: int):
    donor_where = accounts.c.id == donor_id
    donor_query = accounts.select().where(donor_where)
    donor = await (await conn.execute(donor_query)).fetchone()

    recipient_where = accounts.c.id == recipient_id
    recipient_query = accounts.select().where(recipient_where)
    recipient = await (await conn.execute(recipient_query)).fetchone()

    if (not donor.overdraft) and (donor.amount - amount < 0):
        return False

    trans = await conn.begin()
    try:
        await conn.execute(sa.update(accounts).values({'amount': donor.amount - amount}).where(donor_where))
        await conn.execute(sa.update(accounts).values({'amount': recipient.amount + amount}).where(recipient_where))
    except:
        await trans.rollback()
        return False
    else:
        await trans.commit()
        return True


@validator
async def get_balance(conn, account_id: int):
    where = accounts.c.id == account_id
    query = accounts.select().where(where)
    account = await (await conn.execute(query)).fetchone()

    return account.amount


async def handle_jsonrpc(request):
    try:
        request_dict = await request.json()
    except json.JSONDecodeError:
        return web.json_response(PARSE_ERROR)

    methods = {
        'create_account': create_account,
        'transfer_money': transfer_money,
        'get_balance': get_balance,
    }

    error_response = handle_request(request_dict, methods)

    if error_response:
        return web.json_response(error_response)

    method = methods[request_dict['method']]
    params = request_dict.get('params', [])

    try:
        async with request.app['db'].acquire() as conn:
            await create_sa_transaction_tables(conn)

            if isinstance(params, list):
                result = await method(conn, *params)
            else:
                result = await method(conn, **params)

    except TypeError:
        error = PARAMS_ERROR.copy()
        error['id'] = request_dict.get('id', None)

        return web.json_response(error)

    response_dict = {
        'result': result,
        'id': request_dict.get('id', None),
        'jsonrpc': '2.0'
    }

    return web.json_response(
        response_dict
    )


async def run_json_rpc_server(request):
    try:
        result = await handle_jsonrpc(request)
        return result
    except:
        return web.json_response(UNIDENTIFIED_ERROR)


def is_true(value: str) -> bool:
    return value.lower() == 'true'


if __name__ == '__main__':
    load_dotenv()

    db_url = 'postgresql://{user}:{password}@{host}:{port}/{dbname}'.format(

        user=os.getenv('DATABASE_USERNAME'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        port=os.getenv('DATABASE_PORT'),
        dbname=os.getenv('DATABASE_NAME'),
    )

    app = web.Application()
    app.add_routes([
        web.post('/jsonrpc', run_json_rpc_server),
    ])

    app.on_startup.append(partial(init_pg, db_url=db_url))
    app.on_cleanup.append(close_pg)
    web.run_app(app,
                host=os.getenv('SERVER_HOST'),
                port=os.getenv('SERVER_PORT'),
                )
