import streamlit as st
import pandas as pd
from sqlSettings import *
import MySqlUtils
import datetime
from multipage import MultiPage


# class Home_Create:
#     def __init__(self):
def search_box():
    mysql = MySqlUtils.MysqlClass(server=MYSQL_SERVER_IP,
                                  port=MYSQL_SERVER_PORT,
                                  user=MYSQL_USER_NAME,
                                  password=MYSQL_USER_PWD,
                                  db_name=MYSQL_DB_NAME)

    method = 0
    consign_setting = 0
    user_category = 0

    user_id = st.text_input('user_id')
    option1 = st.checkbox('👈点击登录')
    if len(user_id) != 0:
        user_address = mysql.findAll('select add_info from address where user_id = ' + user_id)
        user_category = mysql.findAll('select is_Vip from user where user_id = ' + user_id)[0]
        user_category = user_category[0]
        address_list = []
        for i in range(len(user_address)):
            address_list.append(user_address[i][0])
        option = st.sidebar.selectbox(
            '选择你的配送地址',
            address_list)
        '### 你的选择是:', option
        if user_category == 1:
            option1 = st.sidebar.selectbox(
                '选择你的配送方式',
                ['一次性配送', '逐日多次配送'])
            '### 你的选择是:', option1
        elif user_category == 0:
            option1 = st.sidebar.selectbox(
                '选择你的配送方式',
                ['一次性配送'])
            '### 你的选择是:', option1

        if option1 == '逐日多次配送':
            method = 1
            consign_setting = st.sidebar.number_input(label='单次配送数量', step=1)

    col1, col2 = st.columns([4, 1])
    with col1:
        search = st.text_input(label=' ', value='搜素关键词')
    with col2:
        btn_flag_1 = st.checkbox('👈点击查询1')

    if btn_flag_1:
        try:
            data_search = mysql.findAll('select * from products where pro_name = "' + search + '" order by stock DESC LIMIT 1,10')
        except:
            st.error('没有该商品', icon="🚨")
        temp_pd = pd.DataFrame(list(data_search))
        temp_pd.columns = ['产品号', '产品名称', '产品价格', '库存量', '生产地', '生产日期', '保质期', '商家号']
        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])
            search_dict = locals()
            with col1:
                st.write(temp_pd)  # 搜索前十个
            with col2:
                amount_dict = locals()
                for i in range(0, len(data_search)):
                    amount_dict['amount' + str(i)] = st.number_input(label=str(i), label_visibility="hidden", step=1)
            with col3:
                for i in range(0, len(data_search)):
                    st.button(label='购买', key=str(i), on_click=purchase,
                              args=(data_search[i], amount_dict['amount' + str(i)], user_id, data_search[i][-1], mysql, method, option,
                                 consign_setting))



    # option = st.selectbox(
    #     '选择商品大类',
    #     ['水果','生鲜','牛奶','酒水'])

    # elif btn_flag=='物品种类':
    #     st.write(mysql.findAll('select * from table_name where categroy =' + search))  #搜索前十个  ！！！！！！！！！！！


def app():
    search_box()


def purchase(good_info, amount_demo, user_id, seller_id, mysql, method, user_address , consign_setting):
    mer_address = mysql.findOne('select mer_address from merchants where mer_id = '+str(seller_id))[0]
    st.write(mer_address)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mysql.exec('update products set stock=stock-' + str(amount_demo) + ' where pro_id =' + str(good_info[0]))
    data_order = {}
    data_order['number'] = amount_demo
    data_order['method'] = method  # 1,0
    data_order['order_date'] = now
    data_order['sp_needs'] = '无'
    data_order['pro_id'] = good_info[0]
    data_order['user_id'] = user_id
    data_order['mer_id'] = seller_id
    mysql.save('orders', data_order)

    temp_now = now.replace(' ', '').replace(':', '').replace('-', '').strip()
    orderid = mysql.findAll(
        "select order_id from orders where trim(replace(replace(replace(order_date,' ',''),':',''),'-','')) = " + temp_now)[
        0][0]
    # DATE_FORMAT(order_date, '+' % Y - % m - % d % H: % M: % S)
    amount_lag = amount_demo
    time_stamp = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=-1)
    if method == 1:
        data_consign = {}
        data_consign['order_id'] = orderid
        data_consign['re_add'] = user_address
        data_consign['se_add'] = mer_address
        data_consign['se_time'] = time_stamp
        data_consign['mer_id'] = seller_id
        data_consign['user_id'] = user_id
        data_consign['get_state'] = 0
        data_consign['consign_amount'] = consign_setting
        while (amount_lag - consign_setting) > 0:
            time_stamp = time_stamp + datetime.timedelta(days=1)
            data_consign['se_time'] = datetime.datetime.strftime(time_stamp, '%Y-%m-%d %H:%M:%S')
            data_consign['consign_amount'] = consign_setting
            mysql.save('consign_info', data_consign)
            amount_lag = amount_lag - consign_setting

        if amount_lag > 0:
            time_stamp = time_stamp + datetime.timedelta(days=1)
            data_consign['se_time'] = datetime.datetime.strftime(time_stamp, '%Y-%m-%d %H:%M:%S')
            data_consign['consign_amount'] = amount_lag
            mysql.save('consign_info', data_consign)

    elif method == 0:
        data_consign = {}
        data_consign['order_id'] = orderid
        data_consign['re_add'] = user_address
        data_consign['se_add'] = mer_address
        data_consign['se_time'] = time_stamp
        data_consign['mer_id'] = seller_id
        data_consign['user_id'] = user_id
        data_consign['get_state'] = 0
        data_consign['consign_amount'] = amount_demo
        mysql.save('consign_info', data_consign)
