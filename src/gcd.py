"""
    拓展欧几里得算法
        gcd(a, b):求a,b两数的最大公约数
        extend_gcd(a, b):用于求解gcd(a, b) = ax + by的整数解x、y
"""


# 辗转相除法(欧几里得法)求最大公约数(greatest common divisor)
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


'''
拓展欧几里得算法,用于求解gcd(a, b) = ax + by的整数解x、y
原理:设a>b
    当b=0时,gcd(a,0)=a,对于a=ax+0y,容易得到其正整数解x=1,y=0
    当b!=0时,设:
        ax1 + by1 = gcd(a,b)
        bx2 + (a%b)*y2 = gcd(b,a%b)
    根据辗转相除法的原理有 gcd(a,b) = gcd(b,a%b);两式联立得:
        ax1 + by1 = bx2 + (a%b)*y2
    而a%b可写作 a - (a//b) * b (其中"//"为整除),则有:
        ax1 + by1 = bx2 + ay2 - (a//b)*by2
    比对系数可得:
        x1 = y2
        y1 = x2 - (a//b)*y2
    由此可知，方程gcd(a, b) = ax1 + by1的解可用gcd(b, a%b) = bx2 + (a%b)y2表示，
    构成了类似欧几里得算法的递归，下述函数即通过递归的方式实现了拓展欧几里得算法
'''


def extend_gcd(a, b):
    if b == 0:
        x1 = 1
        y1 = 0
        x = x1
        y = y1
        return x, y
    else:
        x1, y1 = extend_gcd(b, a % b)
        x = y1
        y = x1 - a // b * y1
        return x, y
