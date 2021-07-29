# USTC Choose Course

## 简介

中科大教务系统刷课 Python 小脚本。支持直选课和换班。支持本科生和硕士研究生。选课成功或出现意外情况（且重试次数达到阈值）邮件通知自己。

![image](https://user-images.githubusercontent.com/36265606/127443846-7c9a7c70-78bc-470b-a6b0-f191717c0a15.png)

> 注意：为了降低脚本传播可能带来的不利影响，部分代码已被删去（直选课和换班两个功能各对应一个 TODO，每个 TODO 需约 2 行代码），请根据提示内容，合理使用 Python 调试工具，自行补全。

## 运行

1. 修改 `config.py` 的内容，如不需要发邮件，可忽略邮件相关设置；

2. 补全 `main.py` 中缺失的两个 TODO 部分；

3. `pip install requests bs4 lxml`；

5. 直选课：`python main.py [new course code]`；
   换班：`python main.py [new course code] [old course code] [reason]`。
   
   以上两个命令末尾可加入如下可选参数：
   
   1. `-p` 或 `--period`: 刷课周期，单位秒。接受一个数字，默认为 5，请勿将其设置过短，以免增大教务网站压力；
   2. `-s` 或 `--stable_mode`: 是否启用稳定模式。接受一个字符串（`1/y/yes/True/true` or `0/n/no/False/false` ），默认是 `False`。稳定模式中每次选课都重新登录，可用于长时间抢课（如夜间刷漏），短时间抢课不需加入此参数（因为此模式会降低性能）；
   3. `-i` 或 `--identity`: 学生身份。接受一个字符串（`undergraduate` or `postgraduate`，分别表示本科生和硕士研究生），默认 `undergraduate`。

   详见`python main.py -h`。



**示例**

```bash
python main.py PE00120.02 # 本科生选课堂号是 PE00120.02 的课
python main.py PE00120.02 PE00120.01 # 本科生换 PE00120.01 课为 PE00120.02 课
python main.py PE00120.02 -i postgraduate # 研究生选课堂号是 PE00120.02 的课
python main.py PE00120.02 -p 60 -s True # 本科生选课堂号是 PE00120.02 的课，使用稳定模式一分钟尝试一次
```



## TODO
- [x] 添加对研究生选课的支持（~~我不是研究生，因此无法分析研究生的选课流程，所以暂时无法完成这个功能。如果你是研究生且想要使用此脚本，可以和我联系~~  update: 已完成）。

