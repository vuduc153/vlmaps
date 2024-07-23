import asyncio
import websockets
import logging
import time
import os
import json
import hydra
from pathlib import Path
from omegaconf import DictConfig
from functools import partial

from vlmaps.utils.matterport3d_categories import mp3dcat
from vlmaps.utils.llm_utils import parse_spatial_instruction
from vlmaps.robot.api_robot import ApiRobot


async def parse_speech(websocket, path, robot):

    logger.info("VLMaps server init")

    try:
        async for message in websocket:
            
            json_msg = json.loads(message)
            message  = json_msg['current']
            result_code = parse_spatial_instruction(message)

            if result_code is not None:
                logger.info(result_code)

                for line in result_code.split("\n"):
                    if line:
                        eval(line)

                await websocket.send(robot.get_formatted_goals())

    except json.decoder.JSONDecodeError:
        logger.error("Invalid message from Websocket client")
    except websockets.exceptions.ConnectionClosed:
        logger.info("Connection closed")

@hydra.main(
    version_base=None,
    config_path="../config",
    config_name="map_indexing_cfg.yaml",
)

def main(config: DictConfig):

    data_dir = Path(config.data_paths.vlmaps_data_dir)
    data_dirs = sorted([x for x in data_dir.iterdir() if x.is_dir()])
    robot = ApiRobot(config)
    robot.setup_scene(data_dirs[config.scene_id])

    robot.map._init_clip()
    robot.map.init_categories(mp3dcat[1:-1])
       
    robot.set_curr_pose((284, 94, 0)) # TODO: get pose from client interface

    start = time.time()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    package1_log = logging.getLogger('whisper_online')
    package1_log.setLevel(logging.DEBUG)
    logger = logging.getLogger(__name__)

    logger.info("Server started")
    partial_parse_speech = partial(parse_speech, robot=robot)
    start_server = websockets.serve(partial_parse_speech, 'localhost', 43007)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()