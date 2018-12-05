from pprint import pprint

from django.urls import reverse

from api.models import Post, PostLike


class TestPostsAPI:

    def test_post_auth(self, apiclient):
        response = apiclient.post(
            reverse('post-list'),
            data={
                "content": "Thank u, next"
            }
        )
        assert response.status_code == 401

    def test_posted(self, auth_apiclient):
        response = auth_apiclient.post(
            reverse('post-list'),
            data={
                "content": "Like a river flow, surely to the sea."
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data.get('content') == "Like a river flow, surely to the sea."
        assert data.get('id') == Post.objects.first().id

        first_id = data.get('id')

        # DRY
        response = auth_apiclient.post(
            reverse('post-list'),
            data={
                "content": "hey 2"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data.get('content') == 'hey 2'
        assert data.get('id') == Post.objects.exclude(id=first_id)[0].id

    def test_post_valid(self, auth_apiclient):
        response = auth_apiclient.post(
            reverse('post-list'),
            data={
                "content": ""
            }
        )
        assert response.status_code == 400

    def test_post_valid2(self, auth_apiclient):

        response = auth_apiclient.post(
            reverse('post-list'),
            data={

            }
        )
        assert response.status_code == 400

    def test_post_pagination(self, auth_apiclient, user):

        for i in range(0, 20):

            Post.objects.create(
                user=user,
                content=str(i),


            )

        response = auth_apiclient.get(
            reverse('post-list'),
            data={

            }
        )

        assert len(response.json()['posts']) == 12

    def test_post_pagination_with_id(self, auth_apiclient, user):

        for i in range(0, 20):

            Post.objects.create(
                user=user,
                content=str(i),



            )

        last_post = Post.objects.create(
            user=user,
            content='-1',


        )
        response = auth_apiclient.get(
            reverse(
                'post-list',
            ) + '?cursor_id=%s' % last_post.id,
        )
        # post = response.json()['posts']
        # pprint(post)
        assert response.json()['posts'][0]['id'] == (last_post.id - 1)

    def test_post_pagination_with_id_remain(self, auth_apiclient, user):

        old_post = Post.objects.create(
            user=user,
            content='-1',

        )

        for i in range(0, 20):

            Post.objects.create(
                user=user,
                content=str(i)
            )

        response = auth_apiclient.get(
            reverse(
                'post-list',
            ) + '?cursor_id=%s' % (old_post.id + 1),
        )
        assert response.json()['posts'][0]['id'] == old_post.id
        assert len(response.json()['posts']) == 1

    def test_no_post(self, auth_apiclient):

        response = auth_apiclient.get(
            reverse(
                'post-list',
            ),
        )

        assert len(response.json()['posts']) == 0


def like(auth_apiclient, post):
    return auth_apiclient.post(
        reverse(
            'post-like', args=(post.id,)
        )
    )


class TestPostLike:

    def test_like(self, auth_apiclient, post):

        response = like(auth_apiclient, post)
        assert response.status_code == 200
        assert PostLike.objects.count() > 0

    def test_like_twice(self, auth_apiclient, post):

        response = like(auth_apiclient, post)
        assert response.status_code == 200
        response = like(auth_apiclient, post)
        assert response.status_code == 400

    def test_unlike(self, auth_apiclient, post):
        response = like(auth_apiclient, post)

        assert response.status_code == 200

        response = auth_apiclient.delete(
            reverse(
                'post-like', args=(post.id,)
            )
        )

        assert response.status_code == 200

        assert PostLike.objects.count() == 0
