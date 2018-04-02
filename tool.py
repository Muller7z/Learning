

def format_output(float_num):
    string = str(float(float_num))
    dot = string.index(".")
    return string[:dot+4]  # 保留至小数点后三位


def save(As,As_,a,a_):

    print("配筋完成↓")
    print("理论配筋面积As=%smm²,As'=%smm²" % (format_output(As),format_output(As_)))
    print("配筋设置情况：")
    try:
        d, n, n_, Ar = Rebar(As, As_)

        AREAs = format_output((3.14 / 4) * d * d * n)
        AREAs_ =format_output((3.14 / 4) * d * d * n_)

        if As_ == 0:

            print("╔════════╗上层距离a'=%smm" % a_)
            print("║·    ·║ ·构造筋 x2根 ")
            print("║        ║")
            print("║        ║")
            print("║        ║")
            print("║        ║")
            print("║        ║ 受拉区实际配筋面积=%smm²" % AREAs)
            print("║· · ·║ ·%smm x %s根" % (d, n))
            print("╚════════╝下层钢筋至边缘距离a=%smm" % a)

        else:

            print("╔════════╗上层距离a'=%smm" % a_)
            print("║· · ·║ ·%smm x %s根" % (d, n_))
            print("║        ║ 受压区实际配筋面积=%smm²" % AREAs_)
            print("║        ║")
            print("║        ║")
            print("║        ║")
            print("║        ║ 受拉区实际配筋面积=%smm²" % AREAs)
            print("║· · ·║ ·%smm x %s根" % (d, n))
            print("╚════════╝下层钢筋至边缘距离a=%smm" % a)
            print("若a取为单排筋，且根数过多，请将a加倍后重新计算(偷懒没有做自动调整)")
    except IndexError as e:
        print(e)
        print("预设配筋表中没有找到可选的配筋方法，请自行拟定")


def Rebar(As ,As_):

    # 传入受拉和受压钢筋的面积(mm²)，返回一个经过计算后得出的最优配筋方式
    # 可选的直径
    d_list = [8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36, 40, 50]
    # 可选钢筋根数:2-20根
    amount = [i for i in range(2,21)]
    # 可超过的面积参数，限制在500mm²内,最后有排序算法，不用担心这个值过大，取得过小反而 找不到配筋情况
    limited = 500
    # 下面是这个函数的算法
    avi = []
    n_list = []
    n_list_ = []
    # 单筋截面的情况
    if As_ == 0:
        for d in d_list:
            for n in amount:
                A = n * (3.14 / 4) * d * d
                # print(A)
                if (A - As) >= 0 and (A - As) <= limited:
                    # 将这个可选结果添加到列表中
                    avi.append((d, n, 2,(3.14/4)*d*d*(n+2)))
    # 双筋截面
    else:
        for d in d_list:
            for n in amount:
                A = n * (3.14 / 4) * d * d
                if (A - As) >= 0 and (A - As) <= limited:
                    n_list.append((d,n))
            for n_ in amount:
                A = n_ * (3.14 / 4) * d * d
                if (A - As_) >= 0 and (A - As_) <= limited:
                    n_list_.append((d,n_))
        for i in n_list:
            for x in n_list_:
                if i[0] == x[0]:
                    d,n,n_ = (i[0], i[1], x[1])
                    A = (3.14/4)*d*d*(n+n_)
                    avi.append((d,n,n_,A))
    # 将得到的可用列表按超出的面积由小到大进行排序，并返回最小的一个
    # 数据类型：元组  参数：(直径、受拉钢筋根数，受压钢筋根数，实际配筋面积)
    # 单筋截面也将有受压钢筋2根，作为构造筋
    # print(avi)
    return sorted(avi,key=lambda area:area[-1])[0]


def check(C_class,R_class,s_class,M,M_):

    # 根据材料的标号确定混凝土抗压强度设计值和钢筋屈服强度设计值
    Concrete_Design = {"C10":4.8,"C15":7.2,"C20":9.6,"C25":11.9,"C30":14.3,"C35":16.7,"C40":19.1,"C45":21.1,"C50":23.1,"C55":25.3,"C60":27.5}
    Rebar_Design = {"HPB300":[270.0,270.0,0.41,0.576],"HRB335":[300.0,300.0,0.399,0.550],"HRB400":[360.0,360.0,0.384,0.518],"HRB500":[420.0,420.0,0.384,0.518]}
    Pmin = {"HPB300":0.25,"HRB335":0.2,"HRB400":0.2,"HRB500":0.2}
    try:
        Force_C = Concrete_Design[C_class]
        print("fc=%sN/mm²"%Force_C)
        Force_y = Rebar_Design[R_class][0]
        print("fy=%sN/mm²"%Force_y)
        Force_y_ = Rebar_Design[R_class][1]
        print("fy'=%sN/mm²"%Force_y_)
        Alpha_a_d = Rebar_Design[R_class][2]
        print("αsd=%s"%Alpha_a_d)
        Eps_b = Rebar_Design[R_class][3]
        print("εb=%s"%Eps_b)
        Pmin_ = Pmin[R_class]
        print("ρmin=%s"%Pmin_)
        # 计算结构的弯矩设计值
        structure_class = {"1":1.1,"2":1.0,"3":0.9}
        # 结构重要性系数
        Gamma0 = structure_class[s_class]
        print("结构重要性系数γ0=%s"%Gamma0)
        # 设计状况系数
        Psi = 1.0
        print("设计状况系数ψ=%s"%Psi)
        # 结构系数
        Gammad = 1.20
        print("结构系数γd=%s"%Gammad)
        # 弯矩设计值
        M_Dg = Gamma0*Psi*(M + M_)
        print("弯矩设计值：M=%s kN·m"%format_output(M_Dg))
        # 返回一个列表，包含三个元组
        return [(Force_C*1000*1000,Force_y*1000*1000,Force_y_*1000*1000),(Alpha_a_d,Eps_b),(M_Dg*1000,Gammad,Pmin_)]

    except KeyError as k:
        print("找不到输入的标号，请检查是否输入正确 or 提交更新")
        print(k)
        return None


if __name__ == '__main__':
    check("C70","HRB400","3",300000,300000)

