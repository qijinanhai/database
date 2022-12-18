import datetime
import re
import time
import pandas as pd

from MySqlUtils import MysqlClass
from sqlSettings import *

class DataGenerate:
    def __init__(self):

        self.mysql = MysqlClass(server=MYSQL_SERVER_IP,
                                port=MYSQL_SERVER_PORT,
                                user=MYSQL_USER_NAME,
                                password=MYSQL_USER_PWD,
                                db_name=MYSQL_DB_NAME)
        # self.firm_names = [x[4] for x in self.mysql.findAll("select * from {}".format(MYSQL_STOCK_FIRM_TABLE_NAME))]