import os
import json
from PySide2.QtCore import QDir
from forms.models import dbSession, Test_Paper, Num


session = dbSession()

base_dir = QDir.currentPath()


def get_paths():
    # TODO 将来地区多了需要重新设计
    # TODO 增加所有的json文件夹
    paths = os.path.join(base_dir, "data", "行测", "国家", "json")
    return paths


def get_grade(filename):
    if filename[5] == "地":
        return "地市"
    elif filename[5] == "副":
        return "副省"
    else:
        return None


def put_question_into_db():
    paths = get_paths()
    for path in paths:
        for file in os.listdir(path):
            with open(file, encoding="utf-8") as f:
                d = json.load(f)
            filename = os.path.splitext(file)[0]
            year = get_year(filename)
            grade = get_grade(filename)
            if filename.endswith("questions"):
                pass
            else:
                pass
