from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Test_Paper(Base):
    """真实的试卷
    """

    __tablename__ = "test_paper"
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_kind = Column(String(2))
    region = Column(String(3))
    year = Column(String(4))
    grade = Column(String(2))
    # num = relationship("Num", backref="test_paper")
    # true_paper = relationship("True_Paper", backref="test_paper")
    # virtual_paper = relationship("True_Paper", backref="virtual_paper")


class Num(Base):
    """真实的题号题干选项
    """

    __tablename__ = "num"
    id = Column(Integer, primary_key=True, autoincrement=True)
    paper_id = Column(Integer, ForeignKey("test_paper.id"))
    num = Column(Integer, index=True)
    question = Column(Text)
    # 选项ABCD
    A = Column(Text)
    B = Column(Text)
    C = Column(Text)
    D = Column(Text)


class Num_Property(Base):
    """本题的分类和动态标签
     只会在解析时出现
     动态标签是实现精确分类和精准分析的关键
     所以需要在交卷后分析时加上
    """

    __tablename__ = "num_property"
    num_id = Column(Integer, ForeignKey("num.id"), primary_key=True)
    # 从试卷的大分类到最小的分类
    category_0 = Column(Text)
    category_1 = Column(Text)
    category_2 = Column(Text)


class True_Paper(Base):
    """做的每套真题的记录，包括是否完成信息
    """

    __tablename__ = "true_paper"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 当前试卷
    # 当前题号
    # 当前试卷开始时间，可以查最后时间做的试卷，并且是否完结
    # 当前试卷总用时
    # 是否交卷
    paper_id = Column(Integer, ForeignKey("test_paper.id"))
    start_datetime = Column(Integer, index=True)
    totaltime = Column(Integer)
    last_num = Column(Integer)
    finished = Column(Boolean)


class Virtual_Paper(Base):
    """做的每套练习题的记录，包括是否完成信息
    所有的题号存在Virtual_Num中
    """

    __tablename__ = "virtual_paper"
    id = Column(Integer, primary_key=True, autoincrement=True)
    start_datetime = Column(Integer, index=True)
    totaltime = Column(Integer)
    last_num = Column(Integer)
    finished = Column(Boolean)


class Virtual_Num(Base):
    """每张虚拟试卷的题，由每行的题组成
    """

    __tablename__ = "virtual_num"
    id = Column(Integer, primary_key=True, autoincrement=True)
    virtual_paper_id = Column(Integer, ForeignKey("virtual_paper.id"))
    num_id = Column(Integer, ForeignKey("num.id"))


class Num_Record(Base):
    __tablename__ = "num_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # !既可能是真题，也可能是虚拟试卷
    paper_id = Column(Integer)
    num_id = Column(Integer, ForeignKey("num.id"), index=True)
    chosen = Column(Integer)
    question_time = Column(Integer)
    note = Column(Text)


class Num_Operation(Base):
    __tablename__ = "num_operation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # !既可能是真题，也可能是虚拟试卷
    paper_id = Column(Integer)
    num_id = Column(Integer, ForeignKey("num.id"), index=True)
    # 把操作转换为数字
    # 0: quit query
    # 1: open query
    # 2: previous question
    # 3: next quesiton
    # 4: pause question
    # 6: continue question
    # 8: commit query
    # 9: passive start
    operation = Column(Integer)
    datetime = Column(Integer, index=True)


class Overtime(Base):
    __tablename__ = "overtime"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # !既可能是真题，也可能是虚拟试卷
    paper_id = Column(Integer)
    num_id = Column(Integer, ForeignKey("num.id"), index=True)
    overtime_reason = Column(Integer)


class Wrong(Base):
    # 错误问题
    __tablename__ = "wrong"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # !既可能是真题，也可能是虚拟试卷
    paper_id = Column(Integer)
    num_id = Column(Integer, ForeignKey("num.id"), index=True)
    # TODO 整数转原因
    wrong_reason = Column(Integer)


class Slow(Base):
    # 答的慢的问题
    __tablename__ = "slow"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # !既可能是真题，也可能是虚拟试卷
    paper_id = Column(Integer)
    num_id = Column(Integer, ForeignKey("num.id"), index=True)
    # TODO 整数转原因
    slow_reason = Column(Integer)


class Finished(Base):
    # 答的慢的问题
    __tablename__ = "finished"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # !既可能是真题，也可能是虚拟试卷
    paper_id = Column(Integer)
    num_id = Column(Integer, ForeignKey("num.id"), index=True)
    # TODO 整数转原因
    finished_reason = Column(Integer)


class Guessed(Base):
    # 答的慢的问题
    __tablename__ = "guessed"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # !既可能是真题，也可能是虚拟试卷
    paper_id = Column(Integer)
    num_id = Column(Integer, ForeignKey("num.id"), index=True)
    # TODO 整数转原因
    guessed_reason = Column(Integer)


# engine = create_engine("sqlite:///user_data.db?check_same_thread=False", echo=True)
engine = create_engine("sqlite:///user_data.db?check_same_thread=False")

dbSession = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
