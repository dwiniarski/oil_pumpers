from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from factories.serializers import FactoryBuildSerializer, FactoryToggleOperationalSerializer, FactoryUpgradeSerializer, \
    FactoryAsSupplierSerializer
from factories.models import FactoryType, Factory
from factories.serializers import FactoryTypeSerializer, FactorySerializer
from rest_framework.exceptions import NotFound


class FactoryBuildAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FactoryBuildSerializer

    def post(self, request):
        request.data['user_id'] = request.user.id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FactoryToggleOperationalAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FactoryToggleOperationalSerializer

    def post(self, request, pk):
        serializer = self.serializer_class(
            data={'factory_id': pk, 'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
        return Response({}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FactoryTypeList(generics.ListAPIView):
    queryset = FactoryType.objects.all()
    serializer_class = FactoryTypeSerializer


class UserFactoriesList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FactorySerializer

    def list(self, request, *args, **kwargs):
        factories = Factory.objects.filter(owner=request.user)
        serializer = self.serializer_class(factories, many=True)
        return Response(serializer.data)


class FactoryAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FactorySerializer

    def get_object(self, request, pk):
        try:
            if request.user.is_superuser:
                return Factory.objects.get(pk=pk)
            else:
                return Factory.objects.get(pk=pk, owner=request.user)
        except Factory.DoesNotExist:
            raise NotFound


class FactoryDetail(FactoryAPIView):

    def get(self, request, pk):
        factory = self.get_object(request, pk)
        serializer = self.serializer_class(factory)
        return Response(serializer.data)


class FactoryUpgradeAPIView(FactoryAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FactoryUpgradeSerializer

    def post(self, request, pk):
        request.data['user_id'] = request.user.id
        request.data['factory_id'] = pk
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductSuppliers(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FactoryAsSupplierSerializer

    def get(self, request, product_type):
        factories = Factory.objects.filter(type_id=product_type, is_selling=True, units_stored__gt=0).order_by(
            '-price_per_unit')
        serializer = self.serializer_class(factories, many=True)
        return Response(serializer.data)


class ProductBuy(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        pass
