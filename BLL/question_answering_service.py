import json
import requests
import asyncio
import websockets

from DAL.sqlite_dal import SQLiteDAL

class QuestionAnsweringService:
    def __init__(self, url, macaddress, db: SQLiteDAL):
        self.websocket = None
        self.url = url
        self.macaddress = macaddress
        self.token = self.load_local_token()
        self.db = db



    async def connect(self):
        self.websocket = await websockets.connect(self.url)

    async def authenticate(self):
        if not self.websocket:
            await self.connect()
        await self.websocket.send('{"Type": "mac","Message": "'+self.macaddress+'"}')
        response = await self.websocket.recv()

        repsonse_json = json.loads(response)
        
        self.db.execute_query('INSERT INTO token (value) VALUES (?)', (repsonse_json["Message"],))

    def load_local_token(self):
        token_record = self.db.get_record('SELECT * FROM token WHERE id = 1')
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
