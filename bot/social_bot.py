import argparse
import json
import logging
import random

import sys
from json import JSONDecodeError

import aiohttp
import asyncio

import uvloop

from core import User

logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)
logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description='Behaviour rules')

# defaults
parser.add_argument('-u', '--users', dest='users', type=int,
                    help='Number of users to span', required=False,
                    default=40)
parser.add_argument('-p', '--max-posts', dest='max_user_posts', type=int,
                    help='Maximum number of random posts created by user',
                    default=20, required=False)
parser.add_argument('-l', '--max-likes', type=int, dest='max_user_likes',
                    help='Maximum number of random likes created by user',
                    default=20, required=False)

parser.add_argument('-f', '--config', type=str, dest='config-file',
                    help='Maximum number of random likes created by user',
                    required=False)


RULES = vars(parser.parse_args())


def load_config(path):
    try:
        with open(path) as conf:
            try:
                data = json.load(conf)
            except JSONDecodeError as e:
                sys.exit(f'Error loading {path}: {e}')

            if any(
                type(v) is not int or v < 0 for v in data.values()
                if v in RULES.keys()
            ):
                sys.exit('ERROR: Values must be integer')
            logger.info('Configuration loaded...')
            return data

    except FileNotFoundError:
        logger.warning('Skip bad file  configuration... Using args as default.')


if RULES.get('config-file'):
    RULES.update(load_config(RULES.get('config-file')))


logger.info(f'Rules:  {RULES}')


async def simulate_when_done(coro):
    user = await coro
    await user.simulate()
    return user


async def main():

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(force_close=True)) as session:

        logger.info('Start generating users...')
        tasks = [asyncio.ensure_future(User.generate(
            session,
            max_posts=random.randint(0, RULES['max_user_posts']),
            max_likes=random.randint(0, RULES['max_user_likes']),
        )) for _ in range(RULES['users'])]

        logger.info('Waiting for content generation...')
        # Start simulation right after release of each task
        await asyncio.gather(*[
            asyncio.ensure_future(simulate_when_done(awaited_user))
            for awaited_user in tasks
        ])

        logger.info('Simulation ended successfully...')

if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

