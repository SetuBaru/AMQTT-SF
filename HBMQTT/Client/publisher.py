import logging
import asyncio
from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

logger = logging.getLogger(__name__)


@asyncio.coroutine
def test_coro():
    C = MQTTClient()
    yield from C.connect('mqtt://test.mosquitto.org/')
    tasks = [
        asyncio.ensure_future(C.publish('a/b', b'TEST MESSAGE WITH QOS_0')),
        asyncio.ensure_future(C.publish('a/b', b'TEST MESSAGE WITH QOS_1', qos=QOS_1)),
        asyncio.ensure_future(C.publish('a/b', b'TEST MESSAGE WITH QOS_2', qos=QOS_2)),
    ]
    yield from asyncio.wait(tasks)
    logger.info("messages published")
    yield from C.disconnect()


@asyncio.coroutine
def test_coro2():
    try:
        C = MQTTClient()
        ret = yield from C.connect('mqtt://test.mosquitto.org:1883/')
        message = yield from C.publish('a/b', b'TEST MESSAGE WITH QOS_0', qos=QOS_0)
        message = yield from C.publish('a/b', b'TEST MESSAGE WITH QOS_1', qos=QOS_1)
        message = yield from C.publish('a/b', b'TEST MESSAGE WITH QOS_2', qos=QOS_2)
        # print(message)
        logger.info("messages published")
        yield from C.disconnect()
    except ConnectException as ce:
        logger.error("Connection failed: %s" % ce)
        asyncio.get_event_loop().stop()



if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    asyncio.get_event_loop().run_until_complete(test_coro())
    asyncio.get_event_loop().run_until_complete(test_coro2())
