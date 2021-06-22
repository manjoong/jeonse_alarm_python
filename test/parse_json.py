# -*- coding: utf-8 -*-
import threading
import time
import datetime
import requests
import json
import logging
import copy


with open('../station.json') as json_file:
    data = json.load(json_file)

result=data["subways"]["subway"]

real_result = []
only_name = []


# print(len(result))
# print(json.dumps(result, indent = 1, ensure_ascii = False)) 

for idx1, val1 in enumerate(result):
    only_name.append(val1['name'])

# print(only_name)
# print(len(only_name))

del_duplicate_name = list(set(only_name))
# print(only_name)
# print(len(del_duplicate_name))

count = 0

for idx1, val1 in enumerate(del_duplicate_name):
    for idx2, val2 in enumerate(result):
        if val1 == val2['name']:
            del val2['stnId']
            val2['stnId']= count
            real_result.append(val2)
            count= count + 1
            break


# print(only_name)
# print(len(only_name))

# del_duplicate_name = list(set(only_name))
# print(only_name)
# print(len(del_duplicate_name))

# print(len(result))
print(json.dumps(real_result, indent = 1, ensure_ascii = False))