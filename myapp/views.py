import datetime
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import Q
from .models import Employee
from django.shortcuts import render
import json

from django.http import JsonResponse
from django.db.models import Q
from .models import Employee
from faker import Faker

def datatables_view2(request, model, filter_criteria=None,exclude_columns=[]):
    try:
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        order_column_index = int(request.GET.get('order[0][column]', 0))
        order_direction = request.GET.get('order[0][dir]', 'asc')

        column_config = []
        print("model._meta.fields",model._meta.fields)
        for field in model._meta.fields:
            if field.name not in exclude_columns:
                print("field name",field.name)
                column_config.append({'field_name': field.name})

        id_column = column_config.pop(0)
        column_config.append(id_column)

        column_config.append({'field_name': 'actions', 'is_action_column': True})

        print("column_config",column_config)

        ordered_field = column_config[order_column_index]['field_name']
        print("ordered_field",ordered_field)
        ordering = ordered_field if order_direction == 'asc' else f'-{ordered_field}'

        query = Q()
        if search_value:
            for config in column_config:
                if config.get('is_action_column'):
                    continue
                field_name = config['field_name']
                query |= Q(**{f"{field_name}__icontains": search_value})

        for i, config in enumerate(column_config):
            if config.get('is_action_column'):
                continue
            column_search_value = request.GET.get(f'columns[{i}][search][value]', '')
            if column_search_value:
                field_name = config['field_name']
                query &= Q(**{f"{field_name}__icontains": column_search_value})

        if filter_criteria:
            query &= filter_criteria

        data_model = model.objects.filter(query).order_by(ordering)
        total_records = data_model.count()
        data_model = data_model[start:start + length]

        data = []
        for obj in data_model:
            row = {config['field_name']: getattr(obj, config['field_name']) for config in column_config if not config.get('is_action_column')}
            row['actions'] = f'''
                <button onclick="editRecord({obj.id})">Edit</button>
                <button onclick="deleteRecord({obj.id})">Delete</button>
            '''
            data.append(row)

        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
            'data': data,
            'columns': [{'data': config['field_name']} for config in column_config]
        }
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({'error': str(e)})

def datatables_view(request):
    filter_criteria = Q(first_name__iexact="John")
    return datatables_view2(request, Employee, filter_criteria,exclude_columns=['salary'])

def seed_data_view(request):
    fake = Faker()
    for _ in range(1000):

        obj = Employee.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            position = fake.job(),
            office = fake.company(),
            start_date = fake.date_this_decade(),
            salary = fake.random_int(min=20000, max=100000),
        )
        obj.save()

    return render(request, 'myapp/seed.html')

def index(request):
    return render(request, 'index.html')