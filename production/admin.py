from django.contrib import admin

# Register your models here.
from .models import Employe,Legumineuse,Recolte,Section

admin.site.register(Employe)
admin.site.register(Legumineuse)
admin.site.register(Recolte)
admin.site.register(Section)