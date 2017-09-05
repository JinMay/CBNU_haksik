from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^keyboard/$', views.keyboard, name="keyboard"),
    url(r'^message/$', views.answer, name="answer"),
    url(r'^friend/$', views.friends, name="friends"),
    url(r'^leave/$', views.leave_chatroom, name="chatroom"),

    # crawling
    url(r'^crj.crawling$', views.crj_crawling, name="crj_crawling"),
    url(r'^main.crawling$', views.main_crawling, name="main_crawling"),
    url(r'^jin.crawling$', views.jin_crawling, name="jin_crawling"),
    url(r'^sung.crawling$', views.sung_crawling, name="sung_crawling"),
]
