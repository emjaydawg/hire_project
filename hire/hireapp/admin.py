from django.contrib import admin

from .models import Employee
from .models import Employer
from .models import Job

# Register your models here.
admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(Job)
