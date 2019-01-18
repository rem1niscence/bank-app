import requests


def id_card_exists(id_card):
    id_url = 'https://apitest20190112092531.azurewebsites.net/api/cedula'
    req = requests.get(
        url=id_url, params={'cedula': id_card})
    return req.json()[0]


def get_client(client_id):
    url = 'https://apitest20190112092531.azurewebsites.' \
        f'net/api/clientes/{client_id}'
    req = requests.get(url)
    return req.json()[0]


def get_accounts(client_id):
    url = 'https://apitest20190112092531.azurewebsites.' \
        f'net/api/cuentas/{client_id}'
    req = requests.get(url)
    return req.json()


def get_account_movements(account_id):
    url = 'https://apitest20190112092531.azurewebsites.' \
        f'net/api/movimientos/{account_id}'
    req = requests.get(url)
    res = req.json()
    return res


def make_transaction(data):
    # Response Codes:
    # -1 - Issuer account doesn't exist
    # -2 - Receiver account doesn't exist
    # -3 - Insufficient founds
    url = 'https://apitest20190112092531.azurewebsites.net/api/transferencias'
    req = requests.post(url, json={
        'emisor': data['issuer'],
        'receptor': data['receiver'],
        'monto': data['amount'],
        'banco': 'bank-app'
    })
    res = req.json()
    return res
