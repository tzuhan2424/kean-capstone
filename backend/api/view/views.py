from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from ..models import Test, Sport
from ..serializer.serializers import TestSerializer,SportSerializer
from rest_framework.views import APIView

from rest_framework.response import Response

from django.db import connection

# Create your views here.


def hello(request):
    return HttpResponse("Hello, world. You're at the polls index.")
def test(request):
    return HttpResponse("test")

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
    



