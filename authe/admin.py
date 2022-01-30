from django.contrib import admin

from .models import User

from rest_framework_simplejwt import token_blacklist

class PersonAdmin(admin.ModelAdmin):
    model = User


class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want


admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)

admin.site.register(User)