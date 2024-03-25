from rest_framework import serializers
from ..models import Test, Sport, HabsosT, HabsosJ, HabsosPrediction

class HabsosTSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabsosT
        fields = '__all__'

class HabsosJSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabsosJ
        fields = '__all__'

class HabsosPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabsosPrediction
        fields = '__all__'