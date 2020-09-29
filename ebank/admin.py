from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ebank.models import Profile, TempTransfer, Transfer, User


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(TempTransfer)
admin.site.register(Transfer)
