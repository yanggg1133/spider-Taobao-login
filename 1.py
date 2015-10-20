#coding:utf-8
__author__ = 'greatbuger'

import urllib,urllib2,cookielib,re,webbrowser


class Taobao:
    def __init__(self):
        self.loginURL = "https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fwww.taobao.com%2F"
        self.loginHeaders = {
            'Host':'login.taobao.com',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
            'Referer':'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fwww.taobao.com%2F',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Connection':'keep-alive'
        }
        self.username = 'greatbuger87534'
        self.ua = "059UW5TcyMNYQwiAiwTR3tCf0J/QnhEcUpkMmQ=|Um5Ockt1SXJPcEx1THVPdiA=|U2xMHDJ+H2QJZwBxX39Rb1V7W3UzUjRIORdBFw==|VGhXd1llXGJeZVhnW2JbYlhhVmtJdE57TnZNc091SnRMeEZ7QXRaDA==|VWldfS0TMwo/AiIeKwslUSVEKg5nDV04ByMIVydmC0ouAFYA|VmNDbUMV|V2NDbUMV|WGRYeCgGZhtmH2VScVI2UT5fORtmD2gCawwuRSJHZAFsCWMOdVYyVTpbPR99HWAFYVMpUDUFORshHiQdJR0jAT0JPQc/AD0HPAAiGjhfOFRqCDcdc0M+WSAKcRxwEWoHbBFPFlBgAH0AeVBvV2kiCzQMM39WaVFuIlwiXH4Dag1nDmlLIEciCzQMM39RcV9xJ3E=|WWdHFyMbOwA4GCQbLhs7DjoAIBwiGSICOAM2FioUKRU1DzYPWQ8=|WmBAED5hOnwoUThCOEYhWjZiXnBQbExySx1L|W2NDEz19KXENZwJjHkY7Ui9OJQsre09ySWlXY10LKxY2GDYWIh4qEUcR|XGZGFjhnPHouVz5EPkAnXDBkWHZWa0t/QH1FE0U=|XWdHFzl5LXUJYwZnGkI/VitKIQ8vEzMHOAQ4bjg=|XmdaZ0d6WmVFeUB8XGJaYEB4TGxWbk5yTndXa0tyT29Ta0t1QGBeZDI="
        self.password2  = '3w2f5958'
        self.post = {
           'ua':self.ua,
            'TPL_checkcode':'',
            'CtrlVersion': '1,0,0,7',
            'TPL_password':'',
            'TPL_redirect_url':'http://i.taobao.com/my_taobao.htm?nekot=udm8087E1424147022443',
            'TPL_username':self.username,
            'loginsite':'0',
            'newlogin':'0',
            'from':'tb',
            'fc':'default',
            'style':'default',
            'css_style':'',
            'tid':'XOR_1_000000000000000000000000000000_625C4720470A0A050976770A',
            'support':'000001',
            'loginType':'4',
            'minititle':'',
            'minipara':'',
            'umto':'NaN',
            'pstrong':'3',
            'llnick':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'full_redirect':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname':'10',
            'gvfdcre':'',
            'from_encoding ':'',
            'sub':'',
            'TPL_password_2':self.password2,
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp':'',
            'oslanguage':'zh-CN',
            'sr':'1366*768',
            'osVer':'windows|6.1',
            'naviVer':'firefox|35'
        }
        self.postData = urllib.urlencode(self.post)
        self.cookie = cookielib.LWPCookieJar()
        self.cookieHander = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.cookieHander)

    def needCheckCode(self):
        request = urllib2.Request(self.loginURL,self.postData,self.loginHeaders)
        response = self.opener.open(request)
        content = response.read().decode('gbk')
        status = response.getcode()
        if status == 200:
            print u" 获取请求成功"
            pattern = re.compile(u'\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801',re.S)
            result = re.search(pattern,content)
            #print content
            if result:
                print u"请输入验证码:"
                return content
            else:
                tokenPattern = re.compile('id="J_HToken"')
                tokenMatch = re.search(tokenPattern,content)
                if tokenMatch:
                    print u" 不需要验证码"
                    return False
        else:
            print u"获取失败"
            return None



    def getCheckCode(self,page):
        pattern = re.compile('<img id="J_StandardCode_m.*?data-src="(.*?)"',re.S)
        matchResult = re.search(pattern,page)
        if matchResult and matchResult.group(1):
            print matchResult.group(1)
            return matchResult.group(1)
        else:
            print u" 没有找到验证码的内容"
            return False


    def loginWithCheckCode(self):
        checkcode = raw_input('请输入验证码')
        self.post['TPL_checkcode'] = checkcode
        self.postData = urllib.urlencode(self.post)
        try:
            request = urllib2.Request(self.loginURL,self.postData,self.loginHeaders)
            response = self.opener.open(request)
            content = response.read().decode('gbk')
            pattern = re.compile(u'\u9a8c\u8bc1\u7801\u9519\u8bef',re.S)
            result = re.search(pattern,content)
            if result:
                print u"验证码输入错误"
                return False
            else:
                tokenPattern = re.compile('id="J_HToken" value="(.*?)"')
                tokenMatch = re.search(tokenPattern,content)
                if tokenMatch:
                    print u"验证码输入正确"
                    print tokenMatch.group(1)
                    return tokenMatch.group(1)
                else:
                    print u"J_Token"
                    return False

        except urllib2.HTTPError,e:
            print u"出错",e.reason
            return False






    def main(self):
        needResult = self.needCheckCode()
        if not needResult == None:

            if not needResult == False:
                print u"输入验证码"
                idenCode = self.getCheckCode(needResult)
                if not idenCode == False:
                    print u"验证码获取成功"
                    print u"请输入:"
                    webbrowser.open_new_tab(idenCode)
                    J_HToken = self.loginWithCheckCode()
                    print "J_HToken",J_HToken
                else:
                    print u" 验证码获取失败，请重试"
            else:
                print u"直接登入"
        else:
            print u"请求登入页面失败，"


taobao= Taobao()
taobao.main()
