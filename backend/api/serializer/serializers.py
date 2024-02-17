from rest_framework import serializers
from ..models import Test, Sport

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['name']

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ['name']
