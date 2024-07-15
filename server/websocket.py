import asyncio
import websockets
import logging
import time
import os

from vlmaps.utils.llm_utils import parse_spatial_instruction, parse_object_goal_instruction

async def parse_speech(websocket, path):

    logger.info("VLMaps server init")

    try:
        async for message in websocket:
            
            result = parse_spatial_instruction(message)
            if result is not None:
                await websocket.send(result)

    except websockets.exceptions.ConnectionClosed:
        logger.info("Connection closed")

start = time.time()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
package1_log = logging.getLogger('whisper_online')
package1_log.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Server started")
start_server = websockets.serve(parse_speech, 'localhost', 43007)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()