
import math

# data = [(M,Gd,As'),(b,h),(fc,fy,fy_),(a,a'),(Eps_b,P_min,Alpha_1,Alpha_sd)]


class Calculate(object):

    def __init__(self,data):
        self.data = data
        self.M = data[0][0]
        self.Gd = data[0][1]
        self.b = data[1][0]
        self.h = data[1][1]

        self.Fc = data[2][0]
        self.Fy = data[2][1]
        self.Fy_ = data[2][2]
        self.a = data[3][0]
        self.a_ = data[3][1]
        self.Alpha_sd = data[4][3]
        self.Pmin = data[4][1]
        self.h0 = self.h - self.a

    def Alphas(self,key):
        M = self.M
        Fc = self.Fc
        Fy_ = self.Fy_
        b = self.b
        h0 = self.h0
        Gd = self.Gd

        if key == 1:
            Alpha_s = (Gd * M) / (Fc * b * h0 * h0)
            return Alpha_s

        if key == 2:
            As_ = self.data[0][2]
            a_ = self.data[3][1]
            Alpha_s = (Gd*M-Fy_*As_*(h0-a_))/(Fc*b*h0*h0)
            return Alpha_s

    def Areas(self,key):
        M = self.M
        Fc = self.Fc
        Fy_ = self.Fy_
        b = self.b
        h0 = self.h - self.a
        Gd = self.Gd
        Fy = self.Fy
        As_ = self.data[0][2]
        a_ = self.a_
        Eps_b, P_min, a1, Alpha_sd = self.data[4]

        if key == 1:
            As = (Fc * b * a1 * Eps_b * h0 + Fy_ * As_) / (Fy)
            return As
        if key == 2:
            Eps = 1 - math.pow((1 - 2 * self.Alphas(1)), 0.5)
            As = (Fc * b * Eps * h0) / Fy
            return As
        if key == 3:
            AREAs = (Gd * M) / (Fy * (h0 - a_))
            return AREAs
        if key == 4:
            Eps = 1 - math.pow((1 - 2 * self.Alphas(2)), 0.5)
            AREAs = (Fc * b * Eps * h0 + Fy_ * As_) / (Fy)
            return AREAs
        if key == 5:
            AREAs = P_min * b * h0
            return AREAs
        if key == 0:
            As_ = (Gd * M - (Alpha_sd * Fc * b * h0 * h0)) / (Fy_ * (h0 - a_))
            return As_
