import os, client

from dotenv import load_dotenv

dotenv_file = '.env'
if os.path.isfile('.env.local'):
    dotenv_file = '.env.local'
load_dotenv(dotenv_file)

resume_ids = os.getenv('RESUME_IDS')
resume_list = client.get_resume_list()

# Если access token просрочен, обновляем его
if (client.get_resume_list().status_code != 200):
    client.refresh_access_token()
    resume_list = client.get_resume_list()

if resume_ids != None:
    resume_ids = list(map(str.strip, resume_ids.split(',')))
else:
    resume_ids = []
    resume_list = resume_list.json()

    for resume in resume_list['items']:
        if resume['can_publish_or_update'] == True:
            resume_ids.append(resume['id'])

for resume_id in resume_ids:
    client.publish_resume(resume_id)
