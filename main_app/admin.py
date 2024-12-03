from django.contrib import admin
from .models import *

admin.site.register(Film)
admin.site.register(Producer)
admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Awards)
# admin.site.register(CustomUserManager)
admin.site.register(CustomUser)