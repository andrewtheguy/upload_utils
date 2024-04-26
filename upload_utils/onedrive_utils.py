import logging
import os
import requests
from msal import ConfidentialClientApplication,PublicClientApplication
#import settings
from msal_extensions import FilePersistence
from msal_extensions.token_cache import PersistedTokenCache
from pathlib import Path

logger = logging.getLogger(__name__)

class OneDriveUtils:
    
    def __init__(self,client_id):
        self.client_id = client_id

  

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
        secret_dir=os.path.join(home,".config","onedrive_utils_andrew")
        os.makedirs(secret_dir,exist_ok=True)
        cache_path=os.path.join(secret_dir,f"onedrive_token_cache_{client_id}.json")
        persistence = FilePersistence(cache_path)
        cache=PersistedTokenCache(persistence)
        self.cache=cache
        #print(accounts[0])
        #print(app.acquire_token_silent(scopes=scopes, account=accounts[0]))
        #exit(1)
     
    def get_access_token(self):
        authority_url = "https://login.microsoftonline.com/consumers"  # Or your tenant-specific endpoint
        scopes = ["https://graph.microsoft.com/.default"]

        app = PublicClientApplication(self.client_id, authority=authority_url, token_cache=self.cache)
        accounts = app.get_accounts()
        result = None
        if len(accounts) > 0:
            result = app.acquire_token_silent(scopes=scopes, account=accounts[0])
        if not result:
            result = app.acquire_token_interactive(scopes=scopes)
        if "access_token" not in result:
            raise result.get("error_description")
        #print(result)
        return result["access_token"]

    def get_headers(self):
        return {"Authorization": "Bearer " + self.get_access_token()}

    def upload(self,file_path,dest_path,skip_if_exists=False):
        if(skip_if_exists and self.file_exists(dest_path)):
            logger.info(f"File {dest_path} already exists, skipping upload")
            return
        
        headers = self.get_headers()
            
        #handle empty file
        if(os.path.getsize(file_path)==0):
            response = requests.put(f"https://graph.microsoft.com/v1.0/me/drive/items/root:{dest_path}:/content",
                                    headers=headers, data="")
            #print(response.text)
            response.raise_for_status()
            return

        mutation='''
{
"@microsoft.graph.conflictBehavior": "fail",
"description": "description",
"driveItemSource": { "@odata.type": "microsoft.graph.driveItemSource" },
"mediaSource": { "@odata.type": "microsoft.graph.mediaSource" }
}
    '''
        #print("access_token",access_token)
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
    print(one_drive.file_exists("/CHAFA.txt"))
    print(one_drive.upload("empty_file.txt",'/empty_file.txt'))
    print(one_drive.upload("README.md",'/chafa.txt'))
    #print(one_drive.upload("README.md",'/chafa.txt',skip_if_exists=True))
    print(one_drive.file_exists("/differencefdsfdss2.txt"))