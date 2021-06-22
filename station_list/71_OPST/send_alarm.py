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
reload(sys)
sys.setdefaultencoding('utf-8')


def find_station_location(station_id):
    with open('station.json') as json_file:
        station_data = json.load(json_file)
    station_result = station_data["subways"]["subway"]
    # print(station_result)
    for idx, value in enumerate(station_result):
        if int(value["stnId"]) == int(station_id):
            location = value["name"]
            break
    return location

def translate_type(type):
    if type=="OPST":
        return "오피스텔"
    elif type=="APT":
        return "아파트"
    elif type=="OR":
        return "원룸"

def delete_user(token):
    user_list = []
    user_dic = {}
    conn = pymysql.connect(
        user='dev_user', 
        passwd='1q2w3e!@#',
        port=3306,
        host='ip.mserver.o-r.kr', 
        db='app_db', 
        charset='utf8'
    )
    try:
        # delete
        with conn.cursor() as curs: 
            sql = "delete from user where token_id=%s"
            # curs.execute(sql, (str(name), price, str(), 'www.naver.com/183', 'OPST', '468'))
            curs.execute(sql, str(token))
            rs = curs.fetchall()
            print(rs)
        conn.commit()
    
    finally:
        conn.close()
  

def get_user_token(station, sale_type):
    user_list = []
    user_dic = {}
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
            sql = "select user_id from selected_station where station_id=%s and type=%s"
            # curs.execute(sql, (str(name), price, str(), 'www.naver.com/183', 'OPST', '468'))
            curs.execute(sql, (int(station), str(sale_type)))
            rs = curs.fetchall()
            for row in rs:
                user_list.append(row[0])
        conn.commit()
    
        with conn.cursor() as curs: 
            for user in user_list:
                sql = "select token_id, alarm from user where id=%s"
                curs.execute(sql, (user))
                rs = curs.fetchall()
                for row in rs:
                    # print(row[1])
                    user_dic[row[0]]=row[1]
        conn.commit()

    
    finally:
        conn.close()
    return user_dic
    
   
    

def send_sale_alarm(station, sale_type, sale_name, sale_price, sale_link):
    user_dic = {}
    user_dic = get_user_token(station, sale_type)

    for key, value in user_dic.items():
        print(key, value)

    for key, value in user_dic.items():
        if value==1:
            # push_service = FCMNotification(api_key="AAAADgTMcII:APA91bFMVVBZB7bOM8BqocEGTJToANS9sB4Da0ODqG4RTfndoUapWBye8ASi9d3-rHUCkq4BvabFLgSqBfdyqrxtWCqZj3lYSYXpsFB-Szvo4gEgh9cExF24Puvr3I9rQ7r-H-pWMMQ0")
            
            push_service = FCMNotification(api_key="AAAADgTMcII:APA91bEzzSEqf5xiPHQ6uPPbaq1IwO1ajkJIWbVKrfCW6GrSMXyusMQRFp1vowmekKWGhRWRQKlZp1oFJYI8A6xKYh3qGVqkIAqsamEe0S9MKRp0ieIbc3rKf6vBVB-pns5uRo1ZJ-dC")
            
            
            push_tokens = [str(key)]
            print(str(key))
            han_station=find_station_location(station)
            han_type=translate_type(sale_type)
            message_title = str(han_station) + " " + str(han_type) + " 매물 등록"
            message_body = "매물명: " + str(sale_name) + "/ 가격: " + str(sale_price) 
            result = push_service.notify_multiple_devices(registration_ids=push_tokens, message_title=message_title, message_body=message_body)
            
            print(result)

            if result['failure'] == 1:
                error_description = result['results'][0]
                if error_description['error'] == "NotRegistered":
                    delete_user(push_tokens[0])
                    print(push_tokens[0])
                    print(" NotRegistered token")



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
# send_sale_alarm(270, "APT", "두산위클", 54000, "wwww.www.ww")

# result = push_service.notify_single_device(registration_id=push_tokens, message_title=message_title, message_body=message_body)

# cNTL3jvGjWA:APA91bFYdH88xieN8RRCekqH8WMM8j9KFz1NpHlzXSE8s3ooMutiSgnAoZHaVD48iGh1EW6o_fX1Sur17-nVkCnSatYvG43DD9pITNlmB9phhe1gMPl_1rou4NY2BetKarN3FNEMWDo1


# get_user_token(468, "OPST")
# send_sale_alarm(468, "OPST", "위브타워", "50000", "www.naver.com/land/204502")

# push_sale("204502", "위브타워", "50000", "www.naver.com/image/23", "www.naver.com/land/204502", "OPST", "8")
