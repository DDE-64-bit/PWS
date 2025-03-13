from django.db import models

class NFCTag(models.Model):
    uid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, default="Onbekend")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    scanned_at = models.DateTimeField(auto_now_add=True)
    aanwezig = models.BooleanField(default=False)  # Nieuw veld

    def __str__(self):
        return f"{self.name} ({self.uid}) - €{self.balance} - {'Aanwezig' if self.aanwezig else 'Afwezig'}"
