# -*- coding: utf-8 -*-
#/usr/bin/env python

__version__ = '0.1'
__author__  = 'http://weibo.com/wtmmac'

'''
微信Server模拟
'''

import sys
py_major_ver = sys.version_info[0]
if py_major_ver == 3:
    print("python version:3")
    import urllib, time, hashlib, random
    import http.client as httplib
elif py_major_ver == 2:
    print("python version:2")
    import urllib, httplib, time, hashlib, random
else:
    print("python major version error({0})".format(py_major_ver))

# 配置
env = "bae"
if env == "bae":
    interface_url = '1.soulife.duapp.com'
    port = 80
else:
    interface_url = '127.0.0.1'
    port = 8000

interface_path = '/weixinpub'

Token = 'soulife'

messages = {
    # 用户关注消息
    'subscribe' : '''<xml><ToUserName><![CDATA[gh_a207d2fdeaec]]></ToUserName>
    <FromUserName><![CDATA[oAsR8jt8CRoyj8LBqosYAMUhi2v8]]></FromUserName>
    <CreateTime>123456789</CreateTime>
    <MsgType><![CDATA[event]]></MsgType>
    <Event><![CDATA[subscribe]]></Event>
    <EventKey><![CDATA[EVENTKEY]]></EventKey>
    </xml>''',
    # 用户取消关注消息
    'unsubscribe' : '''<xml><ToUserName><![CDATA[gh_a207d2fdeaec]]></ToUserName>
    <FromUserName><![CDATA[oAsR8jt8CRoyj8LBqosYAMUhi2v8]]></FromUserName>
    <CreateTime>123456789</CreateTime>
    <MsgType><![CDATA[event]]></MsgType>
    <Event><![CDATA[unsubscribe]]></Event>
    <EventKey><![CDATA[EVENTKEY]]></EventKey>
    </xml>''',
    # 用户发送文本信息
    'text': '''<xml>
    <ToUserName><![CDATA[gh_a207d2fdeaec]]></ToUserName>
    <FromUserName><![CDATA[oAsR8jt8CRoyj8LBqosYAMUhi2v8]]></FromUserName> 
    <CreateTime>1348831860</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[test text]]></Content>
    <MsgId>1234567890123456</MsgId>
    </xml>''',
    # 用户发送位置信息
    'location': '''<xml><ToUserName><![CDATA[gh_a207d2fdeaec]]></ToUserName><FromUserName><![CDATA[oAsR8jt8CRoyj8LBqosYAMUhi2v8]]></FromUserName><CreateTime>1376352417</CreateTime><MsgType><![CDATA[location]]></MsgType><Location_X>32.016609</Location_X><Location_Y>118.743431</Location_Y><Scale>20</Scale><Label><![CDATA[中華人民共和國江蘇省南京市建鄴區廬山路18号 邮政编码: 210019]]></Label><MsgId>5911388618785554663</MsgId></xml>''',
    #用户发送图片信息
    'image': '''<xml>
    <ToUserName><![CDATA[gh_a207d2fdeaec]]></ToUserName>
    <FromUserName><![CDATA[oAsR8jt8CRoyj8LBqosYAMUhi2v8]]></FromUserName>
    <CreateTime>1348831860</CreateTime>
    <MsgType><![CDATA[image]]></MsgType>
    <PicUrl><![CDATA[this is a url]]></PicUrl>
    <MsgId>1234567890123456</MsgId>
    </xml>''',
    #用户发送链接信息
    'link': '''<xml>
    <ToUserName><![CDATA[gh_a207d2fdeaec]]></ToUserName>
    <FromUserName><![CDATA[oAsR8jt8CRoyj8LBqosYAMUhi2v8]]></FromUserName>
    <CreateTime>1351776360</CreateTime>
    <MsgType><![CDATA[link]]></MsgType>
    <Title><![CDATA[公众平台官网链接]]></Title>
    <Description><![CDATA[公众平台官网链接]]></Description>
    <Url><![CDATA[url]]></Url>
    <MsgId>1234567890123456</MsgId>
    </xml>''',
    # 用户发送未知信息
    'other': '''<xml>
    <ToUserName><![CDATA[gh_a207d2fdeaec]]></ToUserName>
    <FromUserName><![CDATA[oAsR8jt8CRoyj8LBqosYAMUhi2v8]]></FromUserName> 
    <CreateTime>1348831860</CreateTime>
    <MsgType><![CDATA[other]]></MsgType>
    <Content><![CDATA[test text]]></Content>
    <MsgId>1234567890123456</MsgId>
    </xml>''',
}

def make_post(action):
    '''模拟用户行为产生的消息提交给接口程序'''
    conn = httplib.HTTPConnection(interface_url,port)

    headers = { "Content-type": "text/xml",
                "Content-Length": "{0}".format(len(messages[action]))}

    # 生成签名相关变量
    timestamp = str(int(time.time()))
    nonce = str(random.randint(1,100000))
    signature = makeSignature(Token, timestamp, nonce)
    
    if py_major_ver == 3:
        params = urllib.parse.urlencode({'signature': signature, 'timestamp': timestamp, 'nonce': nonce})
        conn.request("POST", interface_path + "?" +params, "", headers)
        conn.send(bytes(messages[action],encoding = 'utf-8'))
    elif py_major_ver == 2:
        params = urllib.urlencode({'signature': signature, 'timestamp': timestamp, 'nonce': nonce})
        conn.request("POST", interface_path + "?" +params, "", headers)
        conn.send(messages[action])

    response = conn.getresponse()

    print("{0} {1}".format(response.status,response.reason))
    print(response.read())

    conn.close() 
    
def makeSignature(Token, timestamp, nonce):
    '''生成签名'''
    try:
        Token = Token
    except Exception, e:
        pass

    sorted_arr = map(str, sorted([Token, timestamp, nonce]))

    sha1obj = hashlib.sha1()
    sha1obj.update(''.join(sorted_arr))
    hash = sha1obj.hexdigest()

    return hash

def listAction():
    print("======Supported actions:======")
    for i in messages.keys():
        print(i)
    print("==============================")

if __name__ == '__main__':
    if len(sys.argv) < 2:   
        print (u"Please input your action")
        listAction()
    else:
        if (sys.argv[1] in messages):
            from timeit import Timer
            t1=Timer("make_post(sys.argv[1])","from __main__ import make_post")
            co = 1
            total = t1.timeit(co)
            print("excute time {0} / {1} = {2} s.".format(total, co, total/co))
            #make_post(sys.argv[1])
        else:
            print("No this action")
            listAction()
