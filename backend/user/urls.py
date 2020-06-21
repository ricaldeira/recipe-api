from django.urls import path
from rest_framework.routers import DefaultRouter


from . import views

app_name = 'user'


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),

]

    # # path('address/<int:id>/', views.AddressViewSet.as_view(), name='address'),
    # path('address/', views.AddressViewSet.as_view(), name='addresses'),
    # path('city/', views.CityViewSet.as_view(), name='city'),
    # # path('cities/', views.CityListViewSet.as_view(), name='cities'),
    # path('state/', views.StateViewSet.as_view(), name='state'),