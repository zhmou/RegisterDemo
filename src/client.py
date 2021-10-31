"""
    客户端
        register_check():检查注册情况:1.判断.\reg.zh文件是否存在 2.判断HKEY_CURRENT_USER/Software/RegisInfo的子项TIME是否存在
                         3.比对两文件中保存的时间信息是否存在且对应
        register(activate_code):通过Server端生成的激活码进行激活
        client_init():客户端启动,先调用register_check()检查注册情况,然后读取时间 再进入While STATE死循环,每隔一分钟执行write_time()向注册表和文件中写入时间信息
                      以及time_left()以DD:HH:MM的方式显示时间
"""
import os
import subprocess
import winreg
import base64
import time
import baseconvert
from keygen import verify_signature

# CURRENT_MACHINE_ID 获取机器的UUID, Windows平台下使用
CURRENT_MACHINE_ID = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip().replace('-', '')
PUBLIC_KEY = (270916549932685597202772283447247505705092774070722510140833201833867826517, 65537)

STATE = False
dd, hh, mm = 0, 0, 0


def register_check():
    if os.path.exists(r"../log/reg.zh"):
        with open(r'../log/reg.zh', 'r') as f:
            base64_time = f.read()
        decode_time = base64.b64decode(base64_time).decode("utf-8")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\RegisInfo')
            value, _ = winreg.QueryValueEx(key, "TIME")
        except OSError:
            return "found no register info in regedit, need register"
        if decode_time == value:
            global STATE
            STATE = True
            return "register_check success"
        else:
            return "register info are not compatible, need register"
    else:
        return "register file doesn't exist, need register"


def register(activate_code_base62):
    if register_check() == "register_check success":
        return "you have been registered, do not register again"
    activate_code = int(baseconvert.f(activate_code_base62, 62, 10))
    info = verify_signature(activate_code, PUBLIC_KEY)
    machine_id_base10 = int(CURRENT_MACHINE_ID, base=16)
    check_machine_id = int(str(info)[:-4])
    check_time = str(info)[-4:]
    if machine_id_base10 == check_machine_id:
        # 将check_time(天)时间转为秒写入注册表和reg.zh文件中
        winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, r'SOFTWARE\RegisInfo', reserved=0, access=winreg.KEY_WRITE)
        second = int(check_time) * 86400
        write_time(second)
        return "register OK"
    else:
        return "machine id is wrong, please reinsert the activate code"


def client_init():
    global STATE
    if register_check() == "register_check success":
        with open(r'../log/reg.zh', 'r') as f:
            base64_time = f.read()
            seconds = int(base64.b64decode(base64_time).decode("utf-8"))
        while STATE:
            global dd, hh, mm
            dd, hh, mm, = time_left(seconds)
            time.sleep(60)
            seconds = seconds - 60
            if seconds > 0:
                write_time(seconds)
            else:
                STATE = False
                return "time is over"
        STATE = False
        return "client_close is called"
    else:
        return register_check()


def write_time(seconds):
    if not os.path.isdir(r'../log'):
        os.mkdir(r'../log')
    base64_time = base64.b64encode(str(seconds).encode()).decode("utf-8")
    with open(r'../log/reg.zh', 'w') as f:
        f.write(base64_time)

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\RegisInfo', 0, access=winreg.KEY_WRITE)
    winreg.SetValueEx(key, 'TIME', 0, winreg.REG_SZ, str(seconds))


def time_left(seconds):
    global dd, hh, mm
    dd = seconds // 86400
    hh = (seconds % 86400) // 3600
    mm = (seconds - dd * 86400 - hh * 3600) // 60

    return dd, hh, mm


def client_close():
    global STATE
    STATE = False


if __name__ == "__main__":
    print(register("5w8fZl7lBa0TdiBB4aHIrpoeMJfeF2pZZHl7T0N95k"))
