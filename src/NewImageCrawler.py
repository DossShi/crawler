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




def saveAndDownloan(html, path, easyName, topicName, fileName, filePath):
    status = save(html, path)
    checkBucketExist(bucketName);
    uploadFile(bucketName, filePath + fileName, filePath + fileName)
    fileRec = FileRec(None, str(easyName), str(topicName), str(fileName), str(filePath), 1 if status == True else 0)
    fileRec.save_to_db()



minioClient = Minio('47.101.168.84:9000',
                    access_key='minioadmin',
                    secret_key='minioadmin',
                    secure=False)
bucketName = "resource"


# 检查Bucket是否存在
def checkBucketExist(bucketName) :
    if minioClient.bucket_exists(bucketName) :
        pass
    else :
        try:
            minioClient.make_bucket(bucketName)
        except BucketAlreadyOwnedByYou as err:
            pass
        except BucketAlreadyExists as err:
            pass
        except ResponseError as err:
            raise

def uploadFile(bucketName, cloudPath, loaclPath):
    try:
        while cloudPath.startswith('/'):
            cloudPath = cloudPath.replace('/', '', 1)
        minioClient.fput_object(bucketName, str(cloudPath).encode('utf-8'), str(loaclPath))
    except ResponseError as err:
        print(err)


def save(html, path):
    '''
    以文件形式保存数据
    :param html: 要保存的数据
    :param path: 要保存数据的路径
    :return:
    '''
    try:
        # 判断目录是否存在
        if not os.path.exists(os.path.split(path)[0]):
            # 目录不存在创建，makedirs可以创建多级目录
            os.makedirs(os.path.split(path)[0])
        # 保存数据到文件
        with open(path, 'wb') as f:
            f.write(html)
        print('保存成功')
        return True
    except Exception as e:
        print('保存失败', e)
        return False



parent_url = 'http://p3.csgfnmdb.pw/pw/'

url = '要爬的网址'


# 浏览器请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}




# group = (14,15,16,49,114,21)
group = ('15', '16', '21', '49')
for g in group:
    print(g)
    group_url = url + g
    for i in range(1, 2):
        # 分类页翻页
        cur_url = group_url + '&page=' + str(i)
        response = requests.get(cur_url)
        # response = requests.get(url, headers = headers)
        response.encoding = 'utf-8'

        # 分类页
        result = re.findall('<a href="html_data/(.*?)" id="', response.text)
        print(len(result))
        print(result)
        for r in result:
            # 详情页
            page_url = parent_url + "html_data/" + r
            page_response = requests.get(page_url)
            page_response.encoding = 'utf-8'
            # print(page_response.text)
            title = re.findall('<span id="subject_tpc">(.*?)</span>', page_response.text)
            print(title)
            img_result = re.findall('<img src="(.*?)" border="0"', page_response.text)
            print(img_result)
            for img in img_result:
                # 图品
                path = '/image/' + g + '/' + str(i) + '/' + str(title) + '/'
                name = img.split('/')[-1]
                name = str.replace(name, '\'', '')
                response_image = requests.get(img)
                response_image.encoding = 'utf-8'
                # save(response_image.content, path + name)
                saveAndDownloan(response_image.content, path + name, title, group, name, path)
                break
            break
        break
    break

