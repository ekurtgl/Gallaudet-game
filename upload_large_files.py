# based on https://www.youtube.com/watch?app=desktop&v=nSfHrNarqD0&ab_channel=JieJenn

import os
import requests
from ms_graph import GRAPH_API_ENDPOINT, generate_access_token

app_id = '5b719a7e-265e-4a9e-8679-2316153fbab9'
scopes = ['Files.ReadWrite']

# Step 1. Generate Access Token

access_token = generate_access_token(app_id, scopes)
headers = {
    'Authorization': 'Bearer ' + access_token['access_token']
}

# Step 2. Read the file

# file_path = r'C:\Users\emrek\Desktop\Technical\Villanova'
# fname = 'pred_baseline.txt'
file_path = r'C:\ti\mmwave_studio_03_00_00_14\mmWaveStudio\PostProc'
fname = 'adc_data_Raw_0.bin'

file_name = os.path.join(file_path, fname)
print(file_name)

if not os.path.exists(file_name):
    raise Exception(f'{fname} is not found.')

with open(file_name, 'rb') as upload:
    media_content = upload.read()

# Step 3.1.1 Upload a large file (<400 MB)

# folder_id = '%2Fpersonal%2Fekurtoglu_crimson_ua_edu%2FDocuments%2Ftest'
folder_id = 'FBBB1EF1AC125F00%21442'
request_body = {
    'item': {
        'description': 'a large file',
        'name': fname
    }
}

# Step 3.1.2 create an upload session
drive_path = f'/me/drive/items/{folder_id}:/{fname}:/createUploadSession'
# drive_path = '/personal/ekurtoglu_crimson_ua_edu/_layouts/15/onedrive.aspx?id=' \
#              '%2Fpersonal%2Fekurtoglu%5Fcrimson%5Fua%5Fedu%2FDocuments%2Ftest/createUploadSession'
response_upload_session = requests.post(
    GRAPH_API_ENDPOINT + drive_path,
    headers=headers,
    json=request_body
)
print(f'/me/drive/items/{folder_id}:/{fname}:/createUploadSession')
print('response_upload_session:\n', response_upload_session.json(), '\n')

try:
    upload_url = response_upload_session.json()['uploadUrl']
    response_upload_status = requests.put(upload_url, data=media_content)
    print('response_upload_status:\n', response_upload_status.reason, '\n')
except Exception as e:
    print('Exception:', e)





