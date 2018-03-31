

def save(As,As_,a,a_):
    # a *= 0.001
    # a_ *= 0.001
    AREAs = As*1000*1000
    AREAs_ = As_*1000*1000
    print("配筋完成：")
    print("理论配筋面积As=%smm²,As'=%smm²" % (AREAs, AREAs_))
    d, n, n_, Ar = Rebar(AREAs, AREAs_)

    AREAs = (3.14 / 4) * d * d * n
    AREAs_ = (3.14 / 4) * d * d * n_

    if AREAs_ == 0:

        print("┌-------┐保护层厚度a'=%s" % a_)
        print("|◎     ◎| 构造筋%smm x2根" % d)
        print("|       |")
        print("|       |")
        print("|       |")
        print("|       |")
        print("|       | 受拉区配筋面积=%smm²" % AREAs)
        print("|◎  ◎  ◎| %smmx%s根" % (d, n))
        print("└-------┘保护层厚度a=%s" % a)

    else:

        print("┌-------┐保护层厚度a'=%s" % a_)
        print("|◎     ◎| ◎%smm x%s根" % (d, n_))
        print("|       | 受压区配筋面积=%smm²" % AREAs_)
        print("|       |")
        print("|       |")
        print("|       |")
        print("|       | 受拉区配筋面积=%smm²" % AREAs)
        print("|◎  ◎  ◎| %smmx%s根" % (d, n))
        print("└-------┘保护层厚度a=%s" % a)


def Rebar(As ,As_):

    # print("As=%smm²" % As)
    # print("As'=%smm²" % As_)
    # 传入受拉和受压钢筋的面积(mm²)，返回一个经过计算后得出的最优配筋方式
    # 可选的直径
    d_list = [8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36, 40, 50]
    # 可选钢筋根数:2-9根
    amount = [i for i in range(2,10)]
    # 可超过的面积参数，限制在200mm²内
    limited = 200
    # 下面是这个算法，比较臃肿
    avi = []
    n_list = []
    n_list_ = []
    # 单筋截面的情况
    if As_ == 0:
        for d in d_list:
            for n in amount:
                A = n * (3.14 / 4) * d * d
                print(A)
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
    return sorted(avi,key=lambda area:area[-1])[0]


def check(C_class,R_class):
    # 根据材料的标号确定混凝土抗压强度设计值和钢筋屈服强度设计值
    Concrete_Design = {"C10":4.8,"C15":7.2,"C20":9.6,"C25":11.9,"C30":14.3,"C35":16.7,"C40":19.1,"C45":21.1,"C50":23.1,"C55":25.3,"C60":27.5}
    Rebar_Design = {"HPB300":[270,270,0.41,0.576],"HRB335":[300,300,0.399,0.550],"HRB400":[360,360,0.384,0.518],"HRB500":[420,420,0.384,0.518]}
    Force_C = Concrete_Design[C_class]*1000*1000
    Force_y = Rebar_Design[R_class][0]*1000*1000
    Force_y_ = Rebar_Design[R_class][1]*1000*1000
    Alpha_a_d = Rebar_Design[R_class][2]
    Eps_b = Rebar_Design[R_class][3]
    return Force_C,Force_y,Force_y_,Alpha_a_d,Eps_b


if __name__ == '__main__':
    save(1362, 509, 45, 45)
    print(Rebar(1362, 509))
