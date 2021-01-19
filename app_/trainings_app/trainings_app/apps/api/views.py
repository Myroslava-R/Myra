# from django.shortcuts import render

import json
from django.conf import settings
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT, db=0)

@api_view(['GET'])
def get_all(request, *args, **kwargs):
    if request.method == 'GET':
        items = {}
        for key in redis_instance.keys("*"):
            items[key.decode("utf-8")] = redis_instance.get(key)
        response = items
        return Response(response, status=200)

@api_view(['GET', 'PUT', 'DELETE'])
def item(request, *args, **kwargs):
	if request.method == 'GET':
		if kwargs['key']:
			value = redis_instance.get(kwargs['key'])
			if value:
				response = {'value': value,}
				return Response(response, status=200)
			else:
				response = {'value': None,}
				return Response(response, status=404)
	elif request.method == 'PUT':
		if kwargs['key']:
			new_value = json.loads(request.body)['new_value']
			if new_value:
				redis_instance.set(kwargs['key'], new_value)
				response = {'value': new_value,}
				return Response(response, status=200)
			else:
				response = {'value': None,}
				return Response(response, status=404)
	elif request.method == 'DELETE':
		if kwargs['key']:
			result = redis_instance.delete(kwargs['key'])
			response = {'value': None,}
			return Response(response, status=404)
