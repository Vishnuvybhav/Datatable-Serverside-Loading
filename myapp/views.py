from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import Q
from .models import Employee
from django.shortcuts import render
import json

from django.http import JsonResponse
from django.db.models import Q
from .models import Employee

def datatables_view(request):
    # Read parameters
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    # Read ordering parameters
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_direction = request.GET.get('order[0][dir]', 'asc')

    # Mapping of column index to model field name
    column_mapping = {
        0: 'first_name',
        1: 'last_name',
        2: 'position',
        3: 'office',
        4: 'start_date',
        5: 'salary'
    }

    # Get the corresponding model field name for the ordered column
    ordered_field = column_mapping.get(order_column_index, 'first_name')
    ordering = ordered_field if order_direction == 'asc' else f'-{ordered_field}'

    # Filtering
    query = Q()
    if search_value:
        query |= Q(first_name__icontains=search_value)
        query |= Q(last_name__icontains=search_value)
        query |= Q(position__icontains=search_value)
        query |= Q(office__icontains=search_value)

    if 'columns[0][search][value]' in request.GET:
        query &= Q(first_name__icontains=request.GET['columns[0][search][value]'])
    if 'columns[1][search][value]' in request.GET:
        query &= Q(last_name__icontains=request.GET['columns[1][search][value]'])
    if 'columns[2][search][value]' in request.GET:
        query &= Q(position__icontains=request.GET['columns[2][search][value]'])
    if 'columns[3][search][value]' in request.GET:
        query &= Q(office__icontains=request.GET['columns[3][search][value]'])
    if 'columns[4][search][value]' in request.GET:
        query &= Q(start_date__icontains=request.GET['columns[4][search][value]'])
    if 'columns[5][search][value]' in request.GET:
        query &= Q(salary__icontains=request.GET['columns[5][search][value]'])


    # Fetching data with ordering
    employees = Employee.objects.filter(query).order_by(ordering)
    total_records = employees.count()
    employees = employees[start:start+length]

    # Formatting data
    data = []
    for employee in employees:
        data.append([
            employee.first_name,
            employee.last_name,
            employee.position,
            employee.office,
            employee.start_date.strftime('%d-%m-%Y'),
            f"${employee.salary:,.2f}"
        ])

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)

# def column_search_view(request):
    
def index(request):
    return render(request, 'index.html')