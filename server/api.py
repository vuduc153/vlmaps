import asyncio
import websockets
import logging
import time
import os
import json
import hydra
from aiohttp import web
from aiohttp_middlewares import cors_middleware
from aiohttp_middlewares.cors import DEFAULT_ALLOW_HEADERS
import re
import json
from pathlib import Path
from omegaconf import DictConfig
from functools import partial
from vlmaps.utils.matterport3d_categories import mp3dcat
from vlmaps.utils.llm_utils import parse_object_goal_dialogue
from vlmaps.robot.api_robot import ApiRobot


async def parse(request, robot):

    logger.info("VLMaps server init")

    try:
        json_msg = await request.json()
        pose, past, current = json_msg['pose'], json_msg['past'], json_msg['current']
        
        vlmaps_pose = robot.transform_ros_pose_to_vlmaps_pose(pose)
        robot.set_curr_pose(vlmaps_pose)

        llm_input = f"""
            <dialogue_history>
            {past}
            </dialogue_history>
            <current_conversation>
            {current}
            </current_conversation>
        """

        logger.info(llm_input)

        llm_output = parse_object_goal_dialogue(llm_input)

        llm_output = json.loads(llm_output)
        goals = [action['target']['descriptor'] for action in llm_output['actions'] if action['actor'] == 'A']
        
        if goals:
            logger.info(goals)

            for goal in goals:
                eval(f"robot.move_to_object('{goal}')")

            return web.json_response(robot.get_formatted_goals())

        return web.json_response({"movements": []})

    except json.decoder.JSONDecodeError:
        logger.error("Invalid message from Websocket client")
    except KeyError as e:
        logger.error(f"KeyError: {str(e)}")
        return web.Response(text="Missing required fields in JSON", status=400)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return web.Response(text="Internal Server Error", status=500)


async def init(func):
    # app = web.Application(
    #     middlewares=[
    #         cors_middleware(
    #             origins=[re.compile(r"^https?\:\/\/localhost")]
    #         )
    #     ]
    # )
    # Unsecure config
    app = web.Application(
        middlewares=[cors_middleware(allow_all=True)]
    )
    app.router.add_post('/parse', func)
    return app


@hydra.main(
    version_base=None,
    config_path="../config",
    config_name="map_indexing_cfg.yaml",
)

def main(config: DictConfig):

    data_dir = Path(config.data_paths.vlmaps_data_dir)
    data_dirs = sorted([x for x in data_dir.iterdir() if x.is_dir()])
    robot = ApiRobot(config, vis=False)
    robot.setup_scene(data_dirs[0])

    robot.map._init_clip()
    robot.map.init_categories(mp3dcat[1:-1])

    partial_parse_func = partial(parse, robot=robot)
    web.run_app(init(partial_parse_func), host='0.0.0.0', port=43001)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Server started")

    main()