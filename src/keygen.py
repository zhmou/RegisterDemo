"""
    RSA算法
        gen_key(p,q):给定两个大质数p,q,生成对应的公钥(public_key)/私钥对(private_key)
        signature(message, private_key):给指定信息message(数字)通过私钥生成对应的签名code
        verify_signature(code, public_key):通过签名code还原原信息message

        **注意** 在实际开发环境中, 请在生成公钥/私钥对后销毁p和q
"""

from gcd import extend_gcd
from exp_mode import exp_mode


# RSA生成公钥、私钥,步骤参见:https://www.ruanyifeng.com/blog/2013/07/rsa_algorithm_part_two.html
def gen_key(p, q):
    # n的长度即为密钥长度, RSA的安全性基于大数因数分解，目前通常使n=2048bit, 即p,q需要为1024位质数
    n = p * q

    # 计算n的欧拉函数φ(n)
    phi_n = (p - 1) * (q - 1)

    # 取e∈(1,φ(n)),且e与φ(n)互质,通常取65537
    e = 65537

    # 计算e对于φ(n)的模反元素d, 即求解不定方程ed - 1 = kφ(n)
    # 变形,有ex + φ(n)y = 1,考虑到e与φ(n)互质, gcd(e,φ(n))=1,恰好可用拓展欧几里得算法求解:
    x, y = extend_gcd(e, phi_n)

    # 根据该组解,求出一个正数d才是我们需要的解(因为签名/解密所需的d要是正数),
    # e(x + φ(n)) + φ(n)(y - e) = 1, (数学水平有限,不太清楚d=x+φ(n)为啥一定是个正数)
    if x < 0:
        x = x + phi_n
    d = x

    public_key = (n, e)
    private_key = (n, d)
    # 返回:   公钥          私钥
    return public_key, private_key


# 签名: 签名信息 = 待加密信息 ^ d % n
def signature(message, private_key):
    n = private_key[0]
    d = private_key[1]

    code = exp_mode(message, d, n)
    return code


# 验证: 原信息 = 签名信息 ^ e % n
def verify_signature(code, public_key):
    n = public_key[0]
    e = public_key[1]

    message = exp_mode(code, e, n)
    return message


if __name__ == "__main__":
    # 请自行找出两个大质数(1024位)p、q
    p = 3
    q = 5
    print(len(str(p)))
    pubkey, selfkey = gen_key(p, q)
    # 将pubkey的值粘贴于client.py的全局变量PUBLIC_KEY下
    print(pubkey)
    # 将selfkey的值粘贴于server.py的全局变量PRIVATE_KEY下
    print(selfkey)
