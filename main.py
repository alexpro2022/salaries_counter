import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from test.test import test  # noqa F401
from src.bot import start  # noqa F401


async def main():
    logging.basicConfig(level=logging.INFO)
    mongodb_url = 'mongodb://root:example@mongo:27017'
    client = AsyncIOMotorClient(mongodb_url)
    await test(client.salaries.sample_collection)
    await start(client.salaries.sample_collection)

if __name__ == '__main__':
    asyncio.run(main())
