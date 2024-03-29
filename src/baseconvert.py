"""
    进制转换
        f(nx, x1, x):实现62以内任意进制间的转换 nx:待转换字符串, x1:自身进制, x:待转换进制
"""


def f(nx, x1, x):
    a = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
         'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
         'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
         'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    nx = str(nx)
    b1 = list(nx)
    # 逐个检查b1列表每一位是否符合进制上的限制(如二进制只能由01构成),并将其转换为对应字符的数字
    # 譬如nx = '2a4b', b1 = ['2', 'a', '4', 'b'], b2 = [2, 10, 4, 11]
    b2 = []
    for i in b1:
        for i1 in range(0, 62):
            if a[i1] == i:
                b2 = b2 + [i1]
                if i1 > x1:
                    print(i, "错误定义")
    b2.reverse()
    # b2逆序为[11, 4, 10, 2]
    # n1是初值
    n1 = 0
    # 该位的位置
    n2 = 1
    # 从最低位开始, 该位的值转为十进制 该位数数值 * 进制 ^ 位置
    # 譬如 2a4b(base16) = b(11) * 16 ^ 0 + 4 * 16 ^ 1 + a(10) * 16 ^ 2 + 2 * 16 ^ 3
    for i in b2:
        n1 = n1 + int(i) * (pow(x1, n2 - 1))
        n2 = n2 + 1
    # 转换为10进制的数字
    n = n1
    b = []
    # 短除法进行进制转换
    while True:
        # s 商数
        s = n // x
        # y 余数
        y = n % x
        b = b + [y]
        if s == 0:
            break
        n = s
    # 余数逆序排列
    b.reverse()
    bd = ""
    # 再将余数各位的数转换成a[]里的字符
    for i in b:
        # print(a[i],end='')
        bd = bd + a[i]
    # 返回字符串
    return bd


# 测试
if __name__ == "__main__":
    print(f("2a4b", 16, 2))
