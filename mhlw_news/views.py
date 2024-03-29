
from django.http import HttpResponseRedirect
from django.http import Http404
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import F
from django.utils import timezone

from .models import Choice, News
from .forms import NewNewsForm
from .forms import EditNewsForm
from .get_html import scraping_mhlw


class IndexView(generic.ListView):
    # 厚生労働省のニュースを一覧表示
    template_name = "mhlw_news/index.html"
    context_object_name = "latest_news_list"

    def get_queryset(self):
        """ 直近5記事を表示(未来の記事は含まない) """
        return News.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
# 新規記事を作成するページ
def post_news(request):
    if request.method == 'POST':
        print("test")
        form = NewNewsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("mhlw_news:index"))
    else:
        form = NewNewsForm()
    return TemplateResponse(request, 'mhlw_news/post_news.html',
                            {'form': form})
    

# 記事を削除
def delete_news(request, news_id):
    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        news.delete()
        return HttpResponseRedirect(reverse('mhlw_news:index'))
    else:
        return TemplateResponse(request, 'mhlw_news/detail.html',
                                {'id': news_id})

# 記事を編集
def edit_news(request, news_id):
    news = News.objects.get(id=news_id)
    form = EditNewsForm(instance=news)
    if request.method == 'POST':
        form = EditNewsForm(request.POST)
        if form.is_valid():
            print("valid!!")
            form.save()
            return HttpResponseRedirect(reverse('mhlw_news:index'))
    return TemplateResponse(request, 'mhlw_news/edit_news.html',
                           {'form': form, 'news': news})


class DetailView(generic.DetailView):
    model = News
    template_name = "mhlw_news/detail.html"

    def get_queryset(self):
        """ 未来の記事は含まない """
        return News.objects.filter(pub_date__lte=timezone.now())
  

    
class ResultsView(generic.DetailView):
    model = News
    template_name = "mhlw_news/results.html"
                  

def vote(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    try:
        selected_choice = news.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # 投票フォームを再表示する
        return render(
            request, "mhlw_news/detail.html",
            { "news": news,
             "error_message": "意見を選択していません"},
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # POSTデータの対処に成功すればHttpResponseRedirectで戻る
        # これによりBackボタンを押してデータが2回送信されるのを防げる
        return HttpResponseRedirect(reverse("mhlw_news:results", args=(news.id,)))

def scrape_result(request):
    latest_news_list = scraping_mhlw()
    return TemplateResponse(request, 'mhlw_news/scrape_result.html',
                            {"latest_news_list":latest_news_list })