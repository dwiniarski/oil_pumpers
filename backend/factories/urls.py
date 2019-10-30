from django.urls import path
from factories.views import FactoryBuildAPIView, FactoryToggleOperationalAPIView

urlpatterns = [
    path('factories/build', FactoryBuildAPIView.as_view(), name='build-factory'),
    path('factories/<int:pk>/toggle-operational', FactoryToggleOperationalAPIView.as_view(),
         name='toggle-operational-factory'),
]
