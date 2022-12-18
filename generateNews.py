import datetime
import re
import time

from tqdm import tqdm

from MySqlUtils import MysqlClass
# from sqlSettings import *


def remove_html_label(sentence):
    sentence = re.sub(r'\s*', '', sentence)
    sentence = re.sub(r'<.*?>', '', sentence)
    return sentence


def merge_news(news_df):
    # 15：00以后归到后一天
    # news_df['date'] = news_df.apply(self.correct_date, axis=1).astype(str)
    # 合并同一天的新闻
    news_df = news_df.groupby(['date', 'code'])['news'].apply(lambda x: '。'.join(x.values)).reset_index()
    return news_df


def correct_date(df):
    if df['time'] > '150000':
        return df['date'] + datetime.timedelta(days=1)
    else:
        return df['date']


class DataGenerate:
    def __init__(self):

        self.mysql = MysqlClass(server=MYSQL_SERVER_IP,
                                port=MYSQL_SERVER_PORT,
                                user=MYSQL_USER_NAME,
                                password=MYSQL_USER_PWD,
                                db_name=MYSQL_DB_NAME)
        self.firm_names = [x[4] for x in self.mysql.findAll("select * from {}".format(MYSQL_STOCK_FIRM_TABLE_NAME))]

    def get_news_content(self, code, start, end):
        res = self.mysql.findAll(
            "select code,time,content from {} where code='{}' and time between '{}' and '{}'".format(
                MYSQL_STOCK_NEWS_CONTENT_TABLE_NAME, code, start, end))
        date = [x[1].strftime('%Y-%m-%d') for x in res]
        news_contents = [remove_html_label(x[2]) for x in res]
        codes = [code for _ in range(len(date))]
        feature_df = pd.DataFrame({'code': codes, 'date': date, 'news': news_contents})
        return merge_news(feature_df)

    def remove_redun(self, text, max_firm=5):
        # 去除公司名大于5的新闻
        count = 1
        for name in self.firm_names:
            if name in text:
                count += 1
                if count > max_firm:
                    text = ''
                    break
        return text

    def group_firm_daily(self, code, start_date, end_date):
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        sql_col_name = "time, open, close, high, low, turnoverRatio, volume, pb, pe"
        res = self.mysql.findAll(
            "select {} from {} where code='{}' and time between '{}' and '{}'".format(sql_col_name,
                                                                                      MYSQL_STOCK_DAILY_TABLE_NAME,
                                                                                      code,
                                                                                      start_date, end_date))
        column_names = ['date', 'open', 'close', 'high', 'low', 'turnoverRatio', 'volume', 'pb', 'pe']
        codes = pd.DataFrame([code for _ in range(len(res))], columns=['code'])
        feature_df = pd.DataFrame(list(res), columns=column_names)
        feature_df = pd.concat([codes, feature_df], axis=1)
        # feature_df['time'] = feature_df['time'].apply(str).str.replace("-", "")
        feature_df.dropna(inplace=True)
        feature_df['close_shift'] = feature_df['close'].astype(float).shift(-1)
        feature_df['is_rise'] = (feature_df['close_shift'] - feature_df['close'].astype(float)) > 0
        feature_df['is_rise'] = feature_df['is_rise'].map(lambda x: 1 if x else 0)
        feature_df.drop(columns=['close_shift'], axis=1, inplace=True)
        return feature_df


def main(start, end):
    sh = pd.read_csv('沪深300-2020.csv', converters={'代码': str}).iloc[:, 0]
    dataGenerate = DataGenerate()
    news_df = pd.DataFrame()
    stock_df = pd.DataFrame()
    print('***** Read from mysql *****')
    time.sleep(0.1)
    for code in tqdm(sh):
        news_df = pd.concat([news_df, dataGenerate.get_news_content(code, start, end)])
        stock_df = pd.concat([stock_df, dataGenerate.group_firm_daily(code, start, end)])
    stock_df.to_csv('./data/stock.csv', index=False)
    news_df.to_csv('./data/news.csv', index=False)


if __name__ == "__main__":
    main("2021-01-01", "2021-02-01")