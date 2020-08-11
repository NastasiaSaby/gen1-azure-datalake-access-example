import requests
import os
import logging

logging.basicConfig(level=logging.INFO)

#Get the token
data_for_token_request = {
    'grant_type':'client_credentials',
    'resource':'https://management.core.windows.net/', 
    'client_id':'<your-client-id>', 
    'client_secret':'<your-client-secret>'
}
token_response = requests.post(
    'https://login.microsoftonline.com/<your-tenant-id>/oauth2/token',
    data=data_for_token_request).\
    json()

token= token_response['access_token']

#List all the files in models
headers = {"Authorization": "Bearer " + token}
filesRequest = requests.get("https://<your-datalake-name>.azuredatalakestore.net/webhdfs/v1/path/to/your/models?op=LISTSTATUS", headers=headers)

resultFiles = filesRequest.json()

#List all the files in each model
for file in resultFiles["FileStatuses"]["FileStatus"]:
    logging.info("Model: " + file["pathSuffix"])

    headers = {"Authorization": "Bearer " + token}
    fileRequest = requests.get(
        "https://<your-datalake-name>.azuredatalakestore.net/webhdfs/v1/path/to/your/models/{}?op=LISTSTATUS".format(file["pathSuffix"]),
        headers=headers).json()

    for fileInside in fileRequest["FileStatuses"]["FileStatus"]:
        logging.info("Model: " + file["pathSuffix"] + ", file: " + fileInside["pathSuffix"])

        contentFile = requests.get(
            "https://<your-datalake-name>.azuredatalakestore.net/webhdfs/v1/path/to/your/models/{0}/{1}?op=OPEN".format(
                file["pathSuffix"], fileInside["pathSuffix"]),
            headers=headers)

        pathFile = "./data/models/{0}/{1}".format(file["pathSuffix"], fileInside["pathSuffix"])
        os.makedirs(os.path.dirname(pathFile), exist_ok=True)

        #For the model.pkl, we load and store them as bytes, whereas we load ans store the other files as string
        if fileInside["pathSuffix"] == "model.pkl":
            with open(pathFile, "wb") as f:
                logging.info(f.name)
                for chunk in contentFile.iter_content(chunk_size=8192):
                    f.write(chunk)
        else:
            with open(pathFile, "w") as f:
                logging.info(f.name)
                for chunk in contentFile.iter_content(chunk_size=8192):
                    f.write(chunk.decode())

        f.close()
