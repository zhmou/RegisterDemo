"""
    客户端
        create_activate_code(CURRENT_MACHINE_ID, time):
        根据用户发送的机器ID(CURRENT_MACHINE_ID, 字符型)与指定的激活时长(天数, 整型)生成对应的激活码
"""
from keygen import signature
import baseconvert
# 通过keygen.py生成的私钥,不能公开
PRIVATE_KEY = (270916549932685597202772283447247505705092774070722510140833201833867826517, 122823329288797999055324016750608326406193548375374156516392553496600091329)


def create_activate_code(CURRENT_MACHINE_ID, time):
    # signature只能对数字进行加密签名, CURRENT_MACHINE_ID是16进制的字符串, 需要转化为10进制的数字进行操作。
    id_num = int(CURRENT_MACHINE_ID, base=16)
    # 机器信息 + 激活天数 的字符串拼接组成待签名信息(info),再转为整型
    # 激活天数格式化补0至宽度为4位 如 30天 -> 0030
    # TODO: time天数预期设定不超过9999, 但程序中未作数字范围检查, 格式化补0可能产生问题
    info = int(str(id_num) + str(time).zfill(4))
    # 对信息进行签名生成激活码(10进制)
    activate_code = signature(info, PRIVATE_KEY)
    # 调用进制转换, 10进制转62进制用以压缩字符串
    activate_code_base62 = baseconvert.f(activate_code, 10, 62)
    return activate_code_base62


# 测试
if __name__ == "__main__":
    CURRENT_MACHINE_ID = "运行test.py, 点击Generate UUID按钮以获取你自己的CURRENT_MACHINE_ID"
    CURRENT_MACHINE_ID = "EB629300E3E047CC92358C8CAAA8BAC7"
    time = 1
    code = create_activate_code(CURRENT_MACHINE_ID, time)
    print(code)
