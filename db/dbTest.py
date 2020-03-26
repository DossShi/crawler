import db


# 1、查询数据列表
query_sql = "select * from user"
datas = db.query_data(query_sql)
for data in datas:
    print(data)


# 2、新增一条数据
insert_sql = """
        insert user (name, sex, age, email)
        values('mayi', 'man', 20, 'mayi@qq.com')
    """
db.insert_or_update_data(insert_sql)


# 3、更新一条数据
update_sql = "update user set name='1234' where id=3"
db.insert_or_update_data(update_sql)


# 1、查询数据列表
query_sql = "select * from user"
datas = db.query_data(query_sql)
for data in datas:
    print(data)
