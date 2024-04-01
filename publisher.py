import logging
import asyncio
from datetime import datetime
from amqtt.client import MQTTClient, ConnectException

logger = logging.getLogger(__name__)

# This sample shows how to publish messages to broker using different QOS
# Debug outputs shows the message flows


async def test_coro():
    try:
        current_datetime = datetime.now()
        current_datetime = str(current_datetime)
        C = MQTTClient()
        await C.connect("mqtt://0.0.0.0:1883")
        await C.publish("data/classified", b"TOP SECRET", qos=0x01)
        await C.publish("data/classified", b"ONLY Broker can see this!", qos=0x01)
        await C.publish("data/temperature", b"31 Celsius", qos=0x01)
        await C.publish("data/acceleration", b"3 KM/(H^2)", qos=0x01)
        await C.publish("data/speed", b"55 KM/H", qos=0x01)
        await C.publish("data/humidity", b"3%", qos=0x01)
        await C.publish("repositories/amqtt/master", b"BLE012181", qos=0x01)
        await C.publish(
            "repositories/amqtt/devel", b"THIS NEEDS TO BE CHECKED", qos=0x01
        )
        await C.publish("calendar/amqtt/releases", bytes(current_datetime, 'utf-8'), qos=0x01)
        logger.info("messages published")
        await C.disconnect()
    except ConnectException as ce:
        logger.error("Connection failed: %s" % ce)
        asyncio.get_event_loop().stop()


if __name__ == "__main__":
    formatter = (
        "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    )
    formatter = "%(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    asyncio.get_event_loop().run_until_complete(test_coro())
