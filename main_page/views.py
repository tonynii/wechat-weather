# coding=UTF-8
# /usr/python

from django.http import HttpResponse

home_page = u'''
<h1>关怀冷暖</h1>
<p>现在关注微信公众平台——关怀冷暖，及时获取本地信息，后续继续增加心动功能！</p>
<p> </p>
<p>Ver: 2.1.2</p>
<p>Data: 20130914<p>
<p></p>
<h2>History</h2>
<h3>V2.1.2(20130914)</h3>
<p>1、消息构造使用模板文件</p>
<h3>V2.1.1(20130910)</h3>
<p>1、将API和token合并到配置文件中</p>
<p>2、更新top1.jpg文件名为top2.jpg</p>
<h3>V2.1</h3>
<p>1、天气回复消息一个段图文消息改为一张背景图片，天气信息放在后面的段落</p>
<p>2、view负责装配消息结构，modle负责生成消息</p>
'''

def index(request):
    return HttpResponse(home_page)
