# tools/serializers.py
from rest_framework import serializers
from .models import Tool, CO2Absorption, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image']

class ToolSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Tool
        fields = [
            'id',
            'name',
            'co2_emission',
            'category',
            'is_electric',
            'energy_class'
        ]

    def validate(self, data):
        is_electric = data.get('is_electric', False)
        energy_class = data.get('energy_class', None)
        if is_electric and not energy_class:
            raise serializers.ValidationError({
                'energy_class': 'Klasa energetyczna musi być ustawiona dla narzędzi elektrycznych.'
            })
        if not is_electric and energy_class is not None:
            raise serializers.ValidationError({
                'energy_class': 'Klasa energetyczna może być ustawiona tylko dla narzędzi elektrycznych.'
            })
        return data

class CO2AbsorptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CO2Absorption
        fields = ['id', 'source', 'absorption_rate']
