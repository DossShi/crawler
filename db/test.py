import pymysql

conn=pymysql.connect(
    host='47.101.168.84',
    user='root',
    password='root',
    database='django_test',
    charset='utf8'
)

# 从conn得到cursor对象
cursor = conn.cursor()
# 执行SQL语句
sql = "select * from user"
cursor.execute(sql)
# 获取结果
datas = cursor.fetchall()

for data in datas:
    print(data)

# 释放cursor
cursor.close()

# 释放连接
conn.close()