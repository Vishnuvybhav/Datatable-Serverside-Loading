# myapp/views.py
# def department_datatables_view(request):
#     model_name = 'Department'
#     columns = ['name', 'manager', 'location']
#     return get_datatables_data(request, model_name, columns)


# myapp/urls.py
# from .views import department_datatables_view

# urlpatterns = [
#     path('employee/datatables/', employee_datatables_view, name='employee_datatables_view'),
#     path('department/datatables/', department_datatables_view, name='department_datatables_view'),
# ]



#  myapp/utils.py
# from django.http import JsonResponse
# from django.db.models import Q
# from django.apps import apps

# def get_datatables_data(request, model_name, columns):
#     Read parameters
#     draw = int(request.GET.get('draw', 1))
#     start = int(request.GET.get('start', 0))
#     length = int(request.GET.get('length', 10))
#     search_value = request.GET.get('search[value]', '')

#     Get the model class
#     model = apps.get_model('myapp', model_name)

#     Filtering
#     query = Q()
#     if search_value:
#         for column in columns:
#             query |= Q(**{f"{column}__icontains": search_value})

#     Fetching data
#     objects = model.objects.filter(query)
#     total_records = model.objects.count()
#     filtered_records = objects.count()
#     objects = objects[start:start+length]

#     Formatting data
#     data = []
#     for obj in objects:
#         row = []
#         for column in columns:
#             value = getattr(obj, column)
#             if hasattr(value, 'strftime'):  
#                 value = value.strftime('%d-%m-%Y')
#             elif isinstance(value, (int, float)): 
#                 value = f"${value:,.2f}"
#             row.append(value)
#         data.append(row)

#     response = {
#         'draw': draw,
#         'recordsTotal': total_records,
#         'recordsFiltered': filtered_records,
#         'data': data
#     }

#     return JsonResponse(response)
