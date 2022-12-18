import numpy as np
import streamlit as st

class MultiPage:
    def __init__(self):
        self.page=[]

    def add_page(self,title,func):
        self.page.append(
            {
                'title': title,
                'function': func
            }
        )

    def run(self):
        page=st.sidebar.selectbox(
            'menu',
            self.page,
            format_func=lambda page:page['title']
        )
        page['function']()