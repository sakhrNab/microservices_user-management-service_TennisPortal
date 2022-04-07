from django.contrib import admin
from .models import EmailRequest

class EmailRequestAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone_number", "message"]


admin.site.register(EmailRequest, EmailRequestAdmin)