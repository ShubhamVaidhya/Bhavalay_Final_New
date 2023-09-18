from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserVerifyOtpSerializer, SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import requests
from random import randint
from rest_framework.decorators import api_view
from .models import User

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

def send_otp(mobile, otp):
    url = f"https://control.msg91.com/api/v5/otp?template_id=64e46c81d6fc056a09428b84&mobile={mobile}&otp={otp}"

    payload = {}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authkey": "402924A9xeKSEJ3U64e46d64P1"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

# class UserRegistrationView(APIView):
#   def post(self, request, format=None):
#     serializer = UserRegistrationSerializer(data=request.data)
#     if serializer.is_valid():
#        otp = str(randint(1000, 9999))  # Generate a 4-digit OTP
#        serializer.validated_data['otp'] = otp  # Add OTP to the serialized data
#        added_mobile_number = "91"+serializer.validated_data["mobile_number"]
#        user = serializer.save()
#        token = get_tokens_for_user(user)
#        # Send OTP to the mobile number
#        send_otp(added_mobile_number, otp)
       
#        return Response({'token':token, 'msg':'Registration Received'}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def verify_otp(request):
#     if request.method == 'POST':
#         mobile_number = request.data.get('mobile_number')
#         otp = request.data.get('otp')

#         try:
#             serializer = UserVerifyOtpSerializer(data=request.data)
#             serializer.is_valid()
#             mobile_number_serial = serializer.validated_data.get('mobile_number')
#             otp_serial = serializer.validated_data.get('otp')

#             if mobile_number == mobile_number_serial and otp == otp_serial:
#                 # Retrieve the user object from the database based on mobile_number and otp

#                 print("yes reached if condition")

#                 try:
#                     user = User.objects.get(mobile_number=mobile_number,otp=otp)  # Assuming otp is unique in your User model
#                 except User.DoesNotExist:
#                     return Response({"status": "Invalid OTP or mobile number"}, status=status.HTTP_400_BAD_REQUEST)

#                 # Clear the OTP field
#                 user.otp = None
#                 user.save()

#                 return Response({"status": "OTP verified"}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"status": "Invalid OTP or mobile number"}, status=status.HTTP_400_BAD_REQUEST)

#         except User.DoesNotExist:
#             return Response({"status": "Invalid OTP or mobile number"}, status=status.HTTP_400_BAD_REQUEST)

#     # If the request method is not POST, you should return a response indicating the method is not allowed.
#     return Response({"status": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class UserLoginView(APIView):
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      id = User.objects.get(email=email)
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)

