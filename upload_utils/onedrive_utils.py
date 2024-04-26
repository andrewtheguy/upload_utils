import os
import requests
from msal import ConfidentialClientApplication,PublicClientApplication
#import settings
from msal_extensions import FilePersistence
from msal_extensions.token_cache import PersistedTokenCache
from pathlib import Path
class OneDriveUtils:
    
    def __init__(self,client_id):
        self.client_id = client_id

        authority_url = "https://login.microsoftonline.com/consumers"  # Or your tenant-specific endpoint
        scopes = ["https://graph.microsoft.com/.default"]


#client_id = settings.config['ONEDRIVE_CLIENT_ID']


# app = ConfidentialClientApplication(client_id, authority=authority_url,
#                                     client_credential=client_secret)

# result = app.acquire_token_for_client(scopes=scopes)
# if "access_token" not in result:
#     raise ValueError(result.get("error_description"))
# print(result)
# access_token = result['access_token']
# print(access_token)

#public client
        scopes = ["Files.ReadWrite"]

        home = str(Path.home())
        cache_path=os.path.join(home,".cache",f"onedrive_token_cache_{client_id}.json")
        os.makedirs(os.path.join(home,".cache"),exist_ok=True)
        persistence = FilePersistence(cache_path)
        cache=PersistedTokenCache(persistence)
        app = PublicClientApplication(client_id, authority=authority_url, token_cache=cache)
        accounts = app.get_accounts()
        #print(accounts[0])
        #print(app.acquire_token_silent(scopes=scopes, account=accounts[0]))
        #exit(1)
        result = None
        if len(accounts) > 0:
            result = app.acquire_token_silent(scopes=scopes, account=accounts[0])
        if not result:
            result = app.acquire_token_interactive(scopes=scopes)
        if "access_token" not in result:
            raise result.get("error_description")
        #print(result)
        self.access_token=result["access_token"]


    def get_headers(self):
        return {"Authorization": "Bearer " + self.access_token}

    def upload(self,file_path,dest_path):
        mutation='''
{
"@microsoft.graph.conflictBehavior": "fail",
"description": "description",
"driveItemSource": { "@odata.type": "microsoft.graph.driveItemSource" },
"mediaSource": { "@odata.type": "microsoft.graph.mediaSource" }
}
    '''
        #print("access_token",access_token)
        headers = self.get_headers()
        response = requests.post(f"https://graph.microsoft.com/v1.0/me/drive/items/root:{dest_path}:/createUploadSession",
                                headers=headers, json={"query": mutation})
        #print(response.text)
        response.raise_for_status()
        upload_url = response.json()["uploadUrl"]

        with open(file_path, 'rb') as f:
            resp=requests.put(upload_url, data=f)
            resp.raise_for_status()
            

    def file_exists(self,dest_path):

        #print("access_token",access_token)
        headers = self.get_headers()
        response = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/items/root:{dest_path}",
                                headers=headers)
        resp=response.json()
        if resp.get("error") and resp["error"]["code"]=="itemNotFound":
            return False
        response.raise_for_status()
        return True
            
        


if __name__ == "__main__":
    one_drive = OneDriveUtils(os.environ['ONEDRIVE_CLIENT_ID'])
    print(one_drive.upload("test.log",'chafa.txt'))
    print(one_drive.file_exists("/differencefdsfdss2.txt"))