from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import RegisterUserSerializer, UserSerializer, UserRetrieveSerializer
from users.emails.emails import WelcomeEmail
from users.models import User
from subscriptions.lib.PaymentService import PaymentService
from subscriptions.lib.StripeOperator import StripeOperator


class ManageUserView(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveUserProfileView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self) -> User:
        pk = self.kwargs.get('pk')
        return get_object_or_404(User, pk=pk)


class CustomUserCreateView(APIView):
    """
    post:
    Takes an user email, first_name, last_name and password.
    Returns user's data if everything is OK or raises 400 Bad Request.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                PaymentService(StripeOperator()).createCustomer(user)
                if user:
                    WelcomeEmail().create_welcome_email(user).send()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlackListTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(data={'message': 'OK'}, status=status.HTTP_204_NO_CONTENT)
        except TokenError as error:
            return Response(data={'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
