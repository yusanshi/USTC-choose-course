# USTC Choose Course

> 已弃用。



中科大（新）教务系统刷课 Python 小脚本。

> 注意：为了防止脚本的大规模传播，部分代码（两个 TODO 部分共约 7 行代码）已被删去，请通读本脚本并使用浏览器开发者工具弄清楚选课流程后自行补全。
>
> 本脚本是本人学习爬虫等技术的练习作品，仍有不足，开源此脚本的目的也是为了学习交流，欢迎提意见。请勿将选课周期设置过短，以免增大教务网站压力。

## 简介

刷课小脚本，支持直选课和换班。选课成功后会有邮件通知，若出现意外情况也会有邮件通知（可自定义意外后重试的次数）。

主函数定义为`def choose_course(new_course_code, PERIOD, old_course_code=None, reason=None, stable_mode=False)`，直选课时，只传入新课课堂号和刷课周期（单位秒）；换班时，需再填入旧课课堂号和换班理由。若加入`stable_mode=True`参数表示采用每次循环都重新登录的稳定模式，可用于长时间抢课（如夜间刷漏），短时间抢课不需加入此参数（因为此模式会降低性能）。

具体用法示例：

```python

# 用以下行替换 choose_course.py 尾部的 choose_course() 行的内容即可。


# 从 011163.01 换班到 011163.02，刷课周期 5 秒，申请理由是我的姓名，稳定模式
choose_course('011163.02', 5, '011163.01', '余磊', stable_mode=True)

# 直选课 011163.02，刷课周期 5 秒，稳定模式
choose_course('011163.02', 5, stable_mode=True)

# 换班，非稳定模式
choose_course('011163.02', 2, '011163.01', '余磊')

# 直选，非稳定模式
choose_course('011163.02', 2)
```

## 运行

1. 修改`config.py`的内容，如不需要发邮件，可忽略邮件相关设置；
2. 补全`choose_course.py`中缺失的两个 TODO 部分；
3. 修改`choose_course.py`尾部的`choose_course()`行的内容（参见上文的用法示例）；
4. 自行使用 pip 工具安装缺失的包；
5. `python choose_course.py`。

## 截图

> 此处应为截“代码”😁

```
PS C:\Users\Yu\Documents\GitHub\USTC_choose_course> cd 'c:\Users\Yu\Documents\GitHub\USTC_choose_course'; ${env:PYTHONIOENCODING}='UTF-8'; ${env:PYTHONUNBUFFERED}='1'; & 
'C:\Users\Yu\AppData\Local\Programs\Python\Python37\python.exe' 'c:\Users\Yu\.vscode\extensions\ms-python.python-2019.8.29288\pythonFiles\ptvsd_launcher.py' '--default' '--nodebug' '--client' '--host' 'localhost' '--port' '3734' 'c:\Users\Yu\Documents\GitHub\USTC_choose_course\choose_course.py' 
正在第 1 次尝试...
重新登录中...
选课失败，失败原因： 同课程代码只能选一门
正在第 2 次尝试...
重新登录中...
选课失败，失败原因： 同课程代码只能选一门
正在第 3 次尝试...
重新登录中...
选课失败，失败原因： 同课程代码只能选一门
正在第 4 次尝试...
重新登录中...
选课失败，失败原因： 同课程代码只能选一门
正在第 5 次尝试...
重新登录中...
选课失败，失败原因： 同课程代码只能选一门
PS C:\Users\Yu\Documents\GitHub\USTC_choose_course> cd 'c:\Users\Yu\Documents\GitHub\USTC_choose_course'; ${env:PYTHONIOENCODING}='UTF-8'; ${env:PYTHONUNBUFFERED}='1'; & 
'C:\Users\Yu\AppData\Local\Programs\Python\Python37\python.exe' 'c:\Users\Yu\.vscode\extensions\ms-python.python-2019.8.29288\pythonFiles\ptvsd_launcher.py' '--default' '--nodebug' '--client' '--host' 'localhost' '--port' '3794' 'c:\Users\Yu\Documents\GitHub\USTC_choose_course\choose_course.py' 
正在第 1 次尝试...
选课失败，失败原因： 同课程代码只能选一门
正在第 2 次尝试...
选课失败，失败原因： 同课程代码只能选一门
正在第 3 次尝试...
正在第 4 次尝试...
选课失败，失败原因： 同课程代码只能选一门
正在第 5 次尝试...
选课失败，失败原因： 同课程代码只能选一门
PS C:\Users\Yu\Documents\GitHub\USTC_choose_course> cd 'c:\Users\Yu\Documents\GitHub\USTC_choose_course'; ${env:PYTHONIOENCODING}='UTF-8'; ${env:PYTHONUNBUFFERED}='1'; & 
'C:\Users\Yu\AppData\Local\Programs\Python\Python37\python.exe' 'c:\Users\Yu\.vscode\extensions\ms-python.python-2019.8.29288\pythonFiles\ptvsd_launcher.py' '--default' '--nodebug' '--client' '--host' 'localhost' '--port' '3843' 'c:\Users\Yu\Documents\GitHub\USTC_choose_course\choose_course.py'
正在第 1 次尝试...
重新登录中...
选课成功，程序退出！
```

![1566818336035](README.assets/1566818336035.png)