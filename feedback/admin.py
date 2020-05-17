from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Department)
admin.site.register(Feedback)
admin.site.register(Batches)