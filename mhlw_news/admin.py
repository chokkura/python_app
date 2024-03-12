from django.contrib import admin

from .models import Choice, News


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["title", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["title"]

admin.site.register(News, NewsAdmin)