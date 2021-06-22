# -*- coding: utf-8 -*-
import threading
import time
import requests
import json
import logging
import sys
import os
from fake_useragent import UserAgent
import random
from random import randint
from datetime import datetime
# from django.utils import timezone
from pytz import common_timezones, timezone
from requests.auth import HTTPBasicAuth


ua = UserAgent()
node= "python_a"

def que_size(que_file):
    all_line=[]
    f = open(str(que_file),'r')
    line = f.readlines()
    f.close()
    print("que.txt의 총 원소의 갯수는")
    print(len(line))
    return len(line)


def read_all_line(que_file):
    all_line=[]
    f = open(str(que_file),'r')
    line = f.readlines()
    f.close()
    if len(line) != 0:
        for idx, value in enumerate(line):
            if value[-1] == '\n':
                all_line.append(value[:-1])
            else:
                all_line.append(value)
    
    return all_line



def just_last_line(que_file):
    all_line=[]
    f = open(str(que_file),'r')
    line = f.readlines()
    f.close()
    if len(line) != 0:
        for idx, value in enumerate(line):
            if value[-1] == '\n':
                all_line.append(value[:-1])
            else:
                all_line.append(value)
    
    return all_line[-1]


def request_connection_permit(que_file):
    f = open(str(que_file),'r+')
    lines = f.read()
    f.seek(0, 0) #get to the first position
    f.write(str(sys.argv[1]+"_"+str(sys.argv[2]).rstrip('\r\n') + '\n' + lines))
    f.close()


def delete_connection_permit(que_file):
    f = open(str(que_file),'r')
    lines = f.read()
    f.close()
    m=lines.split("\n")
    if m[-1] == '':
        m.pop()
    s="\n".join(m[:-1])
    f = open(str(que_file),'w+')
    for i in range(len(s)):
        f.write(s[i])
    f.close()


def check_infinite():
    all_line = []
    all_line = read_all_line("/root/que.txt")
    error_count = 0

    
    if que_size("/root/que.txt") > 2:
        old_last_line = just_last_line("/root/que.txt")
        for i in range(0, 50):
            time.sleep(3)
            if que_size("/root/que.txt") <2:
 	    	print("중간에 que가 초기화 되어, 반복문을 나갑니다.")
		break
            new_last_line = just_last_line("/root/que.txt")
            print("확인완료, 3초후 재실행")
            if old_last_line != new_last_line:
                print("que의 마지막이 정상적으로 전환 되었습니다.")
                print(str(old_last_line)+" --> " + str(new_last_line))
                error_count = 0
                break
            if i==49:
                if error_count == 5:
                    print("que의 마지막 요소의 지연이 5번 있었습니다. 있습니다. 큐를 재정립합니다.")
                    # GET방식 호출 테스트
                    delete_url  = 'http://ip.mserver.o-r.kr:30080/api/v2/job_templates/11/launch/' # 접속할 사이트주소 또는 IP주소를 입력한다
                    # headers = {'Content-Type': 'application/json; chearset=utf-8'}
                    res = requests.post(delete_url, auth=HTTPBasicAuth('admin', 'password'))
                    print(str(res.status_code) + " | " + res.text)
                    # data = {'station_id': value[0], 'prd_type': value[1]}
                    time.sleep(10)
                    reload_url  = 'http://ip.mserver.o-r.kr:30080/api/v2/job_templates/10/launch/' # 접속할 사이트주소 또는 IP주소를 입력한다
                    # headers = {'Content-Type': 'application/json; chearset=utf-8'}
                    res = requests.post(reload_url, auth=HTTPBasicAuth('admin', 'password'))
                    print(str(res.status_code) + " | " + res.text)
                    # data = {'station_id': value[0], 'prd_type': value[1]}
                    print(str(new_last_line))
                    time.sleep(60)
                    break
                else:
                    error_count= error_count+1
                    print("que의 마지막 요소가 150초 가량 지속되고 있습니다. 맨 마지막 큐를 맨 위로 올립니다.")
                    # GET방식 호출 테스트
                    # print(str(just_last_line("/root/que.txt")))
                    last_line_stn = str(just_last_line("/root/que.txt")).split("_")[0]
                    last_line_type = str(just_last_line("/root/que.txt")).split("_")[1]
                    print(last_line_stn) #오류가 난 역
                    print(last_line_type) #오류가 난 역의 타입
                    data = {"extra_vars": {'station_id': str(last_line_stn), 'prd_type': str(last_line_type), 'node': node}}

                    delete_connection_permit("/root/que.txt") #que의 가장 마지막(오류 난 역) 삭제
                    delete_url  = 'http://ip.mserver.o-r.kr:30080/api/v2/job_templates/13/launch/' # 접속할 사이트주소 또는 IP주소를 입력한다
                    headers = {'Content-Type': 'application/json; chearset=utf-8'}
                    res = requests.post(delete_url, headers=headers, data=json.dumps(data), auth=HTTPBasicAuth('admin', 'password'), verify=False)
                    print(str(res.status_code) + " | " + res.text)
                    # data = {'station_id': value[0], 'prd_type': value[1]}
                    time.sleep(10)
                    reload_url  = 'http://ip.mserver.o-r.kr:30080/api/v2/job_templates/14/launch/' # 접속할 사이트주소 또는 IP주소를 입력한다
                    # headers = {'Content-Type': 'application/json; chearset=utf-8'}
                    res = requests.post(reload_url, headers=headers, data=json.dumps(data), auth=HTTPBasicAuth('admin', 'password'), verify=False)
                    print(str(res.status_code) + " | " + res.text)
                    # data = {'station_id': value[0], 'prd_type': value[1]}
                    print(str(new_last_line))
                    time.sleep(60)
                    break
    else:
        print("que의 길이가 2 이하입니다.")

    threading.Timer(3, check_infinite).start()
            

# def kill_process():

#     appName = "151 OR"
#     killApp = 'killall -9 ' + appName
#     os.system(killApp)
            
            
            


    # print(all_line)


check_infinite()

# kill_process()


