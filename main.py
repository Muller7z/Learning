
import math

from calculate import Calculate
from Tool_new import *


def data_input():
    structure_class = input("请输入结构安全级别(1,2,3):")
    Concrete_Class = input("混凝土标号(C10-C60)：")
    Rebar_Class = input("钢筋标号(如HRB400)：")

    return structure_class,Concrete_Class,Rebar_Class


def rectangle(format_data):
    # data = [[M, Gd, As_],(b,h),(fc,fy,fy_),(a,a_), (Eps_b, P_min, Alpha_1, Alpha_sd)]
    # 矩形截面可以直接调用类中的各种
    # 初始化一个实例对象
    calculate = Calculate(format_data)

    # 未知As'的情况1
    if format_data[0][2] == None :

        # 检查Alpha
        if calculate.Alphas(1) <= calculate.Alpha_sd:
            print("按单筋截面设计")
            Areas = calculate.Areas(2)
            if Areas/(calculate.b + calculate.h0):
                As = Areas
                return As,0
            else:
                As = calculate.Areas(5)
                return As, 0
        else:
            As = calculate.Areas(1)
            As_ = calculate.Areas(0)
            return As,As_
    # 已知As'的情况2
    else:

        if calculate.Alphas(2) <= calculate.Alpha_sd:
            Eps = 1 - math.pow((1 - 2 * calculate.Alphas(2)), 0.5)
            x = Eps*calculate.h0
            if x >= 2*calculate.a_:
                As = calculate.Areas(4)
                return As,0
            else:
                As = calculate.Areas(3)
                return As, 0
        # 超筋了需要增加As'
        else:
            format_data[0][2] = None
            return rectangle(format_data)


if __name__ == '__main__':

    # data = [(M, Gd, As_),(b,h),(fc,fy,fy_),(a,a_), (Eps_b, P_min, Alpha_1, Alpha_sd)]
    pass