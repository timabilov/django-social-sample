import pytest
from django.urls import reverse


class TestRegistrationAPI:

    @pytest.mark.parametrize("cred, response_status", [
        (('',             ''), 400),
        (('',             'passwordstrong'), 400),
        (('foousername',  'passwordstrong'), 200),

        # auth validator
        (('goodusername', 'aaaaaaaa'), 400),
        (('goodusername', 'aa'), 400),
    ])
    def test_sample(self, cred, response_status, apiclient):

        response = apiclient.post(
            reverse('sign-up'),
            {
                "username": cred[0],
                "password": cred[1]
            }
        )

        assert response.status_code == response_status

    def test_exist(self, apiclient):
        response = apiclient.post(
            reverse('sign-up'),
            {
                "username": "robert",
                "password": "juniorfoo"
            }
        )

        assert response.status_code == 200

        assert apiclient.post(
            reverse('sign-up'),
            {
                "username": "robert",
                "password": "juniorfoo"
            }
        ).status_code == 400
