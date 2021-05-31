import asyncio
import logging

import aiohttp
import random
import string


logger = logging.getLogger(__name__)


class User:
    """
     Client for simulating user behaviour handling server API.
     Token refreshed automatically.
     Username and password is necessary for refreshing token.
    """

    API_HOST = 'http://localhost/v1.0/'
    SIGNUP_URL = API_HOST + 'signup/'
    LOGIN_URL = API_HOST + 'token/'
    POST_URL = API_HOST + 'posts/'

    LIKE_URL = API_HOST + 'posts/{id}/like/'

    CONTENT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do 
                 eiusmod tempor incididunt ut labore et dolore magna aliqua.
                 Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
                 nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in 
                 reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
                 Excepteur sint occaecat cupidatat non proident, sunt in culpa qui 
                 officia deserunt mollit anim id est laborum."""

    _total_posts = []

    def __init__(self, session, username, password, max_posts=5, max_likes=5, token=None):
        """

        """

        self.username = username
        self.password = password
        self.session = session
        self.max_posts = max_posts
        self.max_likes = max_likes
        self.posts, self.likes = 0, 0
        self.token = token

    @staticmethod
    def __generate_string(length=8):
        return ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=length)
        )

    @classmethod
    async def generate(cls, session, **kwargs):
        """
        Generate's new random user.
        :param session:
        :param kwargs: All other user parameters
        :return:
        """
        user = User(
            session,
            username=User.__generate_string(),
            password=User.__generate_string(length=20),
            **kwargs
        )

        # return asyncio.ensure_future(user.signup())
        return await user.signup()

    def __exhausted_limit(self, attr):

        if getattr(self, attr) >= getattr(self, 'max_' + attr):
            logger.warning(f'Number of {attr} for user {self.username} exhausted')
            return True

        return False

    async def _token_lock(self):

        while not self.token:
            await asyncio.sleep(0.1)

        return True

    async def _request(self, method, url, auth_header=True, *args, **kwargs):

        exc = None
        # attempts for disconnect or token expiration.
        for i in range(10):

            if self.token:
                kwargs.setdefault('headers', {}).update(self._auth_header())

            try:
                async with self.session.request(method, url, *args, **kwargs) as response:

                    if response.status == 401:
                        if auth_header and not self.token:

                            # other tasks for that user most likely will get 401
                            # too, lock until new token issued.
                            # TODO: implement proper lock/pause
                            await self._token_lock()
                            continue
                        response.close()

                        self.token = None
                        await self._get_token()

                        continue
                    return await response.json(), response.status

            except aiohttp.ClientError as e:
                exc = e
                # print(f'{i} Server disconnect... Try again {url}')
        logger.error(f'Host error after {i} times: {exc}')
        raise Exception(f'Host error after {i} times: {exc}')

    def _auth_header(self):

        return {
            "Authorization": "Bearer %s" % self.token
        }

    async def _get_token(self):

        # we can load users from some file or external resources as example

        response, status = await self._request('POST', User.LOGIN_URL,
                                               auth_header=False,
                                               data={
                                                    "username": self.username,
                                                    "password": self.password
                                               })
        if status != 200:
            logger.warning('Error ', response)
            raise Exception('Invalid token')
        self.token = response['access']

    @property
    def left_likes(self):
        return self.max_likes - self.likes

    @property
    def left_posts(self):
        return self.max_posts - self.posts

    async def create_content(self, content=CONTENT):

        if self.__exhausted_limit('posts'):
            return

        post, status = await self._request('POST', User.POST_URL,
                                           data={"content": content})
        if status == 200:
            self.posts += 1
        return post

    async def like(self, post_id):
        if self.__exhausted_limit('likes'):
            return

        message, status = await self._request(
            'POST', User.LIKE_URL.format(id=post_id)
        )

        if status == 200:
            self.likes += 1

        return status

    async def signup(self):
        _, status = await self._request('POST', User.SIGNUP_URL,
                                        auth_header=False,
                                        data={
                                            "username": self.username,
                                            "password": self.password
                                        })

        if status != 200:
            raise Exception('signup failed')

        await self._get_token()
        return self

    async def generate_content(self):
        """
         Generate posts for amount of quota left
        :return:
        """
        # generate content
        if self.__exhausted_limit('posts'):
            return

        posts = await asyncio.gather(*[
            self.create_content(f"{self.username} content #{i}: {User.CONTENT} ")
            for i in range(self.left_posts)
        ])

        # save generated posts to not waste server resources.
        User._total_posts.extend(map(lambda i: i['id'], posts))

        return posts

    async def generate_likes(self):
        """

        Generate likes for amount of quota left
        :return:
        """
        if self.__exhausted_limit('likes') or not User._total_posts:
            return

        await asyncio.gather(*[

            self.like(pid)
            for pid in random.choices(User._total_posts, k=self.left_likes)
        ])

    async def simulate(self):
        """
        Let bot simulate fake behaviour with best scenario.
        :return:
        """

        # TODO: Declarative way of simulation
        await self.generate_content()
        await self.generate_likes()
