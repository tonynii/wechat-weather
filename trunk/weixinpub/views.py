#!/usr/bin/env python
# coding=utf-8

from django.http import HttpResponse

from weixinpub.models import WeixinMsg
import public.applogging as logging


#消息结构
textTpl = u"""<xml>
            <ToUserName><![CDATA[{0}]]></ToUserName>
            <FromUserName><![CDATA[{1}]]></FromUserName>
            <CreateTime>{2}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{3}]]></Content>
            </xml>"""
musicTpl = u""" <xml>
            <ToUserName><![CDATA[{0}]]></ToUserName>
            <FromUserName><![CDATA[{1}]]></FromUserName>
            <CreateTime>{2}</CreateTime>
            <MsgType><![CDATA[music]]></MsgType>
            <Music>
            <Title><![CDATA[{3}]]></Title>
            <Description><![CDATA[{4}]]></Description>
            <MusicUrl><![CDATA[{5}]]></MusicUrl>
            <HQMusicUrl><![CDATA[{6}]]></HQMusicUrl>
            </Music>
            </xml>"""
newsTpl = u"""<xml>
            <ToUserName><![CDATA[{0}]]></ToUserName>
            <FromUserName><![CDATA[{1}]]></FromUserName>
            <CreateTime>{2}</CreateTime>
            <MsgType><![CDATA[news]]></MsgType>
            <ArticleCount>{3}</ArticleCount>
            <Articles>
            {4}
            </Articles>
            </xml> """
newsBody = u"""<item>
            <Title><![CDATA[{0}]]></Title>
            <Description><![CDATA[{1}]]></Description>
            <PicUrl><![CDATA[{2}]]></PicUrl>
            <Url><![CDATA[{3}]]></Url>
            </item>"""


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
        rcevmsg = WeixinMsg(timestamp, signature, nonce)
        if rcevmsg.verifysignature():
            restype, resdata = rcevmsg.msghandle(data)
            echostr = buildresponse(restype, resdata, host)
            logging.debug(u'Reponse data is: {0}'.format(echostr.replace('\n','')))
        else:
            logging.error(u'Verify signature error!!!')
            echostr = 'Verify signature error!!!'
        return HttpResponse(echostr)
    else:
        return HttpResponse('other')

def buildresponse(restype, resdata, host):
    if restype == 'text':
        echostr = textdecode(resdata[0],resdata[1],resdata[2],resdata[3])
    elif restype == 'music':
        pass
    elif restype == 'news':
        news_list = [[u'您所在区域天气如下：', u' ', 'http://{0}/static/weixinpub/top02.jpg'.format(host),u' '],
                    [resdata[3][0][0], u' ', resdata[3][0][1],u' '],
                    [resdata[3][1][0], u' ', resdata[3][1][1],u' ']]
                    #[resdata[3][2][0], u' ', resdata[3][2][1],u' ']]
        echostr = newsdecode(resdata[0],resdata[1],resdata[2], news_list)
    else:
        logging.warning('MsgType error!({0})'.format(restype))
        #echostr = self.textdecode(resdata[0],resdata[1],resdata[2],resdata[3])
    return echostr

def textdecode(toname, fromname, timestamp, msg): 
    echostr = textTpl.format(toname, fromname,timestamp,unicode(msg))
    return echostr

def newsdecode(toname, fromname, timestamp, newslists):
    nbody = ''
    for i in newslists:
        nbody += newsBody.format(unicode(i[0]),
                                 unicode(i[1]),
                                 unicode(i[2]),
                                 unicode(i[3]))
    
    echostr = newsTpl.format(toname, fromname, timestamp,len(newslists),nbody)
    return echostr

