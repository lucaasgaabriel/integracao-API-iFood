import requests

def import_token():
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "clientId": "" # Digite o clientId para gerar token de acesso
    }
    payload = requests.post("https://merchant-api.ifood.com.br/authentication/v1.0/oauth/userCode", headers=headers,
                                data=data)
    response_token = payload.json()

    auth_code = response_token.get('userCode')
    auth_code_verifier = response_token.get('authorizationCodeVerifier')

    data_token = {
        "grantType": "client_credentials",
        "clientId": "", # Digite o clientId
        "clientSecret": "", # Digite o clientSecret
        "authorizationCode": f'{auth_code}',
        "authorizationCodeVerifier": f'{auth_code_verifier}',
        "refreshToken": ""

    }

    payload_token = requests.post("https://merchant-api.ifood.com.br/authentication/v1.0/oauth/token",
                                    headers=headers,
                                    data=data_token)

    response = payload_token.json()

    access_token = response.get('accessToken')
    # print(access_token)
    merchant_uuid = "" # Digite o merchant UUID
    catalog_uuid = "" # Digite o catalog UUID

    return access_token, merchant_uuid, catalog_uuid



