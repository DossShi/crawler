from flask import Flask
import pymysql
import json


# 初始化flask对象
app = Flask(__name__)


def get_conn():
    """
    获取数据库的链接
    :return:
    """
    return pymysql.connect(
        host='47.101.168.84',
        user='root',
        password='root',
        database='django_test',
        charset='utf8'
    )


def query_mysql_data(data_id):
    """
    查询MySQL数据
    :return: data
    """
    conn = get_conn()
    sql = f"""
        select * from user where id={data_id}
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.close()
    return cursor.fetchall()


@app.route('/query_data/<data_id>')
def query_data(data_id):
    """
    根据data_id查询数据
    :param data_id: 数据ID
    :return: 数据结果
    """
    return json.dumps(
        query_mysql_data(data_id)
    )


if __name__ == '__main__':
    app.run()