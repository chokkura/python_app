import datetime
from django.contrib import admin

from django.db import models
from django.utils import timezone
from django.utils.timezone import now

class News(models.Model):
    # 厚生労働省のニュース
    #   field: 健康・医療, 福祉・介護, 雇用・労働, 年金, その他
    #   pub_date: ニュースがアップロードされた日時 
    @admin.display(
            boolean=True,
            ordering="pub_date",
            description="Published recently?",
    )

    def __str__(self):
        return self.title
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    title = models.CharField(verbose_name='タイトル', max_length=30)
    field = models.CharField(verbose_name='分野', max_length=20)
    summary = models.CharField(verbose_name='要約', max_length=200)
    pub_date = models.DateTimeField(verbose_name='作成日', default=now)




class Choice(models.Model):
    # ニュースに対するコメント・投票

    def __str__(self):
      return self.choice_text

    news = models.ForeignKey(News, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, help_text='記事への意見')
    votes = models.IntegerField(default=0)