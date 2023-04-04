from django.contrib import admin

from .models import Profile

regs = [Profile]

admin.site.register(regs)