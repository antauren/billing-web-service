import json
import os

from aiohttp import web
from dotenv import load_dotenv
from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from handlers import (PARAMS_ERROR, PARSE_ERROR, UNIDENTIFIED_ERROR,
                      handle_request)
from validators import validator

base = declarative_base()


class Account(base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Float, default=0)
    overdraft = Column(Boolean)

    def __repr__(self):
        return '<Account {} {}>'.format(self.id, self.name)


def get_session(db, echo=False):
    engine = create_engine(db, echo=echo)

    base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session


@validator
async def create_account(name: str, overdraft: bool, amount=0):
    account = Account(name=name, overdraft=overdraft, amount=amount)

    session.add(account)
    session.commit()

    return account.id


@validator
async def transfer_money(donor_id: int, recipient_id: int, amount: int):
    donor = session.query(Account).get(donor_id)
    recipient = session.query(Account).get(recipient_id)

    if (not donor.overdraft) and (donor.amount - amount < 0):
        return False

    try:
        donor.amount -= amount
        recipient.amount += amount
    except:
        session.rollback()
        return False

    session.commit()

    return True


@validator
async def get_balance(account_id: int):
    account = session.query(Account).get(account_id)

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
        if isinstance(params, list):
            result = await method(*params)
        else:
            result = await method(**params)

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

    database = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'.format(

        user=os.getenv('DATABASE_USERNAME'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        port=os.getenv('DATABASE_PORT'),
        dbname=os.getenv('DATABASE_NAME'),
    )

    session = get_session(
        db=database,
        echo=is_true(os.getenv('DATABASE_DEBUG', '')),
    )

    app = web.Application()
    app.add_routes([
        web.post('/jsonrpc', run_json_rpc_server),
    ])

    web.run_app(app,
                host=os.getenv('SERVER_HOST'),
                port=os.getenv('SERVER_PORT'),
                )
