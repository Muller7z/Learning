
import math

from tool import *


def Condition_ONE(M,Gd,P_min,b,h,Fc,Fy,Fy_,As_,Alpha_s_d,Eps_b):
    # 情况一
    a = float(input("下部受拉筋至底边缘距离 a(mm):")) * 0.001
    a_ = float(input("上保护层厚度a'(mm):")) * 0.001
    h0 = h - a
    print("h0 = %smm" % format_output(h0 * 1000))
    Alpha_s = (Gd*M)/(Fc*b*h0*h0)
    print("αs = %s" % format_output(Alpha_s))

    if Alpha_s <= Alpha_s_d:
        print("αs=%s <= αsa=%s"%(format_output(Alpha_s),Alpha_s_d))
        print("可按单筋截面设计")
        Eps = 1 - math.pow((1 - 2 * Alpha_s), 0.5)
        print("ε = %s" % format_output(Eps))
        As = (Fc*b*Eps*h0)/Fy
        print("As=%smm²"%format_output(As*1000*1000))
        if As/(b*h0) >= P_min*0.01:
            print("配筋率As/bh0 = %s >= P_min = %s" %(format_output((As / (b * h0))*100),Pmin))
            print("满足最小配筋率要求")
            AREAs = As
            AREAs_ = As_
            # 请注意
            # 传入这个函数的参数不是标准单位，因为要方便调试这个函数
            save(AREAs * 1000 * 1000, AREAs_ * 1000 * 1000, a * 1000, a_ * 1000)
        else:
            print("配筋率As/bh0 = %s < P_min = %s" % (format_output(As / (b * h0)),Pmin))
            print("不满足最小配筋率要求")
            print("按As=pmin*b*h0 计算")
            AREAs = P_min*b*h0
            AREAs_ = As_
            # 请注意
            # 传入这个函数的参数不是标准单位，因为要方便调试这个函数
            save(AREAs * 1000 * 1000, AREAs_ * 1000 * 1000, a * 1000, a_ * 1000)
    else:
        print("αs=%s > αsa=%s" % (format_output(Alpha_s), Alpha_s_d))
        print("不满足单筋截面设计，需采用双筋截面")
        Alpha_s = Alpha_s_d
        print("αs = %s" % format_output(Alpha_s))
        As_ = (Gd*M-(Alpha_s_d*Fc*b*h0*h0))/(Fy_*(h0-a_))
        print("按DL/T5057-2009取a1=1.0")
        print("按SL191-2008取a1=0.85")
        a1 = float(input("请输入α1:"))
        As = (Fc*b*a1*Eps_b*h0+Fy_*As_)/(Fy)
        AREAs = As
        AREAs_ = As_
        # 请注意
        # 传入这个函数的参数不是标准单位，因为要方便调试这个函数
        save(AREAs * 1000 * 1000, AREAs_ * 1000 * 1000, a * 1000, a_ * 1000)


def Condition_TWO(M,Gd,Pmin,b,h,Fc,Fy,Fy_,As_,Alpha_s_d,Eps_b):

    # 情况二
    a = float(input("下部受拉筋至底边缘距离 a(mm):")) * 0.001
    a_ = float(input("上保护层厚度a'(mm):")) * 0.001
    h0 = h-a
    print("h0 = %smm"%format_output(h0*1000))
    Alpha_s = (Gd*M-Fy_*As_*(h0-a_))/(Fc*b*h0*h0)
    # print(Alpha_s)
    print("αs = %s"%format_output(Alpha_s))
    if Alpha_s_d >= Alpha_s:
        print("αs <= αsd =%s"%Alpha_s_d)
        print("受压区配筋率满足要求")
        Eps = 1 - math.pow((1-2*Alpha_s),0.5)
        print("ε = %s"%format_output(Eps))
        x = Eps*h0
        print("x = %s mm"%format_output(x*1000))
        if x>= 2*a_:
            print("x >= 2a'=%s"%(2*a_*1000))
            print("受压筋已充分发挥")
            AREAs = (Fc*b*Eps*h0 + Fy_*As_)/(Fy)
            AREAs_ = As_
            # 请注意
            # 传入这个函数的参数不是标准单位，因为要方便调试这个函数
            save(AREAs * 1000 * 1000, AREAs_ * 1000 * 1000, a * 1000, a_ * 1000)

        else:
            print("x < 2a'=%s" % (2 * a_ * 1000))
            print("受压筋未充分发挥")

            AREAs = (Gd*M)/(Fy*(h0-a_))
            AREAs_ = As_
            # 请注意
            # 传入这个函数的参数不是标准单位，因为要方便调试这个函数
            save(AREAs * 1000 * 1000, AREAs_ * 1000 * 1000, a * 1000, a_ * 1000)
    else:
        print("αs > αsd =%s" % Alpha_s_d)
        print("超筋了，需要增加As',转入情况1")
        Condition_ONE(M,Gd,Pmin,b,h,Fc,Fy,Fy_,0,Alpha_s_d,Eps_b)


if __name__ == '__main__':
    print("Author：Muller")
    print("可能有bug，尽管我已经测试了一阵子，但是bug是不可避免的，so：结果只供参考")
    print("pull issues to:1184276183")

    while True:
        # 输入数据之后转化为标准单位，在打印时临时转化单位
        try:
            Moment_Design = float(input("请输入永久荷载弯矩设计值(kN·m)："))
            Moment_Design_ = float(input("请输入可变荷载弯矩设计值(kN·m)："))
        except Exception as e:
            print(e)
            print("输入有误，请重新运行程序")
            break
        structure_class = input("请输入结构安全级别(1,2,3):")
        Concrete_Class = input("混凝土标号(C10-C60)：")
        Rebar_Class = input("钢筋标号(如HRB400)：")
        # 传入材料标号，得到材料的设计强度
        Result = check(Concrete_Class,Rebar_Class,structure_class,Moment_Design,Moment_Design_)
        if Result:
            Fc,Fy,Fy_ = Result[0]
            Alpha_s_d, Eps_b = Result[1]
            M_Dg, Gammad,Pmin = Result[2]

            Breadth = float(input("请输入设计截面宽度(mm):"))
            b = Breadth * 0.001
            Height = float(input("请输入设计截面高度(mm):"))
            h = Height * 0.001
            Area_s_ = float(input("请输入受压区面积As'(mm²),欲求则输入0："))
            As_ = Area_s_ * 0.001 * 0.001
            M = Moment_Design * 1000
            M_ = Moment_Design_ * 1000
            if Area_s_ != 0:
                print("As不等于0，转入情况2")
                Condition_TWO(M_Dg,Gammad,Pmin,b,h,Fc,Fy,Fy_,As_,Alpha_s_d,Eps_b)
            else:
                print("As等于0，转入情况1")
                Condition_ONE(M_Dg,Gammad,Pmin,b,h,Fc,Fy,Fy_,0,Alpha_s_d,Eps_b)
        else:
            print("请重新开始程序")
            go = input('输入回车继续运行,输入 n 回车结束运行: ')
            if go == 'n':
                break
        print(">>>请按Enter")
        go = input('输入回车继续运行,输入 n 回车结束运行: ')
        if go == 'n':
            break

