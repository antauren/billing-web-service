def validate_create_account(name, overdraft, amount=0):
    if not isinstance(name, str):
        raise TypeError('"name" must be str type')

    if not isinstance(overdraft, bool):
        raise TypeError('"overdraft" must be bool type')

    if not (isinstance(amount, int) or isinstance(amount, float)):
        raise TypeError('"amount" must be float or int type')


def validate_transfer_money(donor_id, recipient_id, amount):
    if not isinstance(donor_id, int):
        raise TypeError('"donor_id" must be int type')

    if not (isinstance(amount, int) or isinstance(amount, float)):
        raise TypeError('"amount" must be float or int type')

    if not isinstance(recipient_id, int):
        raise TypeError('"recipient_id" must be str type')


def validate_get_balance(account_id):
    if not isinstance(account_id, int):
        raise TypeError('"account_id" must be int type')


def validator(func):
    def wrap(*args, **kwargs):
        validate_functions = {'create_account': validate_create_account,
                              'transfer_money': validate_transfer_money,
                              'get_balance': validate_get_balance
                              }

        validate_functions[func.__name__](*args[1:], **kwargs)

        return func(*args, **kwargs)

    return wrap
