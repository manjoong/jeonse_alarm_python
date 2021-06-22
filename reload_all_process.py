#-*-coding:utf-8 -*-
from pyfcm import FCMNotification
import threading
import time
import requests
import json
import logging
import pymysql
import sys
from fake_useragent import UserAgent
from datetime import datetime
from pytz import common_timezones, timezone
import requests
import json
reload(sys)
sys.setdefaultencoding('utf-8')



# def web_request(method_name, url, dict_data, is_urlencoded=True):
#     """Web GET or POST request를 호출 후 그 결과를 dict형으로 반환 """
#     method_name = method_name.upper() # 메소드이름을 대문자로 바꾼다 
#     if method_name not in ('GET', 'POST'):
#         raise Exception('method_name is GET or POST plz...')
        
#     if method_name == 'GET': # GET방식인 경우
#         response = requests.get(url=url, params=dict_data)
#     elif method_name == 'POST': # POST방식인 경우
#         if is_urlencoded is True:
#             response = requests.post(url=url, data=dict_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
#         else:
#             response = requests.post(url=url, data=json.dumps(dict_data), headers={'Content-Type': 'application/json'})
    
#     dict_meta = {'status_code':response.status_code, 'ok':response.ok, 'encoding':response.encoding, 'Content-Type': response.headers['Content-Type']}
#     if 'json' in str(response.headers['Content-Type']): # JSON 형태인 경우
#         return {**dict_meta, **response.json()}
#     else: # 문자열 형태인 경우
#         return {**dict_meta, **{'text':response.text}}


def get_stnId_and_type():
    data = []
    conn = pymysql.connect(
        user='dev_user', 
        passwd='1q2w3e!@#',
        port=3306,
        host='ip.mserver.o-r.kr', 
        db='app_db', 
        charset='utf8'
    )
    try:
        # INSERT
        with conn.cursor() as curs: 
            sql = "select station_id, type from selected_station"
            # curs.execute(sql, (str(name), price, str(), 'www.naver.com/183', 'OPST', '468'))
            curs.execute(sql)
            rs = curs.fetchall()
            for index, row in enumerate(rs):
                # data.append()
                # user_list.append(row[0])
                data.append([row[0], row[1]])
                # data[index]['station_id']=row[0]
                # data[index]['station_type']=row[1]
            


            new_data = list(set(map(tuple, data)))
            print(new_data)
        conn.commit()

    
    finally:
        conn.close()
    return new_data
    
   
    

# def send_sale_alarm(station, sale_type, sale_name, sale_price, sale_link):
#     user_dic = {}
#     user_dic = get_user_token(station, sale_type)

#     for key, value in user_dic.items():
#         print(key, value)

#     for key, value in user_dic.items():
#         if value==1:
#             push_service = FCMNotification(api_key="AAAADgTMcII:APA91bFMVVBZB7bOM8BqocEGTJToANS9sB4Da0ODqG4RTfndoUapWBye8ASi9d3-rHUCkq4BvabFLgSqBfdyqrxtWCqZj3lYSYXpsFB-Szvo4gEgh9cExF24Puvr3I9rQ7r-H-pWMMQ0")
#             push_tokens = [str(key)]
#             print(str(key))
#             han_station=find_station_location(station)
#             han_type=translate_type(sale_type)
#             message_title = str(han_station) + " " + str(han_type) + " 매물 등록"
#             message_body = "매물명: " + str(sale_name) + "/ 가격: " + str(sale_price) 
#             result = push_service.notify_multiple_devices(registration_ids=push_tokens, message_title=message_title, message_body=message_body)
            
#             print(result)



    # for token in user_toker:
    #     push_service = FCMNotification(api_key="AAAADgTMcII:APA91bFMVVBZB7bOM8BqocEGTJToANS9sB4Da0ODqG4RTfndoUapWBye8ASi9d3-rHUCkq4BvabFLgSqBfdyqrxtWCqZj3lYSYXpsFB-Szvo4gEgh9cExF24Puvr3I9rQ7r-H-pWMMQ0")
    #     push_tokens = [str(token)]
    #     print(str(token))
        
    #     han_station=find_station_location(station)
    #     han_type=translate_type(sale_type)
    #     message_title = str(han_station) + " " + str(han_type) + " 매물 등록"
    #     message_body = "매물명: " + str(sale_name) + "/ 가격: " + str(sale_price) 
    #     result = push_service.notify_multiple_devices(registration_ids=push_tokens, message_title=message_title, message_body=message_body)
        
    #     print(result)
# send_sale_alarm(468, "OPST", "두산위클", 54000, "20-12-20 15:43:23" , "wwww.www.ww")

# result = push_service.notify_single_device(registration_id=push_tokens, message_title=message_title, message_body=message_body)

# cNTL3jvGjWA:APA91bFYdH88xieN8RRCekqH8WMM8j9KFz1NpHlzXSE8s3ooMutiSgnAoZHaVD48iGh1EW6o_fX1Sur17-nVkCnSatYvG43DD9pITNlmB9phhe1gMPl_1rou4NY2BetKarN3FNEMWDo1


# get_user_token(468, "OPST")
# send_sale_alarm(468, "OPST", "위브타워", "50000", "www.naver.com/land/204502")
new_data = get_stnId_and_type()

# push_sale("204502", "위브타워", "50000", "www.naver.com/image/23", "www.naver.com/land/204502", "OPST", "8")


# GET방식 호출 테스트
url  = 'https://ip.mserver.o-r.kr/reload_req_awx.php' # 접속할 사이트주소 또는 IP주소를 입력한다
# headers = {'Content-Type': 'application/json; chearset=utf-8'}

for idx, value in enumerate(new_data):
    # data = {'station_id': value[0], 'prd_type': value[1]}
    get_string = "?station_id="+str(value[0])+"&prd_type="+str(value[1])
    res = requests.get(url+get_string)
    print(str(res.status_code) + " | " + res.text)



    # data = {'station_id': value[0], 'prd_type': value[1]}         # 요청할 데이터
    # response = web_request(method_name='GET', url=url, dict_data=data)

    # print(response)
    # if response['ok'] == True:
    #     print(response['text'])
    #     # 성공 응답 시 액션
    # else:
    #     pass
    #     # 실패 응답 시 액션
