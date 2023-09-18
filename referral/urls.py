from django.urls import path
from .views import ReferralListCreateView

urlpatterns = [
    path('referrals/', ReferralListCreateView.as_view(), name='referral-list-create'),
    # Add other URLs as needed
]
