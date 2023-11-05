import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from test.test import test  # noqa F401
from src.bot import start  # noqa F401


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    mongodb_url = 'mongodb://root:example@mongo:27017'
    client = AsyncIOMotorClient(mongodb_url)
    asyncio.run(test(client.salaries.sample_collection))
    # asyncio.run(start(client.salaries.sample_collection))
