import os, re, client

from dotenv import load_dotenv

dotenv_file = '.env'
if os.path.isfile('.env.local'):
    dotenv_file = '.env.local'
load_dotenv(dotenv_file)

def __main__():
    message = ("Перейди по ссылке ниже, чтобы сгенирировать code для получения токена доступа:\n"
               f"{client.get_login_url()}\n"
               "Полученный code из адресной строки вставь сюда: ")
    code = input(message)
    token_json = client.get_access_token_by_code(code).json()
    save_token(token_json)
    message = ("Токен был сохранен в ваш .env файл и в дальнейшем будет использоваться для выполнения запросов.\n"
               f"Access token: {token_json['access_token']}\n"
               f"Refresh token: {token_json['refresh_token']}")
    print(message)

def save_token(token_json: str) -> None:
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
                new_dotenv_content = new_dotenv_content + f"\nACCESS_TOKEN={access_token}"
            
            if 'REFRESH_TOKEN' in old_dotenv_content:
                new_dotenv_content = re.sub(r'REFRESH_TOKEN=.+', 'REFRESH_TOKEN=' + refresh_token, new_dotenv_content)
            else:
                new_dotenv_content = new_dotenv_content + f"\nREFRESH_TOKEN={refresh_token}"
            
            file.write(new_dotenv_content)
    else:
        raise SystemExit('Токен не был сохранен! Ошибка: ' + token_json['error_description'])

if __name__ == "__main__":
   __main__()
