import json
from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render

from customers.models import Customer
from orders.models import Order


def test_create_customer_orders(request):
    data = json.loads(request.body)

    try:
        customer, _ = Customer.objects.get_or_create(email=data['email'])
        order, _ = Order.objects.get_or_create(robot_serial=data['serial'], customer=customer)
    except ValidationError as e:
        return JsonResponse(e.message_dict, status=HTTPStatus.BAD_REQUEST)

    return JsonResponse(order.id, safe=False, status=HTTPStatus.CREATED)
