#!/usr/bin/env python
# coding=utf-8
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response

import time

from weixinpub.models import WeixinMsg
import public.applogging as logging

#消息模板文件名
MSG_TEMP_FILE = u'wechatrespmsg.xml'
ABOUT_TEMP_FILE = u'about.html'



def about(request):
    return render_to_response(ABOUT_TEMP_FILE)

def weixinpub(request):
    try:
        signature = request.GET['signature']
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
    except:
        signature = ''
        timestamp = ''
        nonce = ''
        logging.error(u'get para error')
    host = request.get_host()
    if request.method == 'GET':
        logging.debug(u'recvice GET: {0}'.format(str(request.GET.items())))
        try:
            echostr = request.GET['echostr']
        except:
            echostr = ''
            logging.error(u'get echo para error')
        rcevmsg = WeixinMsg(timestamp, signature, nonce)
        if rcevmsg.verifysignature():
            echostr = echostr
        else:
            logging.error(u'Verify signature error!!!')
            echostr = 'Verify signature error!!!'
        return HttpResponse(echostr)
    elif request.method == 'POST':
        #接收微信的请求内容
        logging.debug(u'recvice POST: {0}'.format(str(request.GET.items())))
        data = unicode(request.body,"utf8",errors='ignore')
        logging.debug(u'POST data is: {0}'.format(data.replace('\n',' ')))
        rcevmsg = WeixinMsg(timestamp, signature, nonce, host)
        if rcevmsg.verifysignature():
            restype, resdata = rcevmsg.msghandle(data)
            t = get_template(MSG_TEMP_FILE)
            if restype == 'text':
                echomsg = WeChatRespTextMsg(rcevmsg.get_from_user(),rcevmsg.get_to_user(),resdata)
                echostr = t.render(Context({'wechatmsg':echomsg}))
            elif restype == 'music':
                pass
            elif restype == 'news':
                echomsg = WeChatRespNewsMsg(rcevmsg.get_from_user(),rcevmsg.get_to_user())
                for i in resdata:
                    echomsg.append_news(title = unicode(i[0]),
                                  desc = unicode(i[1]),
                                  picurl = unicode(i[2]),
                                  url = unicode(i[3]))
                echostr = t.render(Context({'wechatmsg':echomsg}))
            else:
                logging.warning('MsgType error!({0})'.format(restype))
                echostr = u'MsgType error!({0})'.format(restype)
            logging.debug(u'Reponse data is: {0}'.format(echostr.replace('\n','')))
        else:
            logging.error(u'Verify signature error!!!')
            echostr = u'Verify signature error!!!'
    else:
        logging.error(u'request method error!!!')
        echostr = u'request method error!!!'
    return HttpResponse(echostr)



class WeChatRespMsg(object):
    def __init__(self, to_user, from_user):
        self.msg_type = 'other'
        self.to_user = to_user
        self.from_user = from_user
        self.timestamp = '01234'
    
    @classmethod
    def get_timestamp(cls):
        return int(time.time())
    
    def update_msg(self):
        self.timestamp = self.get_timestamp()
    
    def set_type(self, msg_type):
        self.msg_type = msg_type
    
    
    
class WeChatRespTextMsg(WeChatRespMsg):
    def __init__(self, to_user, from_user, content):
        WeChatRespMsg.__init__(self, to_user, from_user)
        self.content = content
        self.set_type('text')
        self.update_msg()



class WeChatRespMusicMsg(WeChatRespMsg):
    def __init__(self, to_user, from_user, title, desc, url, hqurl=u''):
        WeChatRespMsg.__init__(self, to_user, from_user)
        self.title = title
        self.desc = desc
        self.url = url
        self.hqurl = hqurl
        self.set_type('music')
        self.update_msg()



class WeChatRespNewsMsg(WeChatRespMsg):
    def __init__(self, to_user, from_user):
        WeChatRespMsg.__init__(self, to_user, from_user)
        self.set_type('news')
        self.news_list = []
        self.news_num = 0
        self.update_msg()
    
    def update_msg(self):
        WeChatRespMsg.update_msg(self)
        self.news_num = len(self.news_list)
    
    def append_news(self, title, picurl, desc=u'', url=u''):
        self.news_list.append({'title': unicode(title),
                                'desc': unicode(desc),
                                'picurl': unicode(picurl),
                                'url': unicode(url)})    
        self.update_msg()
    



