import json
import datetime

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

import requests
from bs4 import BeautifulSoup

from .models import Main, Yangsung, Yangjin, Crj
from .models import Galaxy


dorm = ['중문기숙사', '양진재', '양성재', '청람재']
day = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
uni_menu = ['은하수식당']

global_dorm = "" # 어떠한 기숙사를 선택했는지



# 중문기숙사
def main_crawling(request):
    Main.objects.all().delete()
    main_url = 'https://dorm.chungbuk.ac.kr/sub05/5_2.php?type1=5&type2=2'
    main_response = requests.get(main_url, verify=False)
    main_html = BeautifulSoup(main_response.content, 'lxml', from_encoding="utf-8")
    main_menus = main_html.select('tr[id]')

    for day in range(7):
        main_menu = "{}\n\n[아침]\n{}\n\n[점심]\n{}\n\n[저녁]\n{}".format(main_menus[day].find_all('td')[0].get_text().strip(),
            main_menus[day].find_all('td')[1].get_text("\n").strip(),
            main_menus[day].find_all('td')[2].get_text("\n").strip(),
            main_menus[day].find_all('td')[3].get_text("\n").strip())

        main = Main(number = day, day = main_menu)
        main.save()



    return HttpResponse()


# 양진재
def jin_crawling(request):
    Yangjin.objects.all().delete()
    jin_url = 'https://dorm.chungbuk.ac.kr/sub05/5_2_tab3.php?type1=5&type2=2'
    jin_response = requests.get(jin_url, verify=False)
    jin_html = BeautifulSoup(jin_response.content, 'lxml', from_encoding="utf-8")
    jin_menus = jin_html.select('tr')[1:8]

    for day in range(7):
        jin_menu = "{}\n\n[아침]\n{}\n\n[점심]\n{}\n\n[저녁]\n{}".format(jin_menus[day].find_all('td')[0].get_text().strip(),
            jin_menus[day].find_all('td')[1].get_text("\n").strip(),
            jin_menus[day].find_all('td')[2].get_text("\n").strip(),
            jin_menus[day].find_all('td')[3].get_text("\n").strip())

        jin = Yangjin(number = day, day = jin_menu)
        jin.save()

    return HttpResponse()


# 양성재
def sung_crawling(request):
    Yangsung.objects.all().delete()
    sung_url = 'https://dorm.chungbuk.ac.kr/sub05/5_2_tab2.php?type1=5&type2=2'
    sung_response = requests.get(sung_url, verify=False)
    sung_html = BeautifulSoup(sung_response.content, 'lxml', from_encoding="utf-8")
    sung_menus = sung_html.select('tr')[1:8]

    for day in range(7):
        sung_menu = "{}\n\n[아침]\n{}\n\n[점심]\n{}\n\n[저녁]\n{}".format(sung_menus[day].find_all('td')[0].get_text().strip(),
            sung_menus[day].find_all('td')[1].get_text("\n").strip(),
            sung_menus[day].find_all('td')[2].get_text("\n").strip(),
            sung_menus[day].find_all('td')[3].get_text("\n").strip())

        sung = Yangsung(number = day, day = sung_menu)
        sung.save()

    return HttpResponse()


# 청람재
def crj_crawling(request):
    Crj.objects.all().delete()
    crj_url = 'http://www.cbhscrj.kr/food/list.do?menuKey=39'
    crj_response = requests.get(crj_url)
    crj_html = BeautifulSoup(crj_response.content, 'lxml')
    crj_menus = crj_html.select('div.food_week_box')

    for day in range(7):
        crj_menu = crj = "{}\n\n[아침]\n{}\n\n[점심]\n{}\n\n[저녁]\n{}".format(crj_menus[day].find_all('p')[0].get_text().strip(),
            crj_menus[day].find_all('p')[1].get_text().replace(',', "\n").strip(),
            crj_menus[day].find_all('p')[2].get_text().replace(',', "\n").strip(),
            crj_menus[day].find_all('p')[3].get_text().replace(',', "\n").strip())

        crj = Crj(number = day, day = crj_menu)
        crj.save()

    return HttpResponse()


# 은하수식당
def get_galaxy():
    menu = Galaxy.objects.first()
    return str(menu)


def keyboard(request):
    keyboard = {
        "type" : "buttons",
        'buttons': ['중문기숙사', '양진재', '양성재', '청람재', '은하수식당']
    }

    return JsonResponse(keyboard)


# # data serializing 문제 때문에 미사용
# def keyboard_choice(mode):
#     dorm_keyboard = {
#         "type" : "buttons",
#         'buttons': ['청람재', '본관', '양진재', '양성재']
#     }
#
#     day_keyboard = {
#         "type" : "buttons",
#         'buttons': ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일', '기숙사 선택']
#     }
#
#     if mode in dorm:
#         return JsonResponse(day_keyboard)
#     elif mode == "기숙사 선택":
#         return JsonResponse(dorm_keyboard)


def menu_answer(day):
    day_dict = {
        "월요일": 1,
        "화요일": 2,
        "수요일": 3,
        "목요일": 4,
        "금요일": 5,
        "토요일": 6,
        "일요일": 0,
    }
    if global_dorm == "청람재":
        day_dict = {
            "월요일": 0,
            "화요일": 1,
            "수요일": 2,
            "목요일": 3,
            "금요일": 4,
            "토요일": 5,
            "일요일": 6,
        }

        day_menu = Crj.objects.get(number = day_dict[day])
        return str(day_menu)
    elif global_dorm == "중문기숙사":
        day_menu = Main.objects.get(number = day_dict[day])
        return str(day_menu)
    elif global_dorm == "양진재":
        day_menu = Yangjin.objects.get(number = day_dict[day])
        return str(day_menu)
    elif global_dorm == "양성재":
        day_menu = Yangsung.objects.get(number = day_dict[day])
        return str(day_menu)


# 오늘이 몇 일 무슨 요일인지 문자열로 리턴
def today_date():
    year = timezone.localdate().year
    month = timezone.localdate().month
    day = timezone.localdate().day
    date = timezone.localdate().weekday()
    date_list = ['월', '화', '수', '목', '금', '토', '일']

    today_str = "오늘은 {}년 {}월 {}일\n{}요일 입니다.".format(year, month, day, date_list[date])

    return today_str


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
        global global_dorm
        global_dorm = dorm_or_day

        return JsonResponse({
            "message": {
                "text" : dorm_or_day + '\n\n' + today_date()
            },
            "keyboard": {
                "type" : "buttons",
                'buttons': ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일', '기숙사 선택']
            }
        })

    # 요일 선택했을 때
    elif dorm_or_day in day:
        # if dorm_or_day == "월요일":
        #     menu = Main.objects.get(id = 1)
        # if global_dorm == "본관":
        #     menu = Main.objects.get(day_dict[dorm_or_day])

        return JsonResponse({
            "message": {
                "text" : dorm_or_day + "식단 입니다.\n" + menu_answer(dorm_or_day)
            },
            "keyboard": {
                "type" : "buttons",
                # 'buttons': keyboard_choice(dorm_or_day)
                'buttons': ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일', '기숙사 선택']
            }
        })

    # 은하수식당을 선택했을 때
    elif dorm_or_day == "은하수식당":
        return JsonResponse({
            "message": {
                "text" : dorm_or_day + '\n\n' + get_galaxy()
            },
            "keyboard": {
                "type" : "buttons",
                'buttons': ['은하수식당', '기숙사 선택']
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
                'buttons': ['중문기숙사', '양진재', '양성재', '청람재', '은하수식당']
            }
        })


# 친구추가 / 차단
# POST / DELETE
def friends(request):
    return HttpResponse(status=200)

# 채팅방 나가기
def leave_chatroom(request):
    return HttpResponse(status=200)
