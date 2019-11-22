from django.urls import path
from core.views import UserRegistration, UserActivation, OilFieldsList, OilFieldBuyAPIView, AccountData, \
    UserOilFieldsList, OilFieldDetail, OilFieldStartDrillingAPIView, OilFieldStopDrillingAPIView

urlpatterns = [
    path('register', UserRegistration.as_view(), name='register'),
    path('activate/<str:activation_token>', UserActivation.as_view(), name='activate'),
    path('account/data', AccountData.as_view(), name='account-data'),
    path('account/oil-fields', UserOilFieldsList.as_view(), name='account-oil-fields'),
    path('oil-fields/for-sale', OilFieldsList.as_view(), name='list-oil-fields-for-sale'),
    path('oil-fields/<int:pk>', OilFieldDetail.as_view(), name='oil-field-detail'),
    path('oil-fields/<int:pk>/buy', OilFieldBuyAPIView.as_view(), name='buy-oil-field'),
    path('oil-fields/<int:pk>/start-drilling', OilFieldStartDrillingAPIView.as_view(), name='start-drilling'),
    path('oil-fields/<int:pk>/stop-drilling', OilFieldStopDrillingAPIView.as_view(), name='stop-drilling'),
]
