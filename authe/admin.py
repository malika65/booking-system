from django.contrib import admin

from .models import User

class PersonAdmin(admin.ModelAdmin):
    model = User
    def has_delete_permission(self, request, obj=None):
        return True

admin.site.register(User)