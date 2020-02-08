# avail_wifi_changer
基于Ping命令实现无线接入点的质量监测及自动切换


****************************************************************
2020.02.08 更新

主要用于解决：

同时支持2.4G和5G的路由器不能根据网络质量智能切换频段的缺陷

也可用于在不同的路由器间选择一个较优的接入点

以第一点为主，不同路由器切换的开销比较大

不建议游戏时使用！否则切换时肯定丢包
*****************************************************************
使用方法：

首先打开all_constants.json配置预定义的常量

```
"MAX_RETRY_TIME":5,			# 最大重连次数
"INTERFACE_NUMBER":0, 			# 默认网卡序号
"MAX_DIFFERENCE_DELAY":15, 		# 允许当前网络与次优网络的最大延迟差值(避免频繁切换带来的开销)
"ALLOWED_MAX_DELAY":40,			# 允许的最大延迟
"ALLOWED_MAX_PACKET_LOSS_RATE":25,	# 允许的最大丢包率
"SLEEP_TIME":10,			# 不需切换时程序休眠的时间
"IP_OR_URL":"baidu.com"			# 默认PING的IP或URL
```

然后双击the_main.exe启动

根据提示操作即可
*****************************************************************
Coded By 无名Joker

代码开源，所有密码不作信息收集

稍后上传至个人主页

GayHub：https://github.com/wuming7847/

CSDN：https://blog.csdn.net/weixin_43249758

如有Bug或性能/算法建议请反馈至 Q: 2302867179
*****************************************************************
[exe下载请戳](https://pan.baidu.com/s/1SdfCtQ0xOOODZaDnPdYWvg) 提取码nhry
*****************************************************************
代码结构

```python
connect_to_wifi.py

直接调用pywifi库

wireless_card_scan 用于扫描本机网卡
wifi_scan 扫描附近的可接入点
add_avail_wifi 用于添加可用wifi的SSID和密码，可以保存到本地json文件中
connect_to 用于连接到指定wifi

```

```python
quality_assessment.py

基于Ping命令检测当前网络的平均延迟和丢包率

get_quality 用于ping指定网址或IP并返回ping的结果
data_wash 用正则对ping的结果作数据清洗，提取出int型的平均延迟和丢包率

此处有处理的不太好的地方
因为直接ping只能发四个包
如果用-c参数需要提供管理员权限
权衡了一下还是选了直接ping
不是写不了
而是要管理权限实在太可疑了

```

```python
speed_assessment.py

检测当前的网速
get_speed_per_deci 计算0.1秒内的网速
calculate_average_speed(seconds) 返回seconds秒内的平均网速

其实网速这个属性意义不是很大，受影响的因素太多了
所以只起一个参考作用
```

```python
wifi_changer.py

对底层三个模块提供的大多数方法进行了封装

change_and_test_wifi 切换wifi后更新其网速和平均延迟、丢包率
only_test_wifi 不需切换时持续更新当前网络的网速、平均延迟、丢包率
max_retry_connect 对指定接入点进行连接，最多重试x次，失败则结束
```

```python
init_constants.py

初始化各种常量

reload_json 如果运行时发现常量设置有误可以打开文件重新修改，输入reload可重新读取
init_constants 封装了reload_json方法，最终返回dict型的所有常量键值对
```

```python
the_main.py

主方法

首先读入配置的常量
然后扫描本机网卡
扫描附近接入点
建立可用wifi组
输入wifi密码
遍历所有wifi
多关键字排序选择当前的最优wifi
while True:
	持续更新其网速、延迟、丢包率等属性
	如果发现需要切换
		则切换到次优的wifi
		更新其网速、延迟、丢包率等属性
		对所有的可用wifi重新排序
	如果无需切换
		则程序休眠一段时间
```

