from sqlalchemy import (
    create_engine,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Boolean,
    Enum,
)
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
from .enums import OP


# DEBUG = True
Base = declarative_base()


class Paper(Base):
    """真实的试卷
    """

    __tablename__ = "paper"
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_kind = Column(String(2))
    region = Column(String(3))
    year = Column(String(4))
    grade = Column(String(2))
    # num = relationship("Num", backref="paper")
    # true_paper = relationship("True_Paper", backref="paper")
    # virtual_paper = relationship("True_Paper", backref="virtual_paper")


class Question(Base):
    """真实的题号题干选项分类
    """

    __tablename__ = "question"
    id = Column(Integer, primary_key=True, autoincrement=True)
    paper_id = Column(Integer, ForeignKey("paper.id"))
    num = Column(Integer, index=True)
    question = Column(Text)
    # 选项ABCD
    A = Column(Text)
    B = Column(Text)
    C = Column(Text)
    D = Column(Text)
    finished = Column(Boolean, default=False)
    # 从试卷的大分类到最小的分类
    category_0 = Column(Text)
    category_1 = Column(Text)
    category_2 = Column(Text)


class Record(Base):
    """做的每套真题或练习的记录，包括是否完成信息
    """

    __tablename__ = "record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 当前试卷开始时间，可以查最后时间做的试卷，并且是否完结
    # 当前试卷总用时
    # 当前题号
    # 是否交卷
    is_practice = Column(Boolean)
    max_num = Column(Integer)
    start_datetime = Column(Integer)
    totaltime = Column(Integer, default=0)
    last_v_question_id = Column(Integer, ForeignKey("v_question.id"))
    finished = Column(Boolean, default=False)
    v_questions = relationship("V_Question", backref="record")


class V_Question(Base):
    """每张虚拟试卷(真题或练习)由哪些题组成(相同record的题)
       Vquestion是Virtual_Question的简称
    """

    __tablename__ = "v_question"
    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey("record.id"))
    v_num = Column(Integer)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="v_questions")
    # q_record是单向的关系，因为反向查询不使用
    q_record = relationship("Q_Record")
    q_operations = relationship("Q_Operation", backref="v_question")


class Q_Record(Base):
    """记录问题的已选项、答题时间、note"""

    __tablename__ = "q_record"
    v_question_id = Column(Integer, ForeignKey("v_question.id"), primary_key=True)
    chosen = Column(Integer, default=-1)
    question_time = Column(Integer, default=0)
    note = Column(Text, default="")


class Q_Property(Base):
    """每个虚拟问题的属性，交卷后可以增加动态标签"""

    __tablename__ = "q_property"
    v_question_id = Column(Integer, ForeignKey("v_question.id"), primary_key=True)
    wrong = Column(Boolean)
    slow = Column(Boolean)
    guessed = Column(Boolean)
    overtime = Column(Boolean)


class Q_Operation(Base):
    """记录该问题在面板中的对应操作和时间"""

    __tablename__ = "q_operation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    v_question_id = Column(Integer, ForeignKey("v_question.id"))
    # 把操作转换为数字
    # 0: quit query
    # 1: open query
    # 2: previous question
    # 3: next quesiton
    # 4: pause question
    # 6: continue question
    # 7: goto question
    # 8: commit query
    # 9: passive start
    operation = Column(Enum(OP), nullable=False)
    datetime = Column(Integer, index=True)


# engine = create_engine("sqlite:///user_data.db?check_same_thread=False", echo=True)
engine = create_engine("sqlite:///test.db?check_same_thread=False")

# scoped_session 单例模式
dbSession = scoped_session(sessionmaker(bind=engine))

# if DEBUG:
#     path = Path("D:\\Desktop\\gov\\user_data.db")
#     if path.exists():
#         path.unlink()
Base.metadata.create_all(engine)
