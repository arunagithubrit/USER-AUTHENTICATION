from rest_framework import generics, status
from rest_framework.response import Response
from .models import Registration
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail


class creation(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Send an email to the user with a link containing the refresh token
        self.send_verification_email(user.email, refresh_token)

        return Response({'access_token': access_token,
                         'message': 'User registered successfully. Check your email for verification.'},
                        status=status.HTTP_201_CREATED)

    def send_verification_email(self, email, refresh_token):
        subject = 'Account Verification'
        message = f'Click the following link to verify your account:http://127.0.0.1:8000/verify/{refresh_token}'
        from_email = 'vishnudemo608@gmail.com'
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)
        # Implement email sending logic here (e.g., using Django's send_mail function)


from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


class EmailVerification(generics.GenericAPIView):
    def get(self, request, token):
        refresh_token = RefreshToken(token)
        user_id = refresh_token.payload['user_id']
        user = get_object_or_404(Registration, id=user_id)

        if user.is_verified == 0:
            user.is_verified = 1  # Set is_verified to 1 when the email is verified
            user.save()
            

            return Response({'message': 'Email verification successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)
        
