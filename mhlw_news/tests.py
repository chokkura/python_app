import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import News

class NewsModelTests(TestCase):
    def test_was_published_recently_with_future_news(self):
        """ 未来のpub_dateを持つ場合にFalseを返す """
        time = timezone.now() + datetime.timedelta(days=30)
        future_news = News(pub_date=time)
        self.assertIs(future_news.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ 現在時間から24時間以内のpub_dateを持つ場合にTrueを返す"""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_news = News(pub_date=time)
        self.assertIs(recent_news.was_published_recently(), True)


def create_news(title, days):
    """ title と pub_date を持つNewsオブジェクトを作成"""
    time = timezone.now() + datetime.timedelta(days=days)
    return News.objects.create(title=title, pub_date=time)

class NewsIndexViewTests(TestCase):
    def test_no_news(self):
        """ 記事がない事を伝えるメッセージが表示される"""
        response = self.client.get(reverse("mhlw_news:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "記事がありません・・")
        self.assertQuerySetEqual(response.context["latest_news_list"], [])

    def test_past_news(self):
        """ pub_date が過去の記事がindexページに表示される"""
        news = create_news(title="Past news", days=-30)
        response = self.client.get(reverse("mhlw_news:index"))
        self.assertQuerySetEqual(response.context["latest_news_list"], [news],)

    def test_future_enws(self):
        """ pub_date が未来の記事はindexページに表示されない"""
        create_news(title="Future news", days=30)
        response = self.client.get(reverse("mhlw_news:index"))
        self.assertContains(response, "記事がありません・・")
        self.assertQuerySetEqual(response.context["latest_news_list"], [])

    def test_future_news_and_past_news(self):
        """ pub_date が過去・未来の記事1つずつあれば、過去の分のみindexページに表示される"""
        news = create_news(title="Past news", days=-30)
        create_news(title="Future news", days=30)
        response = self.client.get(reverse("mhlw_news:index"))
        self.assertQuerySetEqual(response.context["latest_news_list"], [news])

    def test_two_past_news(self):
        """ pub_date が過去の記事が2つあれば、両方indexページに表示される"""
        news1 = create_news(title="Past news1", days=-30)
        news2 = create_news(title="Past news2", days=-5)
        response = self.client.get(reverse("mhlw_news:index"))
        self.assertQuerySetEqual(response.context["latest_news_list"], [news2, news1],)

class NewsDetailViewTests(TestCase):
    def test_future_news(self):
        """ 未来の記事のdetailページは404エラーとなる"""
        future_news = create_news(title="Future news", days=5)
        url = reverse("mhlw_news:detail", args=(future_news.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_news(self):
        """ 過去の記事のdetailページが表示される"""
        past_news = create_news(title="Past news", days=-5)
        url = reverse("mhlw_news:detail", args=(past_news.id,))
        response = self.client.get(url)
        self.assertContains(response, past_news.title)
