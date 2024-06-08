from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} -- {self.location}'
class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    office = models.CharField(max_length=100)
    start_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

