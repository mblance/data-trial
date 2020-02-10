from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_api.models import User, Message
from rest_framework import status
from django.db import IntegrityError


def create_from_request(model, data):
    """
        Create the instance from the request data,
        return the dict containing the created id
    """
    instance = model(**data)
    instance.save()
    return {"id": str(instance.id)}


def api_subarray(model, vector, index: int, sort):
    """
        Return a slice of a sorted model, reversed if
        the vector is negative
    """
    if vector[0] == '-':
        stop, step = index + 1, -1
        start = max(stop + int(vector), 0)
    else:
        start, step = index, 1
        stop = int(vector) + start

    return model.objects.order_by(sort)[start:stop].values()[::-1]


def api_array_response(instances, count):
    """
        Returns a response with the count of the array
        with a serialized subarray
    """
    return Response({
        "total_length": count,
        "array": instances
    })

available_user_sorts = {'username': '-username', 'timestamp': 'timestamp'}
empty_response = Response({"total_length": 0, "array": []})
username_exists_error_response = Response(
    {"error": "username is already in use"},
    status.HTTP_409_CONFLICT
)
array_index_error_response = Response(
    {'error': 'array index is out of bounds'}, 
    status.HTTP_400_BAD_REQUEST
)

def response_body_get(model, vector, index, sort, count):
    index = int(index)
    if index >= count:
        return array_index_error_response
    return api_array_response(
            api_subarray(model, vector, index, sort), count
        )


@api_view(['GET', 'POST'])
def user_api(request):
    if request.method == 'GET':
        if (count := User.objects.count()) == 0:
            return empty_response

        params = request.query_params
        # Default the sorts to -username if an unavailable sort is specified
        sort = available_user_sorts.get(
            params.get('sort', 'username'), '-username'
        )
        return response_body_get(
            User, params.get('vector', '-10'), params.get('index', count - 1),
            sort, count
        )
    else:
        # For efficiency, attempt to insert into the database to save a query
        # Will also fail if required fields are not specified
        try:
            return Response(create_from_request(User, request.data))
        except IntegrityError:
            return username_exists_error_response


@api_view(['GET', 'POST'])
def message_api(request):
    if request.method == 'GET':
        if (count := Message.objects.count()) == 0:
            return empty_response

        params = request.query_params
        return response_body_get(
            Message, params.get('vector', '-10'), params.get('index', count - 1),
            'timestamp', count
        )
    else:
        return Response(
            create_from_request(Message, request.data)
        )
