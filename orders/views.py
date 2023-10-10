import json
from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.core.mail import send_mail
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


def send_email_awaiting(serial):
    orders = Order.objects.select_related().filter(robot_serial=serial)
    customer_emails = orders.values_list('customer__email', flat=True)
    if not customer_emails:
        return

    subject = f'В наличие поступил робот {serial}'
    message_body = ('Добрый день!\n' +
                    f'Недавно вы интересовались нашим роботом модели {serial[:2]}, версии {serial[-2:]}.\n' +
                    'Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.')
    send_mail(subject, message_body, None, customer_emails)

    orders.delete()
