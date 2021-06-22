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




    
   
    
sale_type = str(sys.argv[2])
sale_station= str(sys.argv[1])
# GET방식 호출 테스트
url  = 'https://ip.mserver.o-r.kr/reload_req_awx.php' # 접속할 사이트주소 또는 IP주소를 입력한다


get_string = "?station_id="+str(sale_station)+"&prd_type="+str(sale_type)
res = requests.get(url+get_string)
print(str(res.status_code) + " | " + res.text)



