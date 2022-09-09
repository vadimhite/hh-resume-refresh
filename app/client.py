import requests, os

from dotenv import load_dotenv

dotenv_file = '.env'
if os.path.isfile('.env.local'):
    dotenv_file = '.env.local'
load_dotenv(dotenv_file)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
AUTH_BASE_URL = 'https://hh.ru/oauth'
API_BASE_URL = 'https://api.hh.ru'
API_RESUME_URL = 'https://api.hh.ru/resumes'
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')

def get_login_url() -> str:
    return f"{AUTH_BASE_URL}/authorize?response_type=code&client_id={CLIENT_ID}&state=state&redirect_uri={REDIRECT_URI}"

def get_access_token_by_code(code: str) -> requests.Response:
    if (
        CLIENT_ID == None or
        CLIENT_SECRET == None or
        REDIRECT_URI == None
    ):
        raise SystemExit('Необходимо заполнить переменные окружения, такие как: CLIENT_ID, CLIENT_SECRET, REDIRECT_URI в .env/.env.local файле.')

    return post(
        AUTH_BASE_URL + '/token',
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI
        }
    )

def get_user_info():
    return get(
        API_BASE_URL + '/me',
        headers = {'Authorization': f"Bearer {get_access_token()}"}
    )

def get_resume_list() -> requests.Response:
    return get(
        API_RESUME_URL + '/mine',
        headers = {'Authorization': f"Bearer {get_access_token()}"}
    )

def publish_resume(resume_id: str) -> requests.Response:
    return post(
        f"{API_RESUME_URL}/{resume_id}/publish",
        headers = {'Authorization': f"Bearer {get_access_token()}"}
    )

def get_access_token() -> str:
    if (ACCESS_TOKEN == None):
        raise SystemExit('Access token не задан, необходимо пройти процесс авторизации! Запусти auth.py и следуй инструкции.')
    
    return ACCESS_TOKEN;

def get_refresh_token() -> str:
    if (REFRESH_TOKEN == None):
        raise SystemExit('Refresh token не задан, необходимо пройти процесс авторизации! Запусти auth.py и следуй инструкции.')
    
    return REFRESH_TOKEN;

def refresh_access_token():
    post(
        AUTH_BASE_URL + '/token',
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': get_refresh_token()
        }
    )

def post(url: str, data: dict = None, headers: dict = None) -> requests.Response:
    try:
        return requests.post(url = url, data = data, headers = headers)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

def get(url: str, params: dict = None, headers: dict = None) -> requests.Response:
    try:
        return requests.get(url = url, params = params, headers = headers)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
