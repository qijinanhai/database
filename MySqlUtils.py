# coding:utf-8

import pymysql


class MysqlClass:

    def __init__(self, server, port, user, password, db_name):
        self.port = port
        self.sql_address = server
        self.db_name = db_name
        self.user = user
        self.pwd = password

    def connect_db(self):
        mydb = pymysql.connect(host=self.sql_address, port=self.port, user=self.user, password=self.pwd,
                               db=self.db_name, charset='utf8')
        return mydb

    def exec(self, sql):
        conn = self.connect_db()
        cs1 = conn.cursor()
        cs1.execute(sql)
        conn.commit()
        cs1.close()
        conn.close()
        return True

    def save(self, table, data):
        conn = self.connect_db()
        fields = self.getFields(data)
        value = self.getValue(data)
        sql = "INSERT INTO %s(%s) VALUES (%s)" % (table, fields, value)
        cs1 = conn.cursor()
        cs1.execute(sql)
        conn.commit()
        cs1.close()
        conn.close()
        return True

    def getValue(self, data):
        value = ''
        for key in data:
            v = str(data[key])
            if value == '':
                value = "'" + v + "'"
            else:
                value = value + ",'" + v + "'"
        return value

    def getFields(self, data):
        fields = ""
        for key in data:
            if fields == '':
                fields = '`' + key + '`'
            else:
                fields = fields + ",`" + key + '`'
        return fields

    def saveMany(self, table, data):
        if len(data) <= 0:
            return True
        conn = self.connect_db()
        cursor = conn.cursor()
        fields = self.getFields(data[0])
        is_true = True
        preSql = 'insert into ' + table + ' (' + fields + ') values '
        sqllist = []
        i = 1
        strdata = ""
        for val in data:
            re = self.getValue(val)
            if i % 1000 == 0:
                sqllist.append(strdata)
                strdata = ''
            if strdata == '':
                strdata = "(%s)" % (re)
            else:
                strdata = strdata + ",(%s)" % (re)
            i += 1
        if strdata != '':
            sqllist.append(strdata)
        try:
            for m in range(0, len(sqllist)):
                sql = preSql + sqllist[m]
                cursor.execute(sql)
            conn.commit()
        except Exception as e:
            is_true = False
            print(str(e))
            conn.rollback()
        cursor.close()
        conn.close()
        return is_true

    def findLastOne(self, table):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * from %s order by id desc limit 1" % (table))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data

    def findOne(self, sql):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data

    def findAll(self, sql):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
