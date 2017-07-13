from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^keyboard/$', views.keyboard, name="keyboard"),
    url(r'^message$', views.answer, name="answer"),

    url(r'^crawling$', views.crawling, name="crawling"),
]
