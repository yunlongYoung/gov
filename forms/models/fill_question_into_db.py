import os
import json
from PySide2.QtCore import QDir
from db import dbSession, Test_Paper, Num


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


def get_testkind(path: str, times=2):
    return _split(path, times)


def get_region(path: str, times=1):
    return _split(path, times)


def get_year(filename: str):
    """试题年份"""
    return filename[:4]


def get_grade(filename: str):
    """试题级别"""
    if filename[5] == "地":
        return "地市"
    elif filename[5] == "副":
        return "副省"
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
            testkind = get_testkind(path)
            region = get_region(path)
            year = get_year(filename)
            grade = get_grade(filename)
            d = get_json(os.path.join(path, file))
            print(filename, testkind, region, year, grade)
            break
            if filename.endswith("questions"):
                pass
            else:
                pass


put_question_into_db()
