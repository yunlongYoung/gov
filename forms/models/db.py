from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Test_Paper(Base):
    """试卷的抽象，和Num放在一起也可以
    分离开比较简单方便
    """

    __tablename__ = "test_paper"
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_kind = Column(String(2), default="行测")
    region = Column(String(3), default="国家")
    year = Column(String(4))
    grade = Column(String(3), default="")


class Num(Base):
    """问题的抽象，包括题号、题干、选项
    还包括问题的分类、标签等
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
    """ 因为刚开始打开试卷时，不需要读取分类和标签
    只有后面交卷后才需要分析，所以可以和试卷分开
    增加一个Num_Property
    # ! 如果这个可以动态增加就好了
    """

    num_id = Column(Integer, ForeignKey("num.id"), primary_key=True)
    # 从试卷的大分类到最小的分类
    category_0 = Column(Text)
    category_1 = Column(Text)
    category_2 = Column(Text)
    # 这些标签只会在解析时出现
    # 这个是实现精确分类和精准分析的关键
    # ! 进行交卷分析时，需要打上错误，未做，已做，蒙的，地区（国考或四川、山东、湖北等标签）
    # ! 这些提前能想到的是否直接做成表，可以存储其他信息，比如wrong，overtime等
    finished = Column(Text)
    guessed = Column(Text)
    # ! 根据需要增加，分为考试属性和固有属性


class True_Paper(Base):
    """这个表用于存放做过的真题记录
    也就是一套一套做的卷子，
    而不是练习模式或者专项模式做的
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
    totaltime = Column(Integer, primary_key=True)
    last_num = Column(Integer)
    finished = Column(Boolean, default=False)


class Virtual_Paper(Base):
    # TODO 如何保存练习题的信息，从几套题中抽取的几道题
    # TODO 必须把current和virtual_paper分离
    # 当前在做的试卷信息
    __tablename__ = "virtual_paper"
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_num = Column(Integer)
    start_datetime = Column(Integer, index=True)
    totaltime = Column(Integer, primary_key=True)
    finished = Column(Boolean, default=False)


class Virtual_Num(Base):
    """存放所有曾经生成过的虚拟试卷，比如专项练习等
    意思是这张虚拟试卷的题，由这些题组成
    """

    __tablename__ = "virtual_num"
    id = Column(Integer, primary_key=True, autoincrement=True)
    virtual_paper_id = Column(Integer, ForeignKey("virtual_paper.id"))
    num_id = Column(Integer, ForeignKey("num.id"))


class Num_Record(Base):
    # ! 题号经过抽象，比如练习题中的题号不一定是真题中的题号
    __tablename__ = "num_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # ! 难点是这是张虚拟试卷呢，还是真题呢
    # ! 难道说不能用外键吗，只能存Integer吗
    paper_id = Column(Integer)
    num_id = Column(Integer, ForeignKey("num.id"), index=True)
    chosen = Column(Integer, default=-1)
    question_time = Column(Integer, default=0)
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


engine = create_engine("sqlite:///user_data.db?check_same_thread=False", echo=True)

dbSession = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
