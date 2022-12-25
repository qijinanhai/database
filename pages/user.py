import streamlit as st
import pandas as pd
import datetime

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
        address_data = mysql.findAll('select add_id,add_info from address where user_id = ' + user_id)

        temp_pd = pd.DataFrame(list(data))
        # st.write(temp_pd)
        temp_pd.columns = ['订单号', '订单数量', '发货方式', '订单日期', '产品id', '用户id', '商家id']
        with st.container():  # 展示该用户的订单，提供退单，续单功能,评价订单功能。查看订单后续的发货情况。
            col1, col2, col3, col4 = st.columns([8, 1, 1, 1])
            cancel_dict = locals()
            goon_dict = locals()
            with col1:
                st.table(temp_pd)
            with col2:
                for i in range(0, len(data)):
                    cancel_dict['cancel' + str(i)] = st.button('退单', key='cancel' + str(i), on_click=cancel_order,
                                                               args=(data[i][0], mysql))
            with col3:
                for i in range(0, len(data)):
                    goon_dict['goon' + str(i)] = st.button('续单', key='goon' + str(i), on_click=goon_order,
                                                           args=(data[i], mysql))

            # for i in range(0, len(data)):
            #     goon_dict['detail' + str(i)] = st.checkbox('详情', key='detail' + str(i))

        temp_pd = pd.DataFrame(list(address_data))
        temp_pd.columns = ['地址编号','地址信息']
        with st.expander('查看地址👈'):
            col1, col2 = st.columns([4, 1])
            address_dict = locals()
            with col1:
                st.table(temp_pd)
            with col2:
                for i in range(0, len(address_data)):
                    cancel_dict['address' + str(i)] = st.button(label='删除', key='address' + str(i),
                                                                on_click=delete_address,
                                                                args=(address_data[i][0], mysql))

            address_text=st.text_input('添加地址', label_visibility='hidden')
            st.button('添加地址', on_click=add_address, args=(address_text, data[0][5], mysql))


# 查看已购买的订单
def cancel_order(order_id, mysql):
    mysql.exec('delete from payment where order_id = ' + str(order_id))
    mysql.exec('delete from consign_info1 where order_id = ' + str(order_id))
    mysql.exec('delete from orders where order_id = ' + str(order_id))



# order_id,number,method,order_date,pro_id,user_id,mer_id
def goon_order(data, mysql):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    consign_data = mysql.findAll(
        'select con_id,se_add,re_add,se_time,consign_amount,get_state from consign_info1 where order_id = ' + str(data[0]))
    # st.write(consign_data)
    consign_data=consign_data[0]
    mysql.exec('update products set stock=stock-' + str(data[1]) + ' where pro_id =' + str(data[4]))
    data_order = {}
    data_order['number'] = data[1]
    data_order['method'] = data[2]  # 1,0
    data_order['order_date'] = now
    data_order['sp_needs'] = '无'
    data_order['pro_id'] = data[4]
    data_order['user_id'] = data[5]
    data_order['mer_id'] = data[6]
    mysql.save('orders', data_order)

    temp_now = now.replace(' ', '').replace(':', '').replace('-', '').strip()
    orderid = mysql.findAll(
        "select order_id from orders where trim(replace(replace(replace(order_date,' ',''),':',''),'-','')) = " + temp_now)[
        0][0]
    # DATE_FORMAT(order_date, '+' % Y - % m - % d % H: % M: % S)
    amount_lag = data[1]
    time_stamp = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=-1)
    consign_setting = consign_data[4]
    if data[2] == 1:
        data_consign = {}
        data_consign['order_id'] = orderid
        data_consign['re_add'] = consign_data[2]
        data_consign['se_add'] = consign_data[1]
        data_consign['se_time'] = time_stamp
        data_consign['mer_id'] = data[6]
        data_consign['user_id'] = data[5]
        data_consign['get_state'] = 0
        data_consign['consign_amount'] = consign_setting
        while (amount_lag - consign_setting) > 0:
            data_consign['se_time'] = datetime.datetime.strftime(time_stamp + datetime.timedelta(days=1),
                                                                 '%Y-%m-%d %H:%M:%S')
            data_consign['consign_amount'] = consign_setting
            mysql.save('consign_info1', data_consign)
            amount_lag = amount_lag - consign_setting

        if amount_lag > 0:
            data_consign['se_time'] = datetime.datetime.strftime(time_stamp + datetime.timedelta(days=1),
                                                                 '%Y-%m-%d %H:%M:%S')
            data_consign['consign_amount'] = amount_lag
            mysql.save('consign_info1', data_consign)

    elif data[2] == 0:
        data_consign = {}
        data_consign['order_id'] = orderid
        data_consign['re_add'] = consign_data[2]
        data_consign['se_add'] = consign_data[1]
        data_consign['se_time'] = time_stamp
        data_consign['mer_id'] = data[6]
        data_consign['user_id'] = data[5]
        data_consign['get_state'] = 0
        data_consign['consign_amount'] = data[1]
        mysql.save('consign_info1', data_consign)


def delete_address(address_id, mysql):
    mysql.exec('delete from address where add_id = ' + str(address_id))


def add_address(address, user_id, mysql):
    data_address = {}
    st.write(address)
    data_address['add_info'] = address
    data_address['user_id'] = user_id
    mysql.save('address', data_address)
