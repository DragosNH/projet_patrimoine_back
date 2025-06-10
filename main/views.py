# -*- coding: utf-8 -*-
from token import tok_name
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Construction, Model3D, AtticSkeleton
from .serializers import ConstructionSerializer, SignUpSerializer, Model3DSerializer, AtticSkeletonSerializer
from . import serializers
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from .utils import email_verification_token
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from .serializers import UserProfileSerializer
from django.core.mail import EmailMessage
from django.shortcuts import render
from django_rest_passwordreset.models import ResetPasswordToken
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.authentication import JWTAuthentication


def hello(request):
    return HttpResponse("Hello world!")

@api_view(['GET'])
def api(request):
    return Response({"message": "Welcome to the api"})

# View info
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def construction_list(request):
    constructions = Construction.objects.all()
    serializers = ConstructionSerializer(constructions, many=True)
    return Response(serializers.data)

# Sign up
@api_view(['POST'])
def signup_view(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = email_verification_token.make_token(user)

        verify_url = f"http://192.168.1.123/api/verify-email/{uid}/{token}/"

        html_message = f"""
            <html>
                <body style="color: #715D4C; font-family: Arial, sans-serif;">
                    <h2>Bienvenue sur <strong>Patrimoine en jeu</strong> !</h2>
                    <p>Merci pour votre inscription, {user.first_name}.</p>
                    <p>Votre nom d'utilisateur est : <strong>{user.username}</strong></p>
                    <p>Pour confirmer votre adresse e-mail, cliquez sur le bouton ci-dessous :</p>

                    <p style="margin: 20px 0;">
                        <a href="{verify_url}" style="background-color: #715D4C; color: #FAFAFA; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                            Confirmer mon inscription
                        </a>
                    </p>

                    <p>Si vous n'avez pas créé de compte, ignorez simplement ce message.</p>
                    <p>Cordialement,<br>L'équipe <strong>Patrimoine en jeu</strong></p>

                    <div style="margin-top: 30px;">
                        <img src="https://i.imgur.com/uK7CvDZ.png" alt="Logo Patrimoine en jeu" width="150" style="margin-bottom: 20px;">
                    </div>
                </body>
            </html>
        """

        email = EmailMessage(
            subject = 'Confirmez votre inscription',
            body = html_message,
            from_email = 'Patrimoine en jeu <patrimoine.en.jeu@gmail.com>',
            to=[user.email]
        )
        email.content_subtype = 'html'
        email.send()

        return Response({"message": "Compte créé avec succès. Vérifiez votre e-mail pour activer votre compte."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username = username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh' : str(refresh),
            'access': str(refresh.access_token),
        })
    return Response ({'error': 'Invalid credentals'}, status=401)


# Logout
@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "D\u00e9connexion r\u00e9ussie"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

# Verify email
@api_view(['GET'])
def verify_email(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None 

    if user and email_verification_token.check_token(user, token):
        user.is_verified = True
        user.save()
        return render(request, 'main/email_verified.html')
    else:
        return render(request, 'main/email_invalid.html')


# Delete user
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        password = request.data.get('password')
        user = request.user

        if not user.check_password(password):
            return Response({'error': "Le mot de passe n'est pas correct."}, status=400)

        user.delete()
        return Response({'message': 'Compte supprimé avec succès'}, status=200)


class UserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# Reset password
def reset_password_page(request):
    token_key = request.GET.get('token')

    if not token_key:
        return render(request, 'main/reset_password_invalid.html')  

    try:
        token = ResetPasswordToken.objects.get(key=token_key)
    except ResetPasswordToken.DoesNotExist:
        return render(request, 'main/reset_password_invalid.html')  

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'main/reset_password_form.html', {
                'error': 'Les mots de passe ne correspondent pas.',
                'token': token_key
            })

        user = token.user
        user.password = make_password(password)
        user.save()

        token.delete()

        return render(request, 'main/reset_password_success.html')

    return render(request, 'main/reset_password_form.html', {'token': token_key})


class Model3DViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Model3D.objects.all()
    serializer_class = Model3DSerializer
    permission_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class Model3DDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            m = Model3D.objects.get(pk=pk)
        except Model3D.DoesNotExist:
            raise Http404("Model not found")

        return FileResponse(
            m.file.open('rb'),
            content_type='application/octet-stream',
            headers={'Content-Disposition': f'attachment; filename="{m.file.name}"'}
        )

class AtticSkeletonViewSet(viewsets.ModelViewSet):
    queryset = AtticSkeleton.objects.all()
    serializer_class = AtticSkeletonSerializer