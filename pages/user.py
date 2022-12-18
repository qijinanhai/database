import streamlit as st
import pandas as pd

from sqlSettings import *
import MySqlUtils

def app():
    mysql = MySqlUtils.MysqlClass(server=MYSQL_SERVER_IP,
                                  port=MYSQL_SERVER_PORT,
                                  user=MYSQL_USER_NAME,
                                  password=MYSQL_USER_PWD,
                                  db_name=MYSQL_DB_NAME)
    # login功能 即是一个搜索功能
    user_id = st.text_input('user_id')
    option1 = st.checkbox('👈点击查询1')
    if option1:
        data = mysql.findall('select * from orders where user_id = ' + user_id) #设置的地址，联系方式，自己的id
        with st.container: #地址管理
            col1, col2 = st.columns([4,1])

            with col1:
                for i in range(0,len(data)):
                    st.write(f"{data[i][0]}｜{data[i][1]}")
            with col2:
                st.button(label='修改',key='',on_click=change_address())

        with st.container: #展示该用户的订单，提供退单，续单功能,评价订单功能。查看订单后续的发货情况。
            col1, col2 = st.columns(2)

            with col1:
                for i in range(0,len(data)):
                    st.write(f"{data[i][0]}｜{data[i][1]}")
            with col2:
                st.button(label='修改',key='',on_click=check_list())

#查看已购买的订单
def check_list(good_id,user_id,seller_id,mysql):
    pass

def change_address(good_id,user_id,seller_id,address_id,mysql):
    pass