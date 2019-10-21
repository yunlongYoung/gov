import os
import json
import pprint
from PySide2.QtCore import QDir
from db import dbSession, Paper, Question

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
        return ""


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
            test_paper = Paper(
                test_kind=test_kind, region=region, year=year, grade=grade
            )
            session.add(test_paper)
            session.commit()
            question_dict = get_json(os.path.join(path, file))
            questions = []
            for i in question_dict:
                # TODO 今后能不能把图片存入数据库
                q = question_dict[i]["Q"]
                try:
                    a = question_dict[i]["A"]
                except KeyError:
                    print(file)
                    print(i)
                b = question_dict[i]["B"]
                c = question_dict[i]["C"]
                d = question_dict[i]["D"]
                # TODO paper_id = NULL
                question = Question(
                    paper_id=test_paper.id, num=int(i), question=q, A=a, B=b, C=c, D=d
                )
                questions.append(question)
            session.add_all(questions)
    session.commit()
    session.close()


put_question_into_db()