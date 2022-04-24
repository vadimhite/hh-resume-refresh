import os, requests, re

from dotenv import load_dotenv

dotenv_file = '.env'
if os.path.isfile('.env.local'):
    dotenv_file = '.env.local'
load_dotenv(dotenv_file)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
BASE_URL = 'https://hh.ru/oauth'

if (
    CLIENT_ID == None or
    CLIENT_SECRET == None or
    REDIRECT_URI == None
    ):
    raise SystemExit('You forgot to paste the client data (such as client_id, client_secret, redirect_uri) into the .env file.')

def __main__():
    message = ("Перейди по ссылке ниже, чтобы сгенирировать code для получения токена доступа:\n"
               f"{get_login_url()}\n"
               "Полученный code из адресной строки вставь сюда: ")
    code = input(message)
    token_json = get_token_by_code(code)
    save_token(token_json)
    message = ("Токен был сохранен в ваш .env файл и в дальнейшем будет использоваться для выполнения запросов.\n"
               f"Access token: {token_json['access_token']}\n"
               f"Refresh token: {token_json['refresh_token']}")
    print(message)


def get_login_url():
    return f"{BASE_URL}/authorize?response_type=code&client_id={CLIENT_ID}&state=state&redirect_uri={REDIRECT_URI}"

def get_token_by_code(code):
    try:
        response = requests.post(
            f"{BASE_URL}/token",
            params={
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': REDIRECT_URI
            },
        )
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    return response.json()

def save_token(token_json):
    # Rewrite the .env file with the new access token.
    if 'access_token' in token_json:
        access_token = token_json['access_token']
        refresh_token = token_json['refresh_token']
        with open(dotenv_file, 'r+') as file:
            old_dotenv_content = file.read()
            file.seek(0)
            file.truncate()

            new_dotenv_content = old_dotenv_content
            if 'ACCESS_TOKEN' in old_dotenv_content:
                new_dotenv_content = re.sub(r'ACCESS_TOKEN=.+', 'ACCESS_TOKEN=' + access_token, new_dotenv_content)
            else:
                new_dotenv_content = new_dotenv_content + f"ACCESS_TOKEN={access_token}\n"
            
            if 'REFRESH_TOKEN' in old_dotenv_content:
                new_dotenv_content = re.sub(r'REFRESH_TOKEN=.+', 'REFRESH_TOKEN=' + refresh_token, new_dotenv_content)
            else:
                new_dotenv_content = new_dotenv_content + f"REFRESH_TOKEN={refresh_token}\n"
            
            file.write(new_dotenv_content)
    else:
        raise SystemExit('The access token has not been updated! Error: ' + token_json['error_description'])

if __name__ == "__main__":
   __main__()
