#!/usr/bin/env python
# coding=utf-8
from django.db import models
from django.utils import timezone

import time
import hashlib
from lxml import etree

import public.applogging as logging
import public.config as config
from weixinpub.weather import Weather



#提示信息
tipstr = u'如鱼饮水，冷暖自知。发送位置信息可以获取天气信息哦！现在就试试吧！'
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
    
    def bodydecode(self,msgbody):
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
        self.from_user = recv['FromUserName']
        self.to_user = recv['ToUserName']
        return recv
    
    def get_from_user(self):
        return self.from_user
    
    def get_to_user(self):
        return self.to_user
    
    def msghandle(self, msgbody):
        recv = self.bodydecode(msgbody)
        res_type = 'text'
        res_msg = tipstr
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
                res_type = 'news'
                res_msg = news_list
            elif recv['MsgType'] == 'image':
                pass
            elif recv['MsgType'] == 'link':
                pass
            elif recv['MsgType'] == 'event':
                if recv['Event'] == 'subscribe':
                    res_type = 'text'
                    res_msg = welcomestr
                    #save user info to db
                    try:
                        user_info = WechatUser.objects.get(open_id=recv['FromUserName'])
                    except WechatUser.DoesNotExist:
                        logging.info("{0} will be add to database.".format(recv['FromUserName']))
                        user_info = WechatUser(open_id=recv['FromUserName'],
                                               has_init=False,
                                               data = time.strftime("%Y-%m-%d", time.localtime()))
                        user_info.save()
                    else:
                        logging.info("{0} will be init in database.".format(recv['FromUserName']))
                        user_info.has_init = False
                        user_info.data = time.strftime("%Y-%m-%d", time.localtime())
                        user_info.save()
                    
                elif recv['Event'] == 'unsubscribe':
                    res_type = 'text'
                    res_msg = byestr
                    #delete user info to db
                    try:
                        user_info = WechatUser.objects.get(open_id=recv['FromUserName'])
                    except WechatUser.DoesNotExist:
                        logging.warning("{0} isn't in the database yet.".format(recv['FromUserName']))
                    else:
                        logging.info("{0} will be delete form database.".format(recv['FromUserName']))
                        user_info.delete()
                    
                elif recv['Event'] == 'CLICK':
                    res_type = 'text'
                    res_msg = otherstr
                else:
                    res_type = 'text'
                    res_msg = otherstr
                    logging.warning('Event type error!({0})'.format(recv['Event']))
            else:
                logging.warning('MsgType error!({0})'.format(recv['MsgType']))
                res_type = 'text'
                res_msg = otherstr
        else:
            res_type = 'error'
            res_msg = 'Msg handle error!!!'
        return res_type, res_msg

class WechatUser(models.Model):
    open_id = models.CharField(max_length=50)
    has_init = models.BooleanField()
    data = models.DateField()
    name = models.CharField(max_length=30, null = True)
    city = models.CharField(max_length=60, null = True)
    state_province = models.CharField(max_length=30, null = True)
    country = models.CharField(max_length=50, null = True)
    longitude = models.FloatField(null = True)
    latitude = models.FloatField(null = True)
    
    def __unicode__(self):
        return self.open_id

