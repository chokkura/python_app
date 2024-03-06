from django.urls import path

from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("<int:news_id>/", views.detail, name="detail"),
  path("<int:news_id>/results/", views.results, name="results"),
  path("<int:news_id>/vote/", views.vote, name="vote"),
]