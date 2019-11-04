from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework import status
from core.serializers import RegistrationSerializer, ActivationSerializer, OilFieldBuySerializer, OilFieldSerializer, \
    OilFieldSetForSaleSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models import OilField, User
from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html')


class UserRegistration(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status=status.HTTP_200_OK)


class UserOilFieldsList(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OilFieldSerializer

    def get(self, request):
        oil_fields = OilField.objects.filter(owner=request.user)
        serializer = self.serializer_class(oil_fields, many=True)
        return Response(serializer.data)


class UserActivation(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ActivationSerializer

    def get(self, request, activation_token):
        serializer = self.serializer_class(data={'activation_token': activation_token})
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountData(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = self.serializer_class(user, many=False)
        return Response(serializer.data)


class OilFieldAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OilFieldSerializer

    def get_object(self, request, pk):
        try:
            if request.user.is_superuser:
                return OilField.objects.get(pk=pk)
            else:
                return OilField.objects.get(pk=pk, owner=request.user)
        except OilField.DoesNotExist:
            raise NotFound


class OilFieldGet(OilFieldAPIView):

    def get(self, request, pk):
        oil_field = self.get_object(request, pk)
        serializer = self.serializer_class(oil_field)
        return Response(serializer.data)


class OilFieldChangeName(OilFieldAPIView):
    def patch(self, request, pk):
        oil_field = self.get_object(request, pk)
        serializer = self.serializer_class(oil_field, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OilFieldsList(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OilFieldSerializer

    def get(self, request):
        oil_fields = OilField.objects.filter(owner__isnull=True, is_for_sale=True)
        serializer = self.serializer_class(oil_fields, many=True)
        return Response(serializer.data)


class OilFieldBuyAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OilFieldBuySerializer

    def post(self, request, pk):
        serializer = self.serializer_class(data={'oil_field_id': pk, 'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OilFieldSetForSaleAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OilFieldSetForSaleSerializer

    def post(self, request, pk):
        serializer = self.serializer_class(
            data={'oil_field_id': pk, 'user_id': request.user.id, 'price': request.data['price']})
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
