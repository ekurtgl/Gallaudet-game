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
file_path = r'C:\Users\emrek\Desktop\trash'
fname = 'master_0000_data.bin'

file_name = os.path.join(file_path, fname)
print(file_name)

if not os.path.exists(file_name):
    raise Exception(f'{fname} is not found.')

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

try:
    upload_url = response_upload_session.json()['uploadUrl']
except Exception as e:
    print('Exception:', e)

# Step 3.2 Upload a really large file (>400MB)

with open(file_name, 'rb') as upload:
    total_file_size = os.path.getsize(file_name)
    chunk_size = 327680 * 300  # should be multiple of 327680 bytes
    chunk_number = total_file_size // chunk_size
    chunk_leftover = total_file_size - (chunk_size * chunk_number)
    counter = 0

    while True:
        chunk_data = upload.read(chunk_size)

        start_index = counter * chunk_size
        end_index = start_index + chunk_size

        if not chunk_data:
            break
        if counter == chunk_number:
            end_index = start_index + chunk_leftover

        headers = {
            'Content-Length': f'{chunk_size}',
            'Content-Range': f'bytes {start_index}-{end_index-1}/{total_file_size}'
        }

        chunk_data_upload_status = requests.put(
            upload_url,
            headers=headers,
            data=chunk_data
        )

        if 'createdBy' in chunk_data_upload_status.json():
            print('File upload complete!')
        else:
            print('Upload Progress: {0}'.format(chunk_data_upload_status.json()['nextExpectedRanges']))
            counter += 1
            # print(chunk_data_upload_status.json())
            # break

# Cancel upload
# requests.delete(upload_url)






