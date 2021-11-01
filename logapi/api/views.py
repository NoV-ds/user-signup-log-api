from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import views
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.messages.api import error, success
from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER
from django.http.response import Http404
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, PasswordChangeSerializer, ForgetPasswordSerializer, UserSerializer
from .models import UserDetails
from .forms import userForm
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

# Create your views here.

def index(request):
    return render(request, 'index.html')

class Signup(APIView):
    def post(self, request, format=None):
        serializ = UserSerializer(data=request.data)
        if serializ.is_valid():
            user = serializ.save()
            token, created = Token.objects.get_or_create(user=request.user)
            return Response(serializ.data, {
                'token': str(token),
                'user_id': user.pk,
                'email': user.email
            },
            status=status.HTTP_201_CREATED)
        return Response(serializ.errors, status=status.HTTP_400_BAD_REQUEST)

class login(APIView):
    serializer_class = LoginSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=request.user)
                print(str(token))
                return Response({'token': str(token)}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class logout(APIView):
        permission_classes = (IsAuthenticated,)

        def get(self, request, format=None):
            """
                Remove all auth tokens owned by request.user.
            """
            tokens = Token.objects.filter(user=request.user)
            for token in tokens:
                token.delete()
            context = {'success': _('User logged out.')}
            return Response(context, status=status.HTTP_200_OK)

class ForgetPassword(APIView):
    serializer_class = ForgetPasswordSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            user = UserDetails.objects.filter(email=email)
            token = Token.objects.get_or_create(user)
            mail(email, token)
            context = {'email': email, 'token': token.key}
            return Response(context, status=status.HTTP_201_CREATED)

    def mail(email, token):
        Receiver = email
        Subject = "Password Reset"
        Message = "Click on the link to reset your password \n\n{}".format(token)
        return send_mail(Subject, Message, EMAIL_HOST_USER, [Receiver], fail_silently=False,)


class passwordChange(APIView):
    serializer_class = PasswordChangeSerializer
    permission_class = (IsAuthenticated)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            password = request.POST['password']
            user.set_password(password)
            user.save
            context = {'success':'Password changed'}
            return Response(context, status = status.HTTP_200_OK)
        else:
            return Response(serializer.error, status = status. HTTP_400_BAD_REQUEST)