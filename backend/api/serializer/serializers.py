from rest_framework import serializers
from ..models import Test, Sport, HabsosT

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['name']

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ['name']
class HabsosTSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabsosT
        fields = '__all__'