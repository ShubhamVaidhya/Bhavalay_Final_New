from rest_framework import generics
from .models import Referral
from .serializers import ReferralSerializer

class ReferralListCreateView(generics.ListCreateAPIView):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
