from django.contrib import admin
from .models import Containers, Position, Trash
# Register your models here.

admin.site.register(Containers)
admin.site.register(Position)
admin.site.register(Trash)

