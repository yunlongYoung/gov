import json
from pathlib import Path
from PySide2.QtCore import QDir
from .db import dbSession, Paper, Question
from .gen_question_json import gen_all_json


gen_all_json()
session = dbSession()


def get_paths():
    # TODO 将来地区多了需要重新设计
    # TODO 增加所有的json文件夹
    base_dir = Path(QDir.currentPath())
    paths = base_dir / "data" / "行测" / "国家" / "json"
    return (paths,)


def parents_stem(path, i):
    return path.parents[i].stem


def get_filename(file):
    return file.stem


def get_test_kind(file, i=2):
    return parents_stem(file, i)


def get_region(file, i=1):
    return parents_stem(file, i)


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


def fill_db_with_questions():
    paths = get_paths()
    for path in paths:
        for file in path.iterdir():
            filename = get_filename(file)
            test_kind = get_test_kind(file)
            region = get_region(file)
            year = get_year(filename)
            grade = get_grade(filename)
            test_paper = Paper(
                test_kind=test_kind, region=region, year=year, grade=grade
            )
            session.add(test_paper)
            session.commit()
            question_dict = get_json(file)
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


if __name__ == "__main__":
    fill_db_with_questions()
