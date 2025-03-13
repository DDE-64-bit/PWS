from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import NFCTag
from .serializers import NFCTagSerializer


#/.../.../.../{uid}/
@api_view(['GET'])
def save_nfc_tag(request, uid):
    uid = uid.strip()  # Verwijder onbedoelde spaties

    if not uid:
        return Response({"error": "Geen UID ontvangen"}, status=status.HTTP_400_BAD_REQUEST)

    tag, created = NFCTag.objects.get_or_create(uid=uid)

    if created:
        return Response({
            "message": "UID opgeslagen",
            "data": NFCTagSerializer(tag).data
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            "message": "UID bestond al",
            "data": NFCTagSerializer(tag).data
        }, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def toggle_aanwezig(request, uid):
    """
    API-endpoint om de 'aanwezig' status van een NFC-tag te toggelen.
    """
    try:
        tag = NFCTag.objects.get(uid=uid)
        tag.aanwezig = not tag.aanwezig  # Toggle de status
        tag.save()

        return Response({
            "message": f"Aanwezigheid van {tag.name} is nu {'✅ Aanwezig' if tag.aanwezig else '❌ Afwezig'}",
            "data": NFCTagSerializer(tag).data
        }, status=status.HTTP_200_OK)

    except NFCTag.DoesNotExist:
        return Response({"error": "UID niet gevonden"}, status=status.HTTP_404_NOT_FOUND)