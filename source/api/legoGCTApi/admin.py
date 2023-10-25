from django.contrib import admin
from .models import Einzelteil
from .models import Legoset
from .models import Anbieter
# Register your models here.

admin.site.register(Einzelteil)
admin.site.register(Legoset)
admin.site.register(Anbieter)
