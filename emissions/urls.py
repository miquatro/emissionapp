from django.urls import path
from . import views
from emissions.views import SearchView, CompareView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('search/', SearchView.as_view(), name="search"),
    path('compare/', CompareView.as_view(), name="compare"),
]