from django.urls import path

from .views import ProductMaterialsInfoAPIView

urlpatterns = [
    path('materials-info/', ProductMaterialsInfoAPIView.as_view(), name='materials-info'),
]
