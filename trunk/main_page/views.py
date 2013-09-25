# coding=UTF-8
# /usr/python

from django.http import HttpResponse

home_page = u'''
<h1>关怀冷暖</h1>
<p>现在关注微信公众平台——关怀冷暖，及时获取本地信息，后续继续增加心动功能！</p>
<img src="static/weixinpub/qrcode_for_gh_a207d2fdeaec_430.jpg" alt="关怀冷暖" />
<p/>
<a href="weixinpub/about">about</a>
'''

def index(request):
    return HttpResponse(home_page)
