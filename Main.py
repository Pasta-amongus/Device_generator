import requests
import crayons
import asyncio
import json
import sys 


loop = asyncio.get_event_loop()

class Auth:
    def __init__(self):

       
        self.DAUNTLESS_TOKEN = "YjA3MGYyMDcyOWY4NDY5M2I1ZDYyMWM5MDRmYzViYzI6SEdAWEUmVEdDeEVKc2dUIyZfcDJdPWFSbyN+Pj0+K2M2UGhSKXpYUA=="

        self.ACCOUNT_PUBLIC_SERVICE = "https://account-public-service-prod03.ol.epicgames.com"
        self.OAUTH_TOKEN = f"{self.ACCOUNT_PUBLIC_SERVICE}/account/api/oauth/token"
        self.EXCHANGE = f"{self.ACCOUNT_PUBLIC_SERVICE}/account/api/oauth/exchange"
        self.DEVICE_CODE = f"{self.ACCOUNT_PUBLIC_SERVICE}/account/api/oauth/deviceAuthorization"
        self.DEVICE_AUTH_GENERATE = f"{self.ACCOUNT_PUBLIC_SERVICE}/account/api/public/account/" + "{account_id}/deviceAuth"

    def HTTPRequest(self, url: str, headers = None, data = None, method = None):

        if method == 'GET':
            response = requests.get(url, headers=headers, data=data)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=data)


        return response

    def get(self, url, headers=None, data=None):
        return self.HTTPRequest(url, headers, data, 'GET')

    def post(self, url, headers=None, data=None):
        return self.HTTPRequest(url, headers, data, 'POST')


    
    async def fetch_client_credentials(self):

        headers = {
            "Authorization": f"basic {self.DAUNTLESS_TOKEN}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "token_type": "eg1"
        }
        response = self.post(self.OAUTH_TOKEN, headers=headers, data=data)

        return response.json()

    async def get_device_code_session(self, credentials: dict):

        headers = {
            "Authorization": f"bearer {credentials['access_token']}",
        }
        data = {
            "prompt": "login"
        }
        response = self.post(self.DEVICE_CODE, headers=headers, data=data)

        return response.json()

   
    async def pre_authenticate(self):

        client_credentials = await self.fetch_client_credentials()
        if 'errorCode' in client_credentials:
            return False, client_credentials
        else:
            device_code_session = await self.get_device_code_session(client_credentials)
            if 'errorCode' in device_code_session:
                return False, device_code_session
            else:
                return True, device_code_session

  

with open('Auths.json', 'r', encoding='utf-8') as d:
    auths = json.load(d)


print('Generating Code')
device_code = Auth()
device_code_session = asyncio.run(device_code.pre_authenticate())

if device_code_session[0] == True:
        print(f'Log in to {device_code_session[1]["verification_uri_complete"]}')


        print('code generated')
        loop.create_task
else:
        print(f'An Error occurred')
        sys.exit()
#to do:
#add a feature to store auths in a jaon file
