import logging
import asyncio
import os
from hbmqtt.broker import Broker

config_path = os.path.join(os.getcwd(), 'config.yaml')


@asyncio.coroutine
def broker_coro():
    broker = Broker(config_path)
    yield from broker.start()


if __name__ == '__main__':
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(broker_coro())
    asyncio.get_event_loop().run_forever()