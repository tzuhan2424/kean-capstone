from django.urls import path

from ..view import views

urlpatterns = [
    path("", views.hello, name="hello"),
    path("searchHabsosDb", views.searchHabsosDb.as_view(), name="searchHabsosDb"),
    path("fetchPredictResult", views.PredictResult.as_view(), name="fetchPredictResult"),
    path("searchHabsosDbCondition", views.searchHabsosDbCondition.as_view(), name="searchHabsosDbCondition"),
    path("fetchForecastPredict", views.ForecastPredictResult.as_view(), name="fetchForecastPredict"),


]
