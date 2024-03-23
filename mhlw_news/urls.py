from django.urls import path

from . import views

app_name = "mhlw_news"
urlpatterns = [
  path("", views.IndexView.as_view(), name="index"),
  path("<int:pk>/", views.DetailView.as_view(), name="detail"),
  path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
  path("<int:news_id>/vote/", views.vote, name="vote"),
  path("post_news", views.post_news, name="post_news"),
  path("delete_news/<int:news_id>", views.delete_news, name="delete_news"),
  path("edit_news/<int:news_id>", views.edit_news, name="edit_news"),
  path("scrape_result", views.scrape_result, name="scrape_result"),
]