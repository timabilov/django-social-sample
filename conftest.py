import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from api.models import UserProfile, Post

TEST_USERNAME = 'miranda'
TEST_PASSWORD = 'miranda88'


@pytest.fixture
def user(db):
    return UserProfile.objects.create_user(
        first_name="Miranda Kerr",
        email="mir@mail.ru",
        username=TEST_USERNAME,
        ip='5.134.51.184',
        password=TEST_PASSWORD
    )


@pytest.fixture
def apiclient(db):
    return APIClient()


@pytest.fixture
def post(user):

    # Todo django factory boy handles this cases pretty well

    return Post.objects.create(
        content='Your API suck\'s',
        user=user
    )


@pytest.fixture
def auth_apiclient(apiclient, user):
    response = apiclient.post(reverse('token_obtain_pair'), {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    })

    apiclient.credentials(
        HTTP_AUTHORIZATION='Bearer %s' % response.json().get('access')
    )
    return apiclient
