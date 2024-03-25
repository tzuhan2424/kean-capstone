from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from ..models import Test, Sport, HabsosT,HabsosJ, HabsosPrediction
from ..serializer.serializers import TestSerializer,SportSerializer, HabsosTSerializer,HabsosJSerializer
from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response

from django.db import connection
from datetime import datetime
import json

from django.core.serializers import serialize

# Create your views here.

def hello(request):
    return HttpResponse("Hello, world. You're at the polls index.")
def test(request):
    test_data = {
        'message': 'test'
    }
    return JsonResponse(test_data)

class testList(APIView):
    def get(self, request):
        Tests = Test.objects.all()
        print(Tests.query)  # Print the query to debug it
        Tests._fetch_all()  # Force evaluation of the QuerySet
        print(connection.queries)  # Print executed queries
        return Response('d')
    
class sportList(APIView):
    def get(self, request):
        sports = Sport.objects.all().values('name')  # specify the fields you need
        sports_list = list(sports)  # convert QuerySet to a list of dictionaries
        return JsonResponse(sports_list, safe=False)
    

class searchHabsosDb(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Extract the search parameters from the JSON data
            genus = data.get('genus')
            species = data.get('species')
            from_date_str = data.get('fromDate') + " 00:00:00"
            to_date_str = data.get('toDate') + " 23:59:59"
            # print('from_date_str', from_date_str)
            # print('to_date_str', to_date_str)

            # Use Django's ORM to query the database
            queryset = HabsosJ.objects.filter(
                genus=genus,
                species=species,
                sample_datetime__gte=from_date_str,
                sample_datetime__lte=to_date_str
            )
            # print(str(queryset.query))

         
            serializer = HabsosJSerializer(queryset, many=True)
            return JsonResponse(serializer.data, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

# class searchHabsosDb(APIView):
#     def post(self, request):
#         try:
#             data = json.loads(request.body)
            
#             # Extract the search parameters from the JSON data
#             genus = data.get('genus')
#             species = data.get('species')
#             from_date_str = data.get('fromDate') + " 00:00:00"
#             to_date_str = data.get('toDate') + " 23:59:59"
#             # print('from_date_str', from_date_str)
#             # print('to_date_str', to_date_str)

#             # Use Django's ORM to query the database
#             queryset = HabsosT.objects.filter(
#                 genus=genus,
#                 species=species,
#                 sample_datetime__gte=from_date_str,
#                 sample_datetime__lte=to_date_str
#             )
#             # print(str(queryset.query))

         
#             serializer = HabsosTSerializer(queryset, many=True)
#             return JsonResponse(serializer.data, safe=False)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#         except ValueError as e:
#             return JsonResponse({'error': str(e)}, status=400)


class PredictResult(APIView):
    def generatePredict(self, observations):
        total_predict_category = 0
        NofRows= len(observations)
        for obs in observations:
            total_predict_category += int(obs.predict_category or 0)

        predictChance = total_predict_category
        threshold_low = 4*NofRows/3
        threshold_high = 4*NofRows*2/3
        predictResult = ""
        if predictChance<threshold_low:
            predictResult = 'low'
        elif threshold_low<predictChance<threshold_high:
            predictResult = 'middle'
        else:
            predictResult = 'high'
        return predictResult

    def post(self, request):
        area_name = request.data.get('name')
        area_coordinates = request.data.get('coordinates')

        if area_coordinates:
            x1, y1, x2, y2 = area_coordinates
            x_min = min(x1, x2)
            x_max = max(x1, x2)
            y_min = min(y1, y2)
            y_max = max(y1, y2)

            observations = HabsosPrediction.objects.filter(
                latitude__gte=y_min,
                latitude__lte=y_max,
                longitude__gte=x_min,
                longitude__lte=x_max
            )
            # print(str(observations.query))
            result = self.generatePredict(observations)
            prediction_result = {
                "status": "success",
                "area": area_name,
                "result": result 
            }
        else:
            prediction_result = {"status": "error", "message": "Invalid coordinates"}
        
        
        return JsonResponse(prediction_result)

    