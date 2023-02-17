#  based on https://www.youtube.com/watch?v=1Jyd7SA-0kI&ab_channel=JieJenn
import webbrowser
import msal
import requests
from msal import PublicClientApplication

app_id = '5b719a7e-265e-4a9e-8679-2316153fbab9'
client_secret = 'OVo8Q~hSWof8_CIZ_9kX1gjlUXlFKF_y19WyYc02'
authority_url = 'https://login.microsoftonline.com/consumers/'
base_url = 'https://graph.microsoft.com/v1.0/'

scopes = ['User.Read', 'User.Export.All']

# Method 1: authentication with authorization code

client_instance = msal.ConfidentialClientApplication(
    client_id=app_id,
    client_credential=client_secret,
    authority=authority_url
)

authorization_request_url = client_instance.get_authorization_request_url(scopes)
print('authorization_request_url:', authorization_request_url, '\n')
webbrowser.open(authorization_request_url, new=True)  # find authorization_code from here, check url after code=...

authorization_code = 'M.R3_BAY.dc5129c2-18ec-3e68-1d7b-d7200722e618'

access_token = client_instance.acquire_token_by_authorization_code(
    code=authorization_code,
    scopes=scopes
)
print('access_token:', access_token, '\n')

access_token_id = access_token['access_token']
headers = {'Authorization': 'Bearer ' + access_token_id}

endpoint = base_url + 'me'
response = requests.get(endpoint, headers=headers)
print('response:', response)
print(response.json())

# Method 2: Login to acquire access_token



