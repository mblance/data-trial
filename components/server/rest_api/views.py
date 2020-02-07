from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_api.models import UserSerializer, MessageSerializer, User, Message
from rest_framework import status
from django.db import IntegrityError


def create_from_request(model, data):
    """ 
        Create the instance from the request data, 
        return the dict containing 
    """
    instance = UserSerializer().create(data)
    instance.save()
    return {"id": str(instance.id)}

def api_subarray(model, vector, index, sort):
    """
        Return a slice of a sorted model, reversed if
        the vector is negative
    """
    return model.objects.order_by(sort)[abs(vector):index][::vector//abs(vector)]

def api_array_response_dict(serializer, instances, count):
    """
        Returns a response dict with the count of the array
        with a serialized subarray
    """
    return {
        'total_length': count, 
        'array': serializer(instances, many=True)
    }


@api_view(['GET', 'POST'])
def user_api(request):
    data = request.data
    if request.method == 'GET':
        count = User.objects.count()
        if count == 0:
            return Response({'total_len': 0, 'array': []})

        index, vector, sort = (
            data.get('index', count), data.get('vector', -10), data.get('sort', '-username')
        )
        if sort not in ('-username', 'timestamp'):
            raise ValueError('Specified sort is not available')

        return Response(
            api_array_response_dict(
                UserSerializer, api_subarray(User, vector, index, sort), count
            )
        )
    else:
        try:
            return Response(create_from_request(User, UserSerializer))
        except IntegrityError:
            return Response(
                {"error": "username is already in use"}, 
                status.HTTP_409_CONFLICT
            )

@api_view(['GET', 'POST'])
def message_api(request):
    data = request.data
    if request.method == 'GET':
        count = Message.objects.count()
        if count == 0:
            return Response({'total_length': 0, 'array': []})

        index, vector = data.get('index', count), data.get('vector', -10)
        return Response(
            api_array_response_dict(
                MessageSerializer, api_subarray(Message, vector, index, 'timestamp'), count
            )
        )
    else:
        return Response(
            create_from_request(Message, MessageSerializeer)
        )

