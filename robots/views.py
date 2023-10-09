import json
from datetime import datetime, timedelta
from http import HTTPMethod, HTTPStatus
from io import BytesIO
from itertools import groupby

from django.core.exceptions import ValidationError
from django.db.models import Count
from django.http import FileResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render
from openpyxl.styles import Font
from openpyxl.workbook import Workbook
from openpyxl.writer.excel import save_virtual_workbook

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


def week_production_volume_stats(request):
    if request.method not in (HTTPMethod.GET, HTTPMethod.POST):
        return HttpResponseNotAllowed([HTTPMethod.GET, HTTPMethod.POST])

    week_ago_datetime = datetime.now() - timedelta(weeks=1)
    week_sales = (Robot.objects
                  .filter(created__gte=week_ago_datetime)
                  .values('model', 'version')
                  .annotate(prod_count=Count('*'))
                  .order_by('model'))
    grouped_models = {key: list(group) for key, group in groupby(week_sales, lambda row: row['model'])}

    workbook = _create_excel_workbook(grouped_models)
    workbook_stream = BytesIO(save_virtual_workbook(workbook))
    return FileResponse(workbook_stream, as_attachment=True, filename='robots-week-production.xlsx')


def _create_excel_workbook(data):
    workbook = Workbook()
    workbook.remove(workbook.active)

    bold_font = Font(bold=True)
    for model, rows in data.items():
        worksheet = workbook.create_sheet(model)
        worksheet.append(('Модель', 'Версия', 'Количество за неделю'))
        for cell in worksheet[1]:
            cell.font = bold_font

        for row in rows:
            worksheet.append(tuple(row.values()))
    workbook.close()
    return workbook
