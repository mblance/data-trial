from django.test import TestCase
from django.db.models import Max
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_api.views import (
    message_api, user_api, api_subarray,
    api_array_response, create_from_request
)
from rest_api.models import User, Message


# Create your tests here.
class ModelTestCase(TestCase):

    def setUp(self):
        User.objects.create(username="Batman", password_hash="HASH1")
        User.objects.create(username="The Flash", password_hash="HASH1")
        User.objects.create(username="Kato", password_hash="HASH1")

        Message.objects.create(text="To the batmobile!", author_id="1")
        Message.objects.create(
            text="Things aren't always what they seem", author_id="2"
        )
        Message.objects.create(
            text="Want to see something cool?", author_id="3"
        )

    def test_view_functions(self):
        next_id = str(User.objects.aggregate(Max('id'))['id__max'] + 1)
        response = create_from_request(
            User,
            {"username": "Spider Man", "password_hash": "HASH2"}
        )
        self.assertEqual(response['id'], next_id)

        count = User.objects.count()

        subarray = api_subarray(User, '-1', count, '-username')
        print(subarray, User.objects.order_by('-username'))

        print(api_array_response(User, subarray, count))


class BaseAPITestCase(APITestCase):

    def test(self):
        for case in self.cases:
            response = self.client.post(
                self.url, case, format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        print('Successful Post Sample:', response.data)
        self.assertEqual(self.model.objects.count(), 15)

        response = self.client.get(self.url, format='json')
        print(
            'Default GET Sample:',
            response.data
        )

        response_data = self.client.get(
            self.url, {"vector": "-2", "index": "7"}, format='json'
        ).data
        self.assertEqual(
            response_data['total_length'], 15
        )
        print('Vectored GET Sample:', response_data['array'])
        self.assertEqual(
            len(response_data['array']), 2
        )

        response_data = self.client.get(
            self.url, {"vector": "0", "index": "7"}, format='json'
        ).data
        self.assertEqual(
            len(response_data['array']), 0
        )

        response_data = self.client.get(
            self.url, {"vector": "1"}, format='json'
        ).data
        self.assertEqual(
            len(response_data['array']), 1
        )

        response = self.client.get(
            self.url, {"index": "300"}, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

        print("******\n\n",
            self.client.get(
                self.url, {"vector": "-99", "index": "2", "sort": "timestamp"}, format='json'
            ).data
        )

        print("******\n\n",
            self.client.get(
                self.url, {"vector": "100", "index": "15", "sort": "timestamp"}, format='json'
            ).data
        )


class UserAPITestCase(BaseAPITestCase):

    def setUp(self):
        self.url = reverse(user_api)
        self.model = User
        self.cases = [
            {
                "username": f"test{i:02d}", "password_hash": f"test{i:02d}",
                "timestamp": f"2020-02-08T08:30:{i:02d}.135133Z"
            }
            for i in range(1, 16)
        ]

    def test(self):
        super().test()
        response_data = self.client.get(self.url, format='json').data
        self.assertEqual(
            [u['username'] for u in response_data['array']],
            [
                u.username
                for u in self.model.objects.order_by('-username')[5:15][::-1]
            ])
        response_data = self.client.get(
            self.url,
            {"vector": "-8", "index": "10", "sort": "timestamp"},
            format='json'
        ).data
        self.assertEqual(
            self.client.get(
                self.url,
                {"sort": "InvalidSort"},
                format='json'
            ).status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            [u['username'] for u in response_data['array']],
            [
                u.username
                for u in self.model.objects.order_by('timestamp')[11-8:10+1][::-1]
            ]
        )
        self.assertEqual(User.objects.first().username, 'test01')
        self.assertEqual(User.objects.first().password_hash, 'test01')
        self.assertEqual(
            self.client.post(
                self.url, {'username': 'test01'}, format='json'
            ).status_code,
            status.HTTP_409_CONFLICT
        )


class MessageAPITestCase(BaseAPITestCase):

    def setUp(self):
        self.url = reverse(message_api)
        self.model = Message
        self.cases = [
            {
                "author_id": f"{i:02d}", "text": f"Test Message {i:02d}",
                "timestamp": f"2020-02-08T08:30:{i:02d}.135133Z"
            }
            for i in range(1, 16)
        ]
