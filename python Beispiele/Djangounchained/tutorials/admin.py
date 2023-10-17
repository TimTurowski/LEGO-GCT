from django.contrib import admin
from .models import Anbieter
from .models import Einzelteil
from .models import Einzelteilmarktpreis
from .models import EinzelteilLegoset
from .models import Legoset
from .models import Setmarktpreis

admin.site.register(Anbieter)
admin.site.register(Einzelteil)
admin.site.register(Einzelteilmarktpreis)
admin.site.register(EinzelteilLegoset)
admin.site.register(Legoset)
admin.site.register(Setmarktpreis)
