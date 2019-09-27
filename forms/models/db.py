from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Record(Base):
    __tablename__ = "record"
    id = Column(Integer, primary_key=True)
    test_kind = Column(String(2))
    region = Column(String(3))
    year = Column(Integer)
    grade = Column(String(3), default="")
    num = Column(Integer)
    chosen = Column(Integer)
    question_time = Column(Integer)
    operation = relationship("Operation")


class Operation(Base):
    __tablename__ = "operation"
    id = Column(Integer, primary_key=True)
    operation = Column(String(30))
    # 这是上面的操作对应的时间
    datetime = Column(Integer)
    record_id = Column(Integer, ForeignKey("record.id"))


engine = create_engine("sqlite:///foo.db?check_same_thread=False", echo=True)

dbSession = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
