import os

import json

from dotenv import load_dotenv

from aiohttp import web

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, Float, Boolean

from handlers import handle_request, PARSE_ERROR, PARAMS_ERROR
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
def create_account(name: str, overdraft: bool, amount=0):
    account = Account(name=name, overdraft=overdraft, amount=amount)

    session.add(account)
    session.commit()

    return account.id


@validator
def transfer_money(donor_id: int, recipient_id: int, amount: int):
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
def get_balance(account_id: int):
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
            result = method(*params)
        else:
            result = method(**params)

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


def is_true(value: str) -> bool:
    return value.lower() == 'true'


if __name__ == '__main__':
    load_dotenv()

    session = get_session(
        db=os.getenv('DATABASE'),
        echo=is_true(os.getenv('DATABASE_DEBUG', '')),
    )

    app = web.Application()
    app.add_routes([
        web.post('/jsonrpc', handle_jsonrpc),
    ])

    web.run_app(app,
                host=os.getenv('SERVER_HOST'),
                port=os.getenv('SERVER_PORT'),
                )
