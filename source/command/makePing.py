import requests
from dotenv import load_dotenv
from os import environ

if load_dotenv(dotenv_path="./.env") != True:
    raise ValueError("cannot load dotenv")

applicationID = environ["APP_ID"]
token = environ["TOKEN"]

print(f"application id: {applicationID}")
print(f"token: {token}")

apiURL = "https://discord.com/api/v10"

createCmd = f"/applications/{applicationID}/commands"
getCmd = f"/applications/{applicationID}/commands"

# This is an example CHAT_INPUT or Slash Command, with a type of 1
json = {
    "name": "ping",
    "type": 1,
    "description": "Let's Ping-Pong",
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": f"Bot {token}"
}

r = requests.get(apiURL + getCmd, headers=headers)
print(f"status code: {r.status_code}")
print(r.content)