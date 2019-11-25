from django.urls import path, register_converter
from factories.views import FactoryBuildAPIView, FactoryToggleOperationalAPIView, FactoryTypeList, UserFactoriesList, \
    FactoryDetail, FactoryUpgradeAPIView, ProductSuppliers
from . import converters

register_converter(converters.ProductTypeConverter, 'pt')

urlpatterns = [
    path('<int:pk>', FactoryDetail.as_view(), name='factory-detail'),
    path('<int:pk>/upgrade', FactoryUpgradeAPIView.as_view(), name='factory-upgrade'),
    path('build', FactoryBuildAPIView.as_view(), name='build-factory'),
    path('<int:pk>/toggle-operational', FactoryToggleOperationalAPIView.as_view(),
         name='toggle-operational-factory'),
    path('factory-types', FactoryTypeList.as_view(), name='factory-types-list'),
    path('account/factories', UserFactoriesList.as_view(), name='account-factories'),
    path('products/<pt:product_type>/suppliers', ProductSuppliers.as_view(), name='product-suppliers')
]
