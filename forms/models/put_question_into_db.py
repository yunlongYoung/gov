import os
import json
import pprint
from PySide2.QtCore import QDir
from db import dbSession, Test_Paper, Num

from gen_question_json import gen_all_json


gen_all_json()
session = dbSession()


def get_paths():
    # TODO 将来地区多了需要重新设计
    # TODO 增加所有的json文件夹
    base_dir = QDir.currentPath()
    paths = os.path.join(base_dir, "data", "行测", "国家", "json")
    return (paths,)


def _split(file, n):
    for i in range(n):
        file = os.path.split(file)[0]
    return os.path.split(file)[1]


def get_filename(file: str):
    return os.path.splitext(file)[0]


def get_test_kind(path: str, times=2):
    return _split(path, times)


def get_region(path: str, times=1):
    return _split(path, times)


def get_year(filename: str):
    """试题年份"""
    return filename[:4]


def get_grade(filename: str):
    """试题级别"""
    if "-" in filename:
        return filename.split("-")[1][:2]
    else:
        return None


def get_json(file: str):
    with open(file, encoding="utf-8") as f:
        return json.load(f)


def put_question_into_db():
    paths = get_paths()
    for path in paths:
        for file in os.listdir(path):
            filename = get_filename(file)
            test_kind = get_test_kind(path)
            region = get_region(path)
            year = get_year(filename)
            grade = get_grade(filename)
            questions = get_json(os.path.join(path, file))
            test_paper = Test_Paper(
                test_kind=test_kind, region=region, year=year, grade=grade
            )
            session.add(test_paper)
            session.commit()
            nums = []
            for i in questions:
                # TODO 今后能不能把图片存入数据库
                q = questions[i]["Q"]
                try:
                    a = questions[i]["A"]
                except KeyError:
                    print(file)
                    print(i)
                b = questions[i]["B"]
                c = questions[i]["C"]
                d = questions[i]["D"]
                # TODO paper_id = NULL
                num = Num(
                    paper_id=test_paper.id, num=int(i), question=q, A=a, B=b, C=c, D=d
                )
                nums.append(num)
            session.add_all(nums)
    session.commit()
    session.close()


put_question_into_db()
