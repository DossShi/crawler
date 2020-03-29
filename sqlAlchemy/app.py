import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqlconnector://root:root@47.101.168.84:3306/django_test')
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


Base.metadata.create_all(engine)

# insert
# obj = User(16, 'chennai',  'man', 1)
# obj.save_to_db()
# obj = User(17, 'Mumbai', 'man', 2)
# obj.save_to_db()
# obj = User(18, 'kolkata', 'woman', 3)
# obj.save_to_db()

obj = FileRec(None, 'kolkata', 'woman', '435', 'path', '1')
obj.save_to_db()

# list all
objs = session.query(FileRec).all()
for obj in objs:
    print(obj.dic())

# # update
# obj = session.query(FileRec).filter_by(id=16).first()
# obj.id = 4
# obj.save_to_db()
#
# # list all
# objs = session.query(FileRec).all()
# for obj in objs:
#     print(obj.dic())
#
# # delete
# obj = session.query(FileRec).filter_by(id=4).first()
# obj.remove()