import asyncio
from getmac import get_mac_address as gma
from BLL.question_answering_service import QuestionAnsweringService

from DAL.sqlite_dal import SQLiteDAL


db = SQLiteDAL('database.db')


questionansweringservice = QuestionAnsweringService("wss://api.prøve.svendeprøven.dk/ws/r2d2device", gma(), db)


async def main():

    await questionansweringservice.authenticate()
    pass
asyncio.run(main())