# RegisterDemo
一个实现了机器码生成与激活码激活（模拟软件注册）功能的demo

## 目录结构
![image](https://user-images.githubusercontent.com/43105172/139270375-fa860e8b-eff8-42ef-a0c6-866cdebd329a.png)

    
## 快速上手
### 添加依赖
    pip install pyqt5
### 在keygen.py中生成公钥及私钥
    选取两个质数作为p与q
    运行keygen.py
    销毁p、q
### 将生成的公钥/私钥信息粘贴于client.py/server.py中
### 运行test.py
    点击Generate UUID按钮生成你的机器码
### 激活
    将机器码信息填入server.py的主函数中，修改你想激活的天数，运行
    复制所得到的激活码
    填入Activate右边的文本框中，点击激活按钮
### 效果
    点击start按钮查看效果，显示剩余激活时间
    
    
## 已知bug
    start按钮绑定的执行显示时间的线程忘了写判断条件，导致未注册激活的情况下直接读取了client下的默认时间变量dd, hh, mm = 0, 0, 0
