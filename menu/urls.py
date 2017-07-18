from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^keyboard/$', views.keyboard, name="keyboard"),
    url(r'^message$', views.answer, name="answer"),

    # crawling
    url(r'^crawling$', views.crawling, name="crawling"),
    url(r'^crj.crawling$', views.crj_crawling, name="crj_crawling"),
]
