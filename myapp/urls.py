# myapp/urls.py
from django.urls import path
from .views import datatables_view

urlpatterns = [
    path('datatables/', datatables_view, name='datatables_view')
]