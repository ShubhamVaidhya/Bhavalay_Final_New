from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE)
    referred_name = models.CharField(max_length=200)
    referred_mobile_number = models.CharField(max_length=17, unique=True)
    referral_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.referred_name
