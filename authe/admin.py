from django.contrib import admin

from .models import User
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

class PersonAdmin(admin.ModelAdmin):
    model = User
    
    def BE_AWARE_NO_WARNING_clear_tokens_and_delete(self, request, queryset):
        users = queryset.values("id")
        OutstandingToken.objects.filter(user__id__in=users).delete()
        queryset.delete()

    actions = ["BE_AWARE_NO_WARNING_clear_tokens_and_delete"]

admin.site.register(User)