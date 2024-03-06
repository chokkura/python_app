from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404

from .models import News


# 厚生労働省のニュースを一覧表示
def index(request):
    latest_news_list = News.objects.order_by("-pub_date")[:5]
    context = {"latest_news_list": latest_news_list,}
    return render(request, "mhlw_news/index.html", context)

def detail(request, news_id):
    news = News.objects.get(pk=news_id)
    return render(request, "mhlw_news/detail.html", {"news": news})

def results(request, news_id):
    response = "%sの記事です"
    return HttpResponse(response % news_id)

def vote(request, news_id):
    return HttpResponse("%sの記事に投票します" % news_id)
