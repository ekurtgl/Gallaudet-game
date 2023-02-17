# based on https://www.youtube.com/watch?v=1Jyd7SA-0kI&ab_channel=JieJenn
import webbrowser
import msal
import requests
from msal import PublicClientApplication

app_id = '5b719a7e-265e-4a9e-8679-2316153fbab9'
client_secret = 'OVo8Q~hSWof8_CIZ_9kX1gjlUXlFKF_y19WyYc02'
authority_url = 'https://login.microsoftonline.com/consumers/'
base_url = 'https://graph.microsoft.com/v1.0/'

scopes = ['User.Read']

# Method 2: Login to acquire access_token

app = PublicClientApplication(
    app_id,
    authority=authority_url
)

# accounts = app.get_accounts()
# if accounts:
#     app.acquire_token_silent(scopes=scopes, account=accounts[0])  # choose first account as default

flow = app.initiate_device_flow(scopes=scopes)
print(flow)
print(flow['message'])  # copy and paste this code to the app authentication
webbrowser.open(flow['verification_uri'])

result = app.acquire_token_by_device_flow(flow)

access_token_id = result['access_token']
headers = {'Authorization': 'Bearer ' + access_token_id}

endpoint = base_url + 'me'
response = requests.get(endpoint, headers=headers)
print('response:', response)
print(response.json())

