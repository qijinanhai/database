import streamlit as st
import pandas as pd

from sqlSettings import *
import MySqlUtils
import pages.seller_search as seller_search

def app():
    user_id = st.text_input('user_id')
    sell_id = st.text_input('sell_id')
    option1 = st.checkbox('👈点击查询1')
    if option1:
        seller_search.click_btn_merchant(user_id, sell_id)
# def click_btn_merchant(user_id, sell_id):


