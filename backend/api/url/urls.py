from django.urls import path

from ..view import views

urlpatterns = [
    path("", views.hello, name="hello"),
    path("test", views.test, name="test"),
    path("testlist", views.testList.as_view(), name="testlist"),
    path("sportlist", views.sportList.as_view(), name="sportlist"),


]