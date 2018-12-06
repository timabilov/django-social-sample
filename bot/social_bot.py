import json
import random
import sys
from random import choice

import aiohttp
import asyncio

import uvloop

# uwsgi conf port used
API_URL = 'http://localhost/v1.0/'

generated_posts_id = []

# default
RULES = {
  "users": 40,
  "max_user_posts": 20,
  "max_user_likes": 20
}

try:
    with open('config.json') as conf:
        data = \
            json.load(conf)
        if any(type(v) is not int or v < 0 for v in data.values()):
            print('ERROR: Values must be integer')
            sys.exit(1)
        RULES.update(data)
        print('Configuration loaded...')

except FileNotFoundError:
    print('Skipped file(config.json) configuration... Using defaults.', RULES)


class User:
    def __init__(self, bot_id, session):
        self.username = f'verytrickybot{bot_id}'
        self.password = 'mydumbpassword'
        self.session = session
        self.token = None

    async def request(self, method, url, *args, **kwargs):

        # server drops connection so we use 10 attempts to not miss any req.
        for i in range(10):
            try:
                async with self.session.request(method, url, *args, **kwargs) as response:
                    return await response.json()

            except aiohttp.ClientError:
                pass
                # print(f'{i} Server disconnect... Try again {url}')

        print('Server timeout..')
        sys.exit(1)

    async def _create_content(self, content):
        return await self.request('POST', API_URL + 'posts/', headers={
            "Authorization": f"Bearer {self.token}"
        }, data={"content": content})

    async def get_token(self):

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
            asyncio.ensure_future(self._create_content(f"{self.username} content # {i} "))
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
