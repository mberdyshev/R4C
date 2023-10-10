import json
from http import HTTPMethod, HTTPStatus

from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render

from robots.models import Robot


def create_robot(request):
    if request.method != HTTPMethod.POST:
        return HttpResponseNotAllowed([HTTPMethod.POST])
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return HttpResponseBadRequest('Invalid json')

    data['serial'] = f'{data.get("model")}-{data.get("version")}'
    try:
        instance = Robot.objects.create(**data)
    except ValidationError as e:
        return JsonResponse(e.message_dict, status=HTTPStatus.BAD_REQUEST)

    return JsonResponse(instance.id, safe=False, status=HTTPStatus.CREATED)
