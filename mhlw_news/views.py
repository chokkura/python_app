from django.http import HttpResponse


def index(request):
  return HttpResponse("厚生労働省のニュースをかみくだくサイトです")
