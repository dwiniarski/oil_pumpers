from django.urls import path
from core.views import UserRegistration, UserActivation, OilFieldsList, OilFieldBuyAPIView, OilFieldSetForSaleAPIView, \
    AccountData, index, UserOilFieldsList, OilFieldGet, OilFieldChangeName

urlpatterns = [
    path('register', UserRegistration.as_view(), name='register'),
    path('activate/<str:activation_token>', UserActivation.as_view(), name='activate'),
    path('account/data', AccountData.as_view(), name='account-data'),
    path('account/oil-fields', UserOilFieldsList.as_view(), name='account-oil-fields'),
    path('oil-fields/for-sale', OilFieldsList.as_view(), name='list-oil-fields-for-sale'),
    path('oil-fields/<int:pk>', OilFieldGet.as_view(), name='get-oil-field'),
    path('oil-fields/<int:pk>/change-name', OilFieldChangeName.as_view(),
         name='change-oil-field-name'),
    path('oil-fields/<int:pk>/buy', OilFieldBuyAPIView.as_view(), name='buy-oil-field'),
    path('oil-fields/<int:pk>/set-for-sale', OilFieldSetForSaleAPIView.as_view(), name='set-for-sale-oil-field'),
    path('oil-fields/<int:pk>/save-name', OilFieldSetForSaleAPIView.as_view(), name='save-name-oil-field'),
]
