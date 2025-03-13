from django.contrib import admin
from .models import NFCTag

@admin.register(NFCTag)
class NFCTagAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'balance', 'aanwezig', 'scanned_at')
    list_filter = ('aanwezig',)
    search_fields = ('uid', 'name')
