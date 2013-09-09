# coding=UTF-8
# /usr/python

from django.http import HttpResponse

home_page = u'''
<h1>关怀冷暖</h1>
<p>现在关注微信公众平台——关怀冷暖，及时获取本地信息，后续继续增加心动功能！</p>
<p> </p>
<p>Ver: 2.1</p>
<p>Data: 20180908<p>
<p></p>
<h2>History</h2>
<h3>V2.1</h3>
<p>1、天气回复消息一个段图文消息改为一张背景图片，天气信息放在后面的段落</p>
<p>2、view负责装配消息结构，modle负责生成消息</p>
'''

def index(request):
    return HttpResponse(home_page)
