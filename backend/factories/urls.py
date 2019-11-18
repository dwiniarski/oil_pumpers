from django.urls import path
from factories.views import FactoryBuildAPIView, FactoryToggleOperationalAPIView, FactoryTypeList, UserFactoriesList

urlpatterns = [
    path('build', FactoryBuildAPIView.as_view(), name='build-factory'),
    path('<int:pk>/toggle-operational', FactoryToggleOperationalAPIView.as_view(),
         name='toggle-operational-factory'),
    path('factory-types', FactoryTypeList.as_view(), name='factory-types-list'),
    path('account/factories', UserFactoriesList.as_view(), name='account-factories'),
]
