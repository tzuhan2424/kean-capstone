from rest_framework import serializers
from ..models import Test, Sport, HabsosT, HabsosJ

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

class HabsosJSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabsosJ
        fields = '__all__'