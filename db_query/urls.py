from django.urls import path
from .views import *

urlpatterns = [
    path('parse_query',ParseQuery.as_view()),
]