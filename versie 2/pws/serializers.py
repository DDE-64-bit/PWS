from rest_framework import serializers
from core.models import NFCTag

class NFCTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFCTag
        fields = ['uid', 'scanned_at']
