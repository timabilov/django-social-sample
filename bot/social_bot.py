import argparse
import json
import random
import sys
from json import JSONDecodeError
from random import choice

import aiohttp
import asyncio

import uvloop

# uwsgi conf port used
API_URL = 'http://localhost/v1.0/'

generated_posts_id = []


CONTENT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do 
             eiusmod tempor incididunt ut labore et dolore magna aliqua.
             Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
             nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in 
             reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
             Excepteur sint occaecat cupidatat non proident, sunt in culpa qui 
             officia deserunt mollit anim id est laborum."""

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

args = vars(parser.parse_args())
RULES = args
# can read from args too.
if args.get('config-file'):
    try:
        with open(args.get('config-file')) as conf:
            try:
                data = json.load(conf)
            except JSONDecodeError as e:
                sys.exit(f'Error loading config.json: {e}')

            if any(
                type(v) is not int or v < 0 for v in data.values()
                if v in RULES.keys()
            ):
                sys.exit('ERROR: Values must be integer')

            RULES.update(data)
            print('Configuration loaded...')

    except FileNotFoundError:
        print('Skip bad file  configuration... Using args as default.')


print(RULES)


class User:
    def __init__(self, bot_id, session):
        self.username = f'verytrickybot{bot_id}'
        self.password = 'mydumbpassword'
        self.session = session
        self.token = None

    async def request(self, method, url, *args, **kwargs):

        # server drops connection so we use 20 attempts to not miss any req.
        exc = None
        for i in range(20):
            try:
                async with self.session.request(method, url, *args, **kwargs) as response:
                    return await response.json()

            except aiohttp.ClientError as e:
                exc = e
                # print(f'{i} Server disconnect... Try again {url}')

        sys.exit(f'Host error: {exc}')

    async def _create_content(self, content):
        return await self.request('POST', API_URL + 'posts/', headers={
            "Authorization": f"Bearer {self.token}"
        }, data={"content": content})

    async def get_token(self):

        # we can load users from some file or external resources as example

        await self.request('POST', API_URL + 'signup/',
                           data={"username": self.username,
                                 "password": self.password})

        response = await self.request('POST', API_URL + 'token/',
                                      data={"username": self.username,
                                            "password": self.password})
        self.token = response['access']

    async def process_content(self):

        # set token and start generating content immediately
        await self.get_token()

        # generate content
        posts = await asyncio.gather(*[
            asyncio.ensure_future(self._create_content(f"{self.username} content #{i}: {CONTENT} "))
            for i in range(0, random.randint(0, RULES['max_user_posts']))
        ])

        # save generated posts to not waste server resources.
        generated_posts_id.extend(map(lambda i: i['id'], posts))
        # print(f'{self.username} processed -> ', len(posts))

        return posts

    async def like_content(self):

        def generate_random(times):
            return map(lambda i: choice(generated_posts_id), range(times))

        await asyncio.gather(*[
            asyncio.ensure_future(
                self.request(
                    'POST', f'{API_URL}posts/{i}/like/',
                    headers={
                        "Authorization": f"Bearer {self.token}"
                    }
                ))
            for i in generate_random(random.randint(0, RULES['max_user_likes']))
        ])

        # print(f'Finished  {self.username}' , result)

    async def process(self):
        await self.get_token()
        await self.process_content()
        await self.like_content()


async def main():

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector()) as session:
        users = [User(i, session) for i in range(RULES['users'])]

        print('Generating content...')
        await asyncio.gather(*[
            asyncio.ensure_future(user.process_content())
            for user in users
        ])

        print('Content generated... %s posts ' % len(generated_posts_id))

        print('Start promoting content...')
        await asyncio.gather(*[
            asyncio.ensure_future(user.like_content())
            for user in users
        ])

        print('Content randomly liked...')


if __name__ == '__main__':
    # we can keep plain asyncio loop as well
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
