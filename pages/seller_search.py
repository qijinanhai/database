import streamlit as st
import pandas as pd
import datetime
from time import strftime

from sqlSettings import *
import MySqlUtils


def click_btn_merchant(user_id, sell_id):
    mysql = MySqlUtils.MysqlClass(server=MYSQL_SERVER_IP,
                                  port=MYSQL_SERVER_PORT,
                                  user=MYSQL_USER_NAME,
                                  password=MYSQL_USER_PWD,
                                  db_name=MYSQL_DB_NAME)
    method=0
    consign_setting = 0
    user_category=0


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
        method=1
        consign_setting = st.sidebar.number_input(label='单次配送数量', step=1)

    mer_info = mysql.findAll('select * from merchants where mer_id = ' + sell_id)[0]
    data = mysql.findAll('select * from products where mer_id = ' + sell_id)
    temp_pd = pd.DataFrame(list(data))
    temp_pd.columns = ['产品号', '产品名称', '产品价格', '库存量', '生产地', '生产日期', '保质期', '商家号', '产品大类']
    with st.container():
        col1, col2, col3 = st.columns([4, 1, 1])
        # 初始化展示几个商品  购买按钮，数量按钮，
        with col1:
            st.table(temp_pd)
        with col2:
            amount_dict = locals()
            for i in range(0, len(data)):
                amount_dict['amount' + str(i)] = st.number_input(label=str(i), label_visibility="hidden", step=1)
        with st.container():
            with col3:
                for i in range(0, len(data)):
                    st.button(label='购买', key=str(i), on_click=purchase,
                              args=(data[i], amount_dict['amount' + str(i)], user_id, sell_id, mysql, method, option,
                                    mer_info[4], consign_setting))


# 点击购买商品
def purchase(good_info, amount_demo, user_id, seller_id, mysql, method, user_address, mer_address, consign_setting):
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
    data_order['price_all'] = good_info[2] * amount_demo
    mysql.save('orders', data_order)

    temp_now = now.replace(' ', '').replace(':', '').replace('-', '').strip()
    orderid = mysql.findAll("select order_id from orders where trim(replace(replace(replace(order_date,' ',''),':',''),'-','')) = " + temp_now)[0][0]

    data_order1 = {}
    data_order1['user_id'] = user_id
    data_order1['mer_id'] = seller_id  # 1,0
    data_order1['pay_amount'] = good_info[2] * amount_demo
    data_order1['pay_info'] = '无'
    data_order1['order_id'] = orderid
    mysql.save('payment', data_order1)
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
            data_consign['se_time'] = datetime.datetime.strftime(time_stamp,'%Y-%m-%d %H:%M:%S')
            data_consign['consign_amount'] = consign_setting
            mysql.save('consign_info1', data_consign)
            amount_lag = amount_lag - consign_setting

        if amount_lag > 0:
            time_stamp = time_stamp + datetime.timedelta(days=1)
            data_consign['se_time'] = datetime.datetime.strftime(time_stamp, '%Y-%m-%d %H:%M:%S')
            data_consign['consign_amount'] = amount_lag
            mysql.save('consign_info1', data_consign)

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
        mysql.save('consign_info1', data_consign)
