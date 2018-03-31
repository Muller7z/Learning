
import math

from test import *


def Condition_ONE(M,b,h,Fc,Fy,Fy_,Alpha_s_d,Eps_b):
    a = float(input("下保护层厚度a(mm):"))
    a_ = float(input("上保护层厚度a(mm):"))
    As_ = 0
    h0 = h - a
    Alpha_s = M/(Fc*b*h0*h0)
    # print(Alpha_s)
    # print(Alpha_s_d)
    Eps = 1 - math.pow((1 - 2 * Alpha_s), 0.5)
    if Alpha_s <= Alpha_s_d:
        print("可按单筋截面设计")
        # Eps = 1 - math.pow((1 - 2 * Alpha_s), 0.5)
        As = (Fc*b*Eps*h0)/Fy
        P_min = input("请输入最小配筋率：")
        if As/(b*h0) >= P_min:
            print("满足最小配筋率要求")
            save(As, As_, a, a_)
        else:
            print("不满足最小配筋率要求")
            print("As=pmin*b*h0")
            AREAs = P_min*b*h0
            AREAs_ = As_
            save(AREAs, AREAs_, a, a_)
    else:
        print("不满足单筋截面设计，需采用双筋截面")
        Alpha_s = Alpha_s_d
        As_ = (M-(Alpha_s_d*Fc*b*h0*h0))/(Fy_*(h0-a_))
        print("按DL/T5057-2009取a1=1.0")
        print("按SL191-2008取a1=0.85")
        a1 = float(input("请输入α1():"))
        As = (Fc*b*Alpha_s*a1*Eps_b*h0)/(Fy)

        save(As, As_, a, a_)


def Condition_TWO(M,b,h,Fc,Fy,Fy_,As_,Alpha_s_d,Eps_b):
    # 情况一
    a = float(input("下保护层厚度a(mm):"))
    a_ = float(input("上保护层厚度a(mm):"))
    h0 = h-a
    Alpha_s = (M-Fy_*As_*(h0-a_))/(Fc*b*h0*h0)
    if Alpha_s_d >= Alpha_s:
        print("受压区配筋率满足要求")
        Eps = 1 - math.pow((1-2*Alpha_s),0.5)
        x = Eps*h0
        if x>= 2*a_:
            print("受压筋已充分发挥")
            AREAs = (Fc*b*h0 + Fy_*As_)/(Fy)
            AREAs_ = As_
            save(AREAs,AREAs_, a, a_)

        else:
            print("受压筋未充分发挥")
            AREAs = M/(Fy*(h0-a_))
            AREAs_ = As_
            save(AREAs, AREAs_, a, a_)
    else:
        print("超筋了，需要增加As',转入情况1")
        # Fc, Fy, Fy_, Alpha_s_d, Eps_b = check(Concrete_Class, Rebar_Class)
        Condition_ONE(M,b,h,Fc,Fy,Fy_,Alpha_s_d,Eps_b)


if __name__ == '__main__':
    Moment_Design = float(input("请输入弯矩设计值(kN/m)："))
    M = Moment_Design * 1000
    Concrete_Class = input("混凝土标号：")
    Rebar_Class = input("钢筋标号：")
    Fc,Fy,Fy_,Alpha_s_d, Eps_b = check(Concrete_Class,Rebar_Class)
    Breadth = float(input("请输入设计截面宽度(mm):"))
    b = Breadth * 0.001
    Height = float(input("请输入设计截面高度(mm):"))
    h = Height * 0.001
    Area_s_ = float(input("请输入受压区面积As(mm²),欲求则输入0："))
    As_ = Area_s_ * 0.001 * 0.001
    if Area_s_ != 0:
        print("As不等于0，转入情况2")
        Condition_TWO(M,b,h,Fc,Fy,Fy_,As_,Alpha_s_d,Eps_b)
    else:
        print("As等于0，转入情况1")
        Condition_ONE(M,b,h,Fc,Fy,Fy_,Alpha_s_d,Eps_b)

