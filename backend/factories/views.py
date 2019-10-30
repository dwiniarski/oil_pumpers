from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from factories.serializers import FactoryBuildSerializer, FactoryToggleOperationalSerializer


class FactoryBuildAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FactoryBuildSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data={'factory_type_id': request.data['factory_type_id'], 'user_id': request.user.id,
                  'name': request.data['name']})
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
