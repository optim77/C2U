# tools/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import ToolViewSet, CO2AbsorptionViewSet, CategoryViewSet, current_co2, ToolsByCategoryView

router = routers.DefaultRouter()
router.register(r'tools', ToolViewSet)
router.register(r'absorption', CO2AbsorptionViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tools/category/<int:category_id>/', ToolsByCategoryView.as_view(), name='tools-by-category'),
    path('current_co2/', current_co2, name='current-co2'),
]