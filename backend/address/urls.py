from django.urls import path, include
from rest_framework.routers import DefaultRouter

from address import views

router = DefaultRouter()
router.register('', views.AddressViewSet)

app_name = 'address'

urlpatterns = [
     path('', include(router.urls))
]
