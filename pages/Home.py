import streamlit as st
import requests
from sqlSettings import *
import MySqlUtils
from multipage import MultiPage


# class Home_Create:
#     def __init__(self):
def search_box():
    mysql = MySqlUtils.MysqlClass(server=MYSQL_SERVER_IP,
                                  port=MYSQL_SERVER_PORT,
                                  user=MYSQL_USER_NAME,
                                  password=MYSQL_USER_PWD,
                                  db_name=MYSQL_DB_NAME)
    col1, col2 = st.columns([4, 1])
    with col1:
        search = st.text_input(label=' ', value='搜素关键词')
    with col2:
        btn_flag = st.selectbox('查询范围', ('物品名称', '物品种类'), label_visibility='hidden')
    btn_flag_1 = st.button('查询')
    st.write('you enter is ', search)
    if btn_flag_1:
        try:
            if btn_flag == '物品名称':
                st.write(mysql.findAll('select * from products where pro_name =' + search))  # 搜索前十个
            else:
                st.error('没有该商品', icon="🚨")
            # elif btn_flag=='物品种类':
            #     st.write(mysql.findAll('select * from table_name where categroy =' + search))  #搜索前十个  ！！！！！！！！！！！
        except:
            st.error('没有该商品', icon="🚨")


def app():
    search_box()
