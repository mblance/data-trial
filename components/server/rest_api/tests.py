from django.test import TestCase
from django.db.models import Max
from rest_api.views import *
from rest_api.models import *

# Create your tests here.
class ModelTestCase(TestCase):

    def setUp(self):
        User.objects.create(username="Batman", password_hash="HASH1")
        User.objects.create(username="The Flash", password_hash="HASH1")
        User.objects.create(username="Kato", password_hash="HASH1")

        Message.objects.create(text="To the batmobile!", author_id="1")
        Message.objects.create(text="Things aren't always what they seem", author_id="2")
        Message.objects.create(text="Want to see something cool?", author_id="3")

    def test_view_functions(self):
        
        next_id = str(User.objects.aggregate(Max('id'))['id__max'] + 1)
        response = create_from_request(User, UserSerializer, {"username": "Spider Man", "password_hash": "HASH2"})
        self.assertEqual(response['id'], next_id)

        count = User.objects.count()

        subarray = api_subarray(User, -1, count, '-username')
        print(subarray, User.objects.order_by('-username'))

        print(api_array_response_dict(UserSerializer, subarray, count))


from rest_framework.test import APITestCase
from django.urls import reverse

class BaseAPITestCase(APITestCase):


    def test(self):
        response = self.client.get(self.url, format='json')

        for case in self.cases:
            response = self.client.post(self.url, case, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        print('Successful Post Sample:', response.data)
        self.assertEqual(self.model.objects.count(), 15)

        print('Default GET Sample:', self.client.get(self.url, format='json').data)

        response_data = self.client.get(self.url, {"vector": "-2", "index": "7"}, format='json').data
        self.assertEqual(
            response_data['total_length'], 15
        )
        print('Vectored GET Sample:', response_data['array'])
        self.assertEqual(
            len(response_data['array']), 5
        )

        response_data = self.client.get(self.url, {"vector": "0", "index": "7"}, format='json').data
        self.assertEqual(
            len(response_data['array']), 7
        )

        response_data = self.client.get(self.url, {"vector": "2"}, format='json').data
        self.assertEqual(
            len(response_data['array']), 13
        )

class UserAPITestCase(BaseAPITestCase):

    def setUp(self):
        self.url = reverse(user_api)
        self.model = User
        self.cases = [
            {"username": f"test{i:02d}", "password_hash": f"test{i:02d}"}
            for i in range(1, 16)
        ]

    def test(self):
        super().test()
        response_data = self.client.get(
            self.url, {"vector": "-0", "index": "10", "sort": "timestamp"}, format='json'
        ).data
        self.assertEqual(
            [u['username'] for u in response_data['array']],
            [u.username for u in self.model.objects.order_by('timestamp')[0:10][::-1]]
        )
        self.assertEqual(User.objects.first().username, 'test01') 
        self.assertEqual(User.objects.first().password_hash, 'test01')
        self.assertEqual(
            self.client.post(self.url, {'username': 'test01'}, format='json').status_code,
            status.HTTP_409_CONFLICT
        )


class MessageAPITestCase(BaseAPITestCase):

    def setUp(self):
        self.url = reverse(message_api)
        self.model = Message
        self.cases = [
            {"author_id": f"{i:02d}", "text": f"Test Message {i:02d}"}
            for i in range(1, 16)
        ]
