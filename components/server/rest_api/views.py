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


def api_subarray(model, vector, index, sort):
    """
        Return a slice of a sorted model, reversed if
        the vector is negative
    """
    step = {'-': -1}.get(vector[0], 1)
    start, stop = abs(int(vector)), int(index)

    return model.objects.order_by(sort).values()[start:stop][::step]


def api_array_response_dict(instances, count):
    """
        Returns a response dict with the count of the array
        with a serialized subarray
    """
    return {
        "total_length": count,
        "array": instances
    }


available_user_sorts = {'username': '-username', 'timestamp': 'timestamp'}
empty_response = Response({"total_length": 0, "array": []})
username_exists_error_response = Response(
    {"error": "username is already in use"},
    status.HTTP_409_CONFLICT
)


@api_view(['GET', 'POST'])
def user_api(request):
    if request.method == 'GET':
        params = request.query_params
        if (count := User.objects.count()) == 0:
            return empty_response

        index, vector = params.get('index', count), params.get('vector', '-10')

        # Default the sorts to -username if an unavailable sort is specified
        sort = available_user_sorts.get(
            params.get('sort', 'username'), '-username'
        )

        return Response(
            api_array_response_dict(
                api_subarray(User, vector, index, sort), count
            )
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
        params = request.query_params
        if (count := Message.objects.count()) == 0:
            return empty_response

        index, vector = params.get('index', count), params.get('vector', '-10')
        return Response(
            api_array_response_dict(
                api_subarray(Message, vector, index, 'timestamp'),
                count
            )
        )
    else:
        return Response(
            create_from_request(Message, request.data)
        )
