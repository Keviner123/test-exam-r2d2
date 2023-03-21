import json
import requests
import asyncio
import websockets

from DAL.file_dal import FileDAL

class QuestionAnsweringService:
    def __init__(self, url, macaddress, token_file: FileDAL):
        self.websocket = None
        self.url = url
        self.macaddress = macaddress
        self.token_file = token_file
        self.token = token_file.read()



    async def connect(self):
        self.websocket = await websockets.connect(self.url)

    async def authenticate(self):
        if not self.websocket:
            await self.connect()
        await self.websocket.send('{"Type": "mac","Message": "'+self.macaddress+'"}')
        response = await self.websocket.recv()

        repsonse_json = json.loads(response)
        
        response_token = repsonse_json["Message"]
        self.token_file.write(response_token)
        self.token = response_token

        

    def load_local_token(self):
        token_record = self.db.get_record('SELECT * FROM token WHERE id = 1')

        print(token_record[0])

        return token_record[0]


    def get_answer(self, question: str) -> str:

        url = "https://api.xn--prve-hra.xn--svendeprven-ngb.dk/api/question/device?question="+question

        payload={}
        headers = {
        'Authorization': 'Bearer '+self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload, timeout=60)
        response = json.loads(response.text)

        return response["answer"]
