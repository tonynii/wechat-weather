#!/usr/bin/env python
# coding=utf-8
from django.db import models
from django.utils import timezone

import hashlib
from lxml import etree

import public.applogging as logging
import public.config as config
from weixinpub.weather import Weather



#提示信息
tipstr = u'嘿嘿！发送位置信息可以获取天气信息哦！现在就试试吧！'
welcomestr = u'嗨！欢迎您的关注，关怀冷暖，体贴入微！现在发送位置信息就可以获取天气信息啦！'
byestr = u'嘿嘿！欢迎您再次使用本服务，关怀冷暖，体贴入微！'
otherstr = u'嘿嘿！你的心思我怎么猜也猜不透！'

class WeixinMsg(object):
    '''微信消息处理'''
    def __init__(self, timestamp, signature, nonce, host = None, otherpara = None):
        self.signature = signature
        self.timestamp = timestamp
        self.nonce = nonce
        self.host = host
        self.otherpara = otherpara
        
        self.from_user = ''
        self.to_user = ''
    
    def verifysignature(self):
        '''加密/校验流程：
            1. 将token、timestamp、nonce三个参数进行字典序排序
            2. 将三个参数字符串拼接成一个字符串进行sha1加密
            3. 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信'''
        ret = False
        #获取TOKEN
        token = config.WECHATPUB['token']
        
        #对微信发送的请求，做验证
        tmplist = [ self.timestamp, token, self.nonce ]
        tmplist.sort()
        tmpstr = ''.join( tmplist )
        hashstr = hashlib.sha1( tmpstr ).hexdigest()

        #如果相等，返回True
        if hashstr == self.signature:
            ret = True
        return ret
    
    @classmethod
    def bodydecode(cls,msgbody):
        #解析XML内容
        utf8_parser = etree.XMLParser(encoding='utf-8')
        try:
            root = etree.fromstring( msgbody, parser=utf8_parser )
        except:
            logging.warning('recive data handle error!')
            return None
        child = list( root )
        recv = {}
        tmpstr = ''
        for i in child:
            recv[i.tag] = i.text
            tmpstr += u'{0}: {1}, '.format(i.tag, i.text)
        logging.debug('recive data handle to: {0}'.format(tmpstr.encode('utf-8')))
        return recv
    
    def get_from_user(self):
        return self.from_user
    
    def get_to_user(self):
        return self.to_user
    
    def msghandle(self, msgbody):
        recv = self.bodydecode(msgbody)
        self.from_user = recv['FromUserName']
        self.to_user = recv['ToUserName']
        res = ('text', tipstr)
        if recv:
            if recv['MsgType'] == 'text':
                pass
            elif recv['MsgType'] == 'location':
                weather_obj = Weather()
                logging.debug('location data is: {0} {1} '.format(recv['Location_Y'],
                                               recv['Location_X']))
                weather_info = weather_obj.getweatherbydegree(recv['Location_Y'],
                                               recv['Location_X'])
                news_list = [[u'您所在区域天气如下：', u' ', 'http://{0}/static/weixinpub/top02.jpg'.format(self.host),u' '],
                            [weather_info[0][0] + ' ' + weather_info[0][1], u' ', weather_info[0][2], u''],
                            [weather_info[2][0] + ' ' + weather_info[2][1], u' ', weather_info[2][2], u'']]
                res = ('news', news_list)
            elif recv['MsgType'] == 'image':
                pass
            elif recv['MsgType'] == 'link':
                pass
            elif recv['MsgType'] == 'event':
                if recv['Event'] == 'subscribe':
                    res = ('text',welcomestr)
                elif recv['Event'] == 'unsubscribe':
                    res = ('text', byestr)
                elif recv['Event'] == 'CLICK':
                    res = ('text',otherstr)
                else:
                    res = ('text', otherstr)
                    logging.warning('Event type error!({0})'.format(recv['Event']))
            else:
                logging.warning('MsgType error!({0})'.format(recv['MsgType']))
                res = ('text', otherstr)
        else:
            res = ('error', 'Msg handle error!!!')
        return res

