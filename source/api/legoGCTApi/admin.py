from django.contrib import admin
from .models import Einzelteil
from .models import Legoset
from .models import Anbieter, Einzelteilmarktpreis, UserSuchliste, EinzelteilLegoset, Setmarktpreis
# Register your models here.

admin.site.register(Einzelteil)
admin.site.register(Legoset)
admin.site.register(Anbieter)
admin.site.register(Einzelteilmarktpreis)
admin.site.register(UserSuchliste)
admin.site.register(EinzelteilLegoset)
admin.site.register(Setmarktpreis)
