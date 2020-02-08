from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_api.models import UserSerializer, MessageSerializer, User, Message
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.db import IntegrityError


def create_from_request(model, serializer, data):
    """ 
        Create the instance from the request data, 
        return the dict containing 
    """
    instance = serializer().create(data)
    instance.save()
    return {"id": str(instance.id)}

def api_subarray(model, vector, index, sort):
    """
        Return a slice of a sorted model, reversed if
        the vector is negative
    """
    step = {'-': -1}.get(vector[0], 1)
    start, stop = abs(int(vector)), int(index)
    return model.objects.order_by(sort)[start:stop][::step]

def api_array_response_dict(serializer, instances, count):
    """
        Returns a response dict with the count of the array
        with a serialized subarray
    """
    return {
        "total_length": count, 
        "array": serializer(instances, many=True).data
    }


@api_view(['GET', 'POST'])
def user_api(request):
    if request.method == 'GET':
        params = request.query_params
        count = User.objects.count()
        if count == 0:
            return Response({"total_len": 0, "array": []})

        index, vector, sort = (
            params.get('index', count), params.get('vector', '-10'), params.get('sort', '-username')
        )
        if sort not in ('-username', 'timestamp'):
            raise ValueError('Specified sort is not available')

        return Response(
            api_array_response_dict(
                UserSerializer, api_subarray(User, vector, index, sort), count
            )
        )
    else:
        data = request.data
        try:
            return Response(create_from_request(User, UserSerializer, data))
        except IntegrityError:
            return Response(
                {"error": "username is already in use"}, 
                status.HTTP_409_CONFLICT
            )

@api_view(['GET', 'POST'])
def message_api(request):
    if request.method == 'GET':
        params = request.query_params
        count = Message.objects.count()
        if count == 0:
            return Response({'total_length': 0, 'array': []})

        index, vector = params.get('index', count), params.get('vector', '-10')
        return Response(
            api_array_response_dict(
                MessageSerializer, api_subarray(Message, vector, index, 'timestamp'), count
            )
        )
    else:
        data = request.data
        return Response(create_from_request(Message, MessageSerializer, data))

