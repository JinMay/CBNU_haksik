import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import requests
from bs4 import BeautifulSoup

from .models import Main


dorm = ['청람재', '본관', '양진재', '양성재']
day = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

# crawling
def crawling(request):
    Main.objects.all().delete()
    main_url = 'https://dorm.chungbuk.ac.kr/sub05/5_2.php?type1=5&type2=2'
    main_response = requests.get(main_url, verify=False)
    main_html = BeautifulSoup(main_response.content, 'lxml', from_encoding="utf-8")

    main_menus = main_html.select('tr[id]')

    for day in range(7):
        test = "{}\n\n[아침]\n{}\n\n[점심]\n{}\n\n[저녁]\n{}".format(main_menus[day].find_all('td')[0].get_text().strip(),
            main_menus[day].find_all('td')[1].get_text("\n").strip(),
            main_menus[day].find_all('td')[2].get_text("\n").strip(),
            main_menus[day].find_all('td')[3].get_text("\n").strip())
        day = Main(number = day, day = test)
        day.save()

        print(test)

    return HttpResponse()


def keyboard(request):
    keyboard = {
        "type" : "buttons",
        'buttons': ['청람재', '본관', '양진재', '양성재']
    }

    return JsonResponse(keyboard)

def keyboard_choice(mode):
    dorm_keyboard = {
        "type" : "buttons",
        'buttons': ['청람재', '본관', '양진재', '양성재']
    }

    day_keyboard = {
        "type" : "buttons",
        'buttons': ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일', '기숙사 선택']
    }

    if mode in dorm:
        return JsonResponse(day_keyboard)
    elif mode == "기숙사 선택":
        return JsonResponse(dorm_keyboard)



@csrf_exempt
def answer(request):
    # test = request.POST['content']
    raw_data = (request.body).decode('utf-8')
    json_body = json.loads(raw_data)
    dorm_or_day = json_body['content']
    # print(dorm_or_day) # 기숙사 이름 출력
    # print(dorm_or_day.__class__) # <class 'str'>

    # 기숙사 종류 선택했을 때
    if dorm_or_day in dorm:
        return JsonResponse({
            "message": {
                "text" : dorm_or_day
            },
            "keyboard": {
                "type" : "buttons",
                'buttons': ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일', '기숙사 선택']
            }
        })

    # 요일 선택했을 때
    elif dorm_or_day in day:
        if dorm_or_day == "월요일":
            menu = Main.objects.get(id = 1)
        return JsonResponse({
            "message": {
                "text" : dorm_or_day + "식단 입니다." + menu
            },
            "keyboard": {
                "type" : "buttons",
                # 'buttons': keyboard_choice(dorm_or_day)
                'buttons': ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일', '기숙사 선택']
            }
        })
    # 기숙사 선택을 눌렀을 때
    else:
        return JsonResponse({
            "message": {
                "text" : dorm_or_day
            },
            "keyboard": {
                "type" : "buttons",
                'buttons': ['청람재', '본관', '양진재', '양성재']
            }
        })
