from django.db import models
from django.conf import settings

class Shop(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shop')
    name = models.CharField(max_length=200)
    kra_pin = models.CharField(max_length=20, blank=True)
    logo_url = models.URLField(blank=True)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=16.00)
    vat_inclusive = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    mpesa_till = models.CharField(max_length=20, blank=True)
    mpesa_paybill = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self):
        return f"{self.shop.name} - {self.name}"
