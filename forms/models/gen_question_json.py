"""
将txt的题目读入几个字典，题目字典
题目字典的key从1到140，每道题的题目都在里面，包括图片
所以这就要求手动把图片输入成html放到题目中，并且设置好图片地址
结束之后，把题目生成的html字典存储到json中

如果存在对应题目的json，则读入字典
没有的话就生成字典，生成后存储到对应位置

命名规则
试卷名+txt，试卷名+json，试卷名+题号+图片序号
文件夹，国家或者山东省——18、19等
"""
import os
import re
import json

# from pprint import pprint

BASE = r"d:\Desktop\gov\data\行测"


# 测试是否可以找出公用的题干，使用xx～xx题来辨别
# import re
# DIR = r"d:\Desktop\gov\data\行测\国家\txt\2007.txt"
# pattern = re.compile(r'\d+～\d+题')
# with open(DIR, encoding='utf-8') as f:
#     for line in f:
#         if re.search(pattern, line.strip()):
#             print(line)

# 在data这个文件夹下，有行测
# 在行测文件夹中寻找所有的分类，作为题目分类标签，也就试卷名字典
# 类似行测——国家——txt——，搜索文件夹下所有的txt作为试卷名
# 试卷名为行测-国家-2019-副省级

# 对于每张试卷，搜索1到140题，直到结束
# 然后把这个结构存储在json中
# 也就是在国家文件夹下，创建一个json文件夹，主要是试卷


# 输入输出
# 输入为一组真题txt
# 输出为一组json文件，每个文件是一个字典，字典的键是题号，内容是题干包括选项

# 输入为一个真题txt
# 输出为一个json文件，json的名字同真题的名字
# 每个json文件是一个字典，字典的键是题号，内容是题干包括选项

# 读入一个真题txt
# 逐行进行判断
# 从题号n开始，检查该题是否有综合或者资料分析的情况，n默认为50，2019开始有复合题


# TODO 不太重要：题号1前面是题目要求prefix，遇到题号1前的都存入prefix
# 如果先找到了~，则为资料背景。把上题结束到~行之前的部分设置为上一题，~行开始的部分都设置为背景资料，然后把下面5道题的背景都设置为它
# 如果先找到了题号，则为普通题，继续寻找下一道题，并把这些缓存中的部分都设置为上题题干
# 如果什么都没找到，则打印剩下的部分，并且把剩余的所有部分设置为上一个题号的题干
# 还有可能是题目要求，如果已经找到了选项D，但是本题的题干还没有结束，可能是题目要求，可以放在下一道题的背景UI中，优先于背景资料
# {1:'扽狂三疯狂单色房东反对三', 2:'另囧扽反对房东  房东 ', backgroud:{125:'赛蓝发动蓝发动蓝看发动机', 126:'塞拉芬KDJ森林东讲课'}}

# 从上个json中，或者字典中，再次分析选项
# 如果以A.开头，则查找B，如果找到，把B前面的都归到A选项，以此类推
# 如果已经找到了D选项，则D选项是D.所在的一行
# 如果D所在的一行结束后，后面还有几行，则属于答题要求

# 从1到140，开始寻找'^\s*{i}+[.|．]'
# if pat.match(line):
#     # 第i题开始
#     读取下一行
#     如果是'^\s*A[.|．]'，则选项开始，开始读取选项
#     如果本行
#     如果是pat(i+1)，则下题开始，开始读取下题

# 读取选项：
#     寻找B，如果本行没有B，则存入A选项
#     下行.之后的存入B，下行.之后的存入C，下行.之后的存入D
#     寻找下一个题号，i加1，continue
#     并且寻找~的背景资料
#     寻找到题号前的内容全部放弃

# 把循环转换为函数调用：
#     寻找题号i
#     找到题号后，寻找选项
#     找到选项A之前的内容放入题干

# 寻找选项：
#     开始寻找A.
#     找到A.后，将之前的缓冲存入题干
#     开始读取选项


# 从50题开始（找到题号50后），找到选项D后，要同时寻找背景和题号
# 不分先后，因为他们都可能先出现
# current_num就是上次find_question_num找到的num

# 开始同时查找

# 现在又出现一个问题，关于f.readline的问题，因为现在每个函数里面有自己的readline的话，整个流程不好控制
# 怎么样把逻辑独立出来

# 再来理一遍逻辑

# 首先打开一个txt文件，需要输出一个字典，然后对字典需要做二次处理
# 然后字典存到json，json的文件名和txt相同

# 然后决定读入文件的方式，因为是正则匹配，要一行一行过
# 那么使用readline的方式最好。

# 但是现在列出的代码，对于流程控制不是很好，分支结构也不好。

# 现在读取文件的第一行，当readline的结果不为真时，
# 则停止此文件的匹配，所以必须要有个退出流程的控制，
# 流程控制的标识是readline不为真，那么在大的循环流程中，
# 必须有line这个变量，这个变量值控制是否退出这个循环（while循环）
# 题号判断、题干判断、选项判断、背景判断、其他部分可以丢弃

# 第1题题号前都丢弃，
# 第1题题号之后是题干
# 题干之后是选项
# 选项ABC
# 选项D下一行开始有可能有背景
# 背景在下一题题号前

# 当题号大于49时，需要在前一题的选项结束时，判断是否有背景资料
# 如果从每一行直接判断时，
# 题号可以直接确定、选项可以直接确定，其他都要靠区间法
# 如果是普通文字（什么都没匹配到），那么如果它的位置在题号后，在选项前，则为题干
# 如果它的位置在选项后，则有可能是题目要求或者背景，需要使用~判断
# 在~之后，就只能是题号
# 有的题不规则，则需要把题弄成规则的，比如图片的，最好在txt里改成img的链接
# 把选项也转换过来。
# 不然会造成一定的麻烦
# 也就是，如果格式化原数据标准比较容易的话，最好先格式化，不然清洗算法会很复杂。


def find_question():
    _num = re.compile("^\s*(\d+)[\.|．]")
    _A = re.compile("^\s*A[\.|．](.*)")
    _B = re.compile("\s*B[\.|．]")
    _C = re.compile("\s*C[\.|．]")
    _D = re.compile("\s*D[\.|．]")
    # bg为背景材料，background的缩写
    _bg = re.compile("(\d+)[~|～](\d+)")
    bg_range = []
    questions = {}
    options = {}

    def get_files(base=BASE):
        files = []
        test_names = {"行测": {}}
        for area in os.listdir(base):
            path = os.path.join(base, area, "txt")
            if path not in test_names["行测"]:
                test_names["行测"][area] = []
            for f in os.listdir(path):
                files.append(os.path.join(path, f))
                test_names["行测"][area].append(os.path.splitext(f)[0])
        return files, test_names

    files, test_names = get_files()

    def handle_num_line(line, num):
        current_num = int(num.group(1))
        if current_num not in questions:
            questions[current_num] = ""
        else:
            questions[current_num] += "<br><br><br>"
        questions[current_num] += _num.split(line)[2]  # q is for question，题干
        return current_num

    def abcd_in_4_lines(f, a, current_num):
        # 属于ABCD各一行的
        options[current_num] = []
        options[current_num].append("A. " + a)
        line = f.readline()
        options[current_num].append("B. " + _B.split(line, 1)[1].strip())
        line = f.readline()
        options[current_num].append("C. " + _C.split(line, 1)[1].strip())
        line = f.readline()
        options[current_num].append("D. " + _D.split(line, 1)[1].strip())

    def abcd_in_2_lines(f, a, b, current_num):
        # 属于ABCD各一行的
        options[current_num] = []
        options[current_num].append("A. " + a)
        options[current_num].append("B. " + b)
        line = f.readline()
        line = _C.split(line, 1)[1]
        c, d = _D.split(line, 1)
        options[current_num].append("C. " + c)
        options[current_num].append("D. " + d)

    def abcd_in_1_line(a, b, current_num):
        # ABCD在同一行的处理
        b, c = _C.split(b, 1)
        c, d = _D.split(c, 1)
        options[current_num] = []
        options[current_num].append("A. " + a)
        options[current_num].append("B. " + b)
        options[current_num].append("C. " + c)
        options[current_num].append("D. " + d)

    for file in files:
        # print(file)
        # 在与txt同目录的json目录中生成同名的json文件
        dirname = os.path.dirname(file)
        jsondir = os.path.join(os.path.dirname(dirname), "json")
        filename = os.path.basename(file).split(".")[0]
        questions_json = os.path.join(jsondir, filename + "_questions.json")
        options_json = os.path.join(jsondir, filename + "_options.json")
        current_num = 0  # 当前题号
        pos = 0
        with open(file, encoding="utf-8") as f, open(
            questions_json, "w", encoding="utf-8"
        ) as g, open(options_json, "w", encoding="utf-8") as h:
            while 1:
                line = f.readline()
                if pos is 0:  # 寻找题号，上题选项后、背景资料题号后
                    num = _num.match(line)
                    backgroud = _bg.search(line)
                    if num:
                        # print(file)
                        current_num = handle_num_line(line, num)
                        pos = 1
                    elif backgroud:
                        beg, end = backgroud.groups()
                        bg_range = [i for i in range(int(beg), int(end) + 1)]
                        for i in bg_range:
                            questions[i] = {}
                            # 把background也合并到question里
                            questions[i] = ""
                        # print(bg_range)
                        pos = 2
                elif pos is 1:  # 寻找选项，本题题号后，题干中
                    a = _A.match(line)
                    if a:
                        a = a.group(1)
                        if _B.search(a):
                            a, b = _B.split(a, 1)
                            if _C.search(b):
                                abcd_in_1_line(a, b, current_num)
                            else:
                                abcd_in_2_lines(f, a, b, current_num)
                        else:
                            abcd_in_4_lines(f, a, current_num)
                        pos = 0
                    else:
                        # line属于题干
                        questions[current_num] += "<br>" + line
                elif pos is 2:  # 寻找下题题号，背景资料中
                    num = _num.match(line)
                    if num:
                        # print(file)
                        current_num = handle_num_line(line, num)
                        pos = 1
                    else:  # 这些是背景或者题目要求
                        for i in bg_range:
                            # 把background也合并到question里
                            questions[i] += "<br>" + line
                if not line:
                    break
            json.dump(questions, g, ensure_ascii=False)
            json.dump(options, h, ensure_ascii=False)


find_question()
