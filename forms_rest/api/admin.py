import django.contrib.admin
import api.models

django.contrib.admin.site.register(api.models.Form)
django.contrib.admin.site.register(api.models.TextQuestion)
django.contrib.admin.site.register(api.models.RadioQuestion)
django.contrib.admin.site.register(api.models.CheckboxQuestion)
# Register your models here.
