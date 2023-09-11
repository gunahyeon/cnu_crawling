from flask import Flask, request
from extractors.cnu_menu import extract_menu
import locale
from datetime import datetime

app = Flask("테스트 웹페이지")

quickReplies = [
                    {
                        "messageText": "오늘 밥 뭐야?",
                        "action": "message",
                        "label": "오늘 밥 뭐야?"
                    },
                    {
                        "messageText": "홈",
                        "action": "message",
                        "label": "홈"
                    },
                ]               

# 홈
@app.route('/', methods=['POST'])
def welcome():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                            "title": "",
                            "description": "안녕하세요 학우님, 어떤 정보를 알려드릴까요?🐰\n",
                            "buttons": [
                                {
                                "action": "message",
                                "label": "오늘 밥 뭐야?",
                                "messageText": "오늘 밥 뭐야?"
                                },
                                {
                                "action":  "webLink",
                                "label": "학생생활관 바로가기",
                                "webLinkUrl": "https://dorm.cnu.ac.kr/html/kr/guide/guide_0601.html"
                                }
                            ]
                            }
                        }
                    ],
                }
            }

    return responseBody

## 카카오톡 캐러셀형 응답 : 밥 알려주기(한국어)
@app.route('/api/menu_all/kor', methods=['POST'])
def menu_all_kor():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    cnu_menu = extract_menu('kor')

    # 요일 배열 만들기
    days_of_week_korean = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

    # 현재 요일 가져오기
    today = datetime.now()
    day_index = today.weekday()  # 0(월요일)부터 6(일요일)까지의 숫자로 요일을 나타냄
    today_day = days_of_week_korean[day_index]    

    responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "carousel": {
                                "type": "basicCard",
                                "items": [
                                    {
                                        "title": "오늘 " + today_day + " 아침입니다🍚!",
                                        "description": cnu_menu[0]['morning_kor']
                                    },
                                    {
                                        "title": "오늘 " + today_day + " 점심입니다🍚!",
                                        "description": cnu_menu[0]['lunch_kor']
                                    },
                                    {
                                        "title": "오늘 " + today_day + " 저녁입니다🍚!",
                                        "description": cnu_menu[0]['dinner_kor']
                                    },
                                ]
                                # "items": [
                                #     {
                                #         "title": datetime.now().strftime("%Y년%m월%d일") + today_day + " 아침🍚",
                                #         "description": cnu_menu[0]['morning_kor']
                                #     },
                                #     {
                                #         "title": datetime.now().strftime("%Y년%m월%d일") + today_day + " 점심🍚",
                                #         "description": cnu_menu[0]['lunch_kor']
                                #     },
                                #     {
                                #         "title": datetime.now().strftime("%Y년%m월%d일") + today_day + " 저녁🍚",
                                #         "description": cnu_menu[0]['dinner_kor']
                                #     },
                                # ]
                            }
                        }
                    ],
                    "quickReplies": quickReplies                            
                }
            }

    return responseBody

## 카카오톡 캐러셀형 응답 : 밥 알려주기(영어)
@app.route('/api/menu_all/eng', methods=['POST'])
def menu_all_eng():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    cnu_menu = extract_menu('eng')

    responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "carousel": {
                                "type": "basicCard",
                                "items": [
                                    {
                                        "title": datetime.now().strftime("%Y/%m/%d") + " " + datetime.now().strftime("%a") + " breakfast🍚",
                                        "description": cnu_menu[0]['morning_eng']
                                    },
                                    {
                                        "title": datetime.now().strftime("%Y/%m/%d") + " " + datetime.now().strftime("%a") + " lunch🍚",
                                        "description": cnu_menu[0]['lunch_eng']
                                    },
                                    {
                                        "title": datetime.now().strftime("%Y/%m/%d") + " " + datetime.now().strftime("%a") + " dinner🍚",
                                        "description": cnu_menu[0]['dinner_eng']
                                    },
                                ]
                            }
                        }
                    ]
                }
            }

    return responseBody


## 카카오톡 이미지형 응답
# @app.route('/api/showHello', methods=['POST'])
# def showHello():
#     body = request.get_json()
#     print(body)
#     print(body['userRequest']['utterance'])

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleImage": {
#                         "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
#                         "altText": "hello I'm Ryan"
#                     }
#                 }
#             ]
#         }
#     }

#     return responseBody

app.run(host='0.0.0.0', port=3001)