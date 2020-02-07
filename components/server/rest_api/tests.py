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
        response = create_from_request(User, {"username": "Spider Man", "password_hash": "HASH2"})
        self.assertEqual(response['id'], next_id)

        count = User.objects.count()

        subarray = api_subarray(User, -1, count, '-username')
        print(subarray, User.objects.order_by('-username'))

        print(api_array_response_dict(UserSerializer, subarray, count))

