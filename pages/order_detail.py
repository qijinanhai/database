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
    option1 = st.checkbox('👈点击查询订单')

    if option1:
        data = mysql.findAll(
            'select order_id,number,method,order_date,pro_id,user_id,mer_id from orders where user_id = ' + user_id)  # 设置的地址，联系方式，自己的id
        order_list = []
        for i in range(len(data)):
            order_list.append(data[i][0])

        option = st.sidebar.selectbox(
            '查看订单详情',
            order_list)
        '### 你的选择是:', option

        if option:
            consign_data = mysql.findAll(
                'select con_id,se_add,re_add,se_time,consign_amount,get_state from consign_info where order_id = ' + str(option))  # 设置的地址，联系方式，自己的id
            temp_pd = pd.DataFrame(list(consign_data))
            temp_pd.columns = ['订单号','发货地址', '收货地址', '发货时间', '发货数量', '收获状态']

            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.table(temp_pd)
                with col2:
                    detail_dict = locals()
                    for i in range(0, len(consign_data)):
                        detail_dict['amount' + str(i)] = st.button('确认收货', key='confirm' + str(i), on_click=confirm,
                                                               args=(consign_data[i][0],mysql))

def confirm(con_id,mysql):
    mysql.exec('update consign_info set get_state=1 where con_id = ' + str(con_id))

