from datetime import datetime, timedelta
# from time import strftime
# print(datetime.datetime.now())
# print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+timedelta(days=1))
# print(type(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#
# print(int(100/8))

import streamlit as st
import pandas as pd
from sqlSettings import *
import MySqlUtils
import datetime
import random
import numpy as np

mysql = MySqlUtils.MysqlClass(server=MYSQL_SERVER_IP,
                              port=MYSQL_SERVER_PORT,
                              user=MYSQL_USER_NAME,
                              password=MYSQL_USER_PWD,
                              db_name=MYSQL_DB_NAME)

# data = mysql.findAll('select distinct mer_type from products')
# print(data)

# type_list=['蔬果类','奶制品','生鲜类','酒类']
# for type_ in type_list:
# data_1 = mysql.findAll('select pro_id from products where mer_type = "' + '蔬果类"')
# temp_list=[]
# for i in range(len(data_1)):
#     data_dict = {}
#     data_dict['pro_id'] = data_1[i][0]
#     data_dict['max_diameter'] = round(np.random.random(),3)*10
#     temp_list.append(data_dict)
# mysql.saveMany('fruit', temp_list)


# data_1 = mysql.findAll('select pro_id from products where mer_type = "' + '奶制品"')
# temp_list=[]
# milk_type=['新西兰','澳大利亚','新疆']
# for i in range(len(data_1)):
#     data_dict = {}
#     data_dict['pro_id'] = data_1[i][0]
#     data_dict['milk_cat'] = random.choice(milk_type)
#     temp_list.append(data_dict)
# mysql.saveMany('milk', temp_list)

# data_1 = mysql.findAll('select pro_id from products where mer_type = "' + '生鲜类"')
# temp_list=[]
# milk_type=['四川','东北','新疆','山东']
# for i in range(len(data_1)):
#     data_dict = {}
#     data_dict['pro_id'] = data_1[i][0]
#     data_dict['fresh_info'] = random.choice(milk_type)
#     temp_list.append(data_dict)
# mysql.saveMany('fresh', temp_list)

data_1 = mysql.findAll('select pro_id from products where mer_type = "' + '酒类"')
temp_list=[]
# milk_type=['四川','东北','新疆','山东']
for i in range(len(data_1)):
    data_dict = {}
    data_dict['pro_id'] = data_1[i][0]
    data_dict['Alcoholic_strength'] = round(np.random.random(),3)*10+45
    temp_list.append(data_dict)
mysql.saveMany('wine', temp_list)