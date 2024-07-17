import asyncio
import websockets
import logging
import time
import os
import json

from vlmaps.utils.llm_utils import parse_object_goal_instruction_with_scene_graph
from vlmaps.utils.prompt.template import PromptTemplate


async def parse_speech(websocket, path):

    logger.info("VLMaps server init")

    try:
        async for message in websocket:
            
            json_msg = json.loads(message)
            message  = PromptTemplate.build_prompt(json_msg['past'], json_msg['current'])
            logger.info(message)
            result = parse_object_goal_instruction_with_scene_graph(message)
            if result is not None:
                logger.info(result)
                await websocket.send(result)

    except json.decoder.JSONDecodeError:
        logger.error("Invalid message from Websocket client")
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