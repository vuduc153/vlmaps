from aiohttp import web
from aiohttp_middlewares import cors_middleware
from aiohttp_middlewares.cors import DEFAULT_ALLOW_HEADERS
import re
import logging
import time
import json

from vlmaps.utils.llm_utils import parse_object_goal_instruction_with_scene_graph, parse_object_goal_description
from vlmaps.utils.prompt.template import DialoguePromptTemplate


async def parse_dialogue(request):

    try:
        json_msg = await request.json()
        message = DialoguePromptTemplate.build_prompt(json_msg['past'], json_msg['current'])
        logger.info("Prompt: \n" + message)
        result = parse_object_goal_instruction_with_scene_graph(message)
        logger.info("Result: \n" + result)
        
        if result:
            return web.json_response(json.loads(result))
        else:
            return web.json_response({"movements": []})
    
    except json.decoder.JSONDecodeError:
        logger.error("Invalid JSON payload from client")
        return web.Response(text="Invalid JSON payload", status=400)
    except KeyError as e:
        logger.error(f"KeyError: {str(e)}")
        return web.Response(text="Missing required fields in JSON", status=400)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return web.Response(text="Internal Server Error", status=500)


async def parse_description(request):

    try:
        json_msg = await request.json()
        message = json_msg['desc']
        logger.info("Description: \n" + message)
        result = parse_object_goal_description(message)
        logger.info("Result: \n" + result)
        
        if result:
            return web.json_response(json.loads(result))
        else:
            return web.json_response({"coordinate": []})
    
    except json.decoder.JSONDecodeError:
        logger.error("Invalid JSON payload from client")
        return web.Response(text="Invalid JSON payload", status=400)
    except KeyError as e:
        logger.error(f"KeyError: {str(e)}")
        return web.Response(text="Missing required fields in JSON", status=400)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return web.Response(text="Internal Server Error", status=500)


async def init():
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
    app.router.add_post('/parse', parse_dialogue)
    app.router.add_post('/parse_desc', parse_description)
    return app


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Server started")
    
    start = time.time()
    web.run_app(init(), host='0.0.0.0', port=43001)