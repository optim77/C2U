# tools/views.py
from rest_framework import viewsets, status, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Tool, CO2Absorption, Category
from .serializers import ToolSerializer, CO2AbsorptionSerializer, CategorySerializer
from rest_framework.pagination import PageNumberPagination
import requests
from django.conf import settings

class ToolPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomPagination(PageNumberPagination):
    page_size = 5  # Ustaw rozmiar strony
    page_size_query_param = 'page_size'
    max_page_size = 10

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint do zarządzania kategoriami.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ToolViewSet(viewsets.ModelViewSet):
    """
    API endpoint do zarządzania narzędziami oraz ich porównywania.
    """
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'is_electric', 'energy_class']
    ordering_fields = ['co2_emission']
    search_fields = ['name']

    @action(detail=False, methods=['get'])
    def rank_by_category(self, request):
        """
        Endpoint do zwracania rankingu narzędzi w danej kategorii na podstawie emisji CO2.
        """
        category_id = request.query_params.get('category')
        if not category_id:
            return Response({"error": "Proszę podać kategorię."}, status=status.HTTP_400_BAD_REQUEST)

        tools = Tool.objects.filter(category=category_id).order_by('co2_emission')
        page = self.paginate_queryset(tools)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(tools, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def compare_in_category(self, request, pk=None):
        """
        Endpoint do porównywania narzędzia z innymi narzędziami w tej samej kategorii.
        """
        tool = self.get_object()
        category_tools = Tool.objects.filter(category=tool.category).exclude(id=tool.id).order_by('co2_emission')
        serializer = self.get_serializer(category_tools, many=True)
        return Response({
            "current_tool": ToolSerializer(tool).data,
            "competitors": serializer.data
        })

class CO2AbsorptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint dla pochłaniania CO2.
    """
    queryset = CO2Absorption.objects.all()
    serializer_class = CO2AbsorptionSerializer

@api_view(['GET'])
def current_co2(request):
    """
    API endpoint do pobierania aktualnych wskaźników CO2 z zewnętrznego API.
    """
    try:
        # Przykładowe API. Zastąp rzeczywistym API i kluczem API.
        api_url = 'https://api.example.com/current-co2'
        headers = {
            'Authorization': f'Bearer {settings.CO2_API_KEY}'
        }
        response = requests.get(api_url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        current_co2 = data.get('co2_ppm', None)

        if current_co2 is None:
            return Response({"error": "Nie znaleziono wskaźnika CO2"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"current_co2_ppm": current_co2}, status=status.HTTP_200_OK)
    except requests.RequestException as e:
        return Response({"error": "Błąd podczas pobierania danych CO2"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ToolsByCategoryView(generics.ListAPIView):
    serializer_class = ToolSerializer
    pagination_class = ToolPagination

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Tool.objects.filter(category_id=category_id)



