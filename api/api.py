from flask import Flask
import pymysql
import json
import requests
import re
import os
from sqlalchemy import create_engine, true
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import datetime
from minio import Minio
from minio.error import ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists
from minio import Minio, CopyConditions

engine = create_engine('mysql+pymysql://root:root@47.101.168.84:3306/django_test')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()



class FileRec(Base):
    __tablename__ = 'rmp_file'

    id = Column(Integer, primary_key=True)
    easyName = Column(String)
    topicName = Column(String)
    fileName = Column(String)
    filePath = Column(String)
    status = Column(String)
    # createTime = Column(DateTime)
    # updateTime = Column(DateTime)

    def __init__(self, id, easyName, topicName, fileName, filePath, status):
        self.id = id
        self.easyName = easyName
        self.topicName = topicName
        self.fileName = fileName
        self.filePath = filePath
        self.status = status
        # self.createTime = createTime
        # self.updateTime = updateTime

    def dic(self):
        return {
            'id': self.id,
            'easyId': self.easyName,
            'topicId': self.topicName,
            'fileName': self.fileName,
            'filePath': self.filePath,
            'status': self.status,
            # 'createTime': self.createTime,
            # 'updateTime': self.updateTime,
        }

    def save_to_db(self):
        session.add(self)
        session.commit()

    def remove(self):
        session.delete(self)
        session.commit()


# 初始化flask对象
app = Flask(__name__)



@app.route('/query_row_num/')
def query_row_num():
    rows = session.query(FileRec).count()
    return json.dumps(
        {"rows":rows}
    )


@app.route('/query_all/')
def query_all():
    objs = session.query(FileRec).all()
    list = []
    for obj in objs :
        list.append(obj.dic())
    return json.dumps(
        list
    )


# @app.route("/info", methods=["GET", "POST"], endpoint="r_info", defaults={"nid": 100})
@app.route('/query_by_page/<offset>/<limit>')
def query_by_page(offset, limit):
    # objs = session.query(FileRec).pagination(1, 10)
    objs = session.query(FileRec).offset(offset).limit(limit)
    list = []
    for obj in objs :
        list.append(obj.dic())
    return json.dumps(
        list
    )


@app.route('/query_data/<data_id>')
def query_data(data_id):
    """
    根据data_id查询数据
    :param data_id: 数据ID
    :return: 数据结果
    """
    return json.dumps(
        session.query(FileRec).filter_by(id=data_id).first().dic()
    )



if __name__ == '__main__':
    app.run()
    # objs = session.query(FileRec).all()
    # for obj in objs:
    #     print(obj.dic())
