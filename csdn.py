#!/usr/bin/python
#encoding:utf-8

import re
import urllib
import urllib2
import requests
import cookielib
from bs4 import BeautifulSoup

class CSDN(object):
    """
    csdn网站抓取工具
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_url = 'https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn'
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
        self.main_page_url = 'http://my.csdn.net/my/mycsdn'

    def login(self):
        """
        无cookie方式登录csdn
        :return:
        """
        # 获取登录界面
        html = urllib.urlopen(self.login_url).read()
        data = urllib.urlencode(self.__parse_login_html(html))
        action = re.search(r'action=\"(.*?)\"', html).group(1)
        print action

        #登录
        response = urllib.urlopen("https://passport.csdn.net/" + action, data)

        print response.read()

    def view_main(self):
        """
        无cookie方式访问个人主页
        注：再禁用cookie的情况下，不能进入登录后界面
        :return:
        """
        headers = self.__prepare_headers()
        headers['Referer'] = 'http://my.csdn.net'
        request = urllib2.Request(self.main_page_url, headers=headers)
        response = urllib2.urlopen(request)
        print response.read()

    def login_cookie(self):
        """
        cookie方式登录csdn
        :return:
        """
        cookie = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        response = opener.open(self.login_url)
        html = response.read()

        data = self.__parse_login_html(html)
        response = opener.open(self.login_url, urllib.urlencode(data))
        print response.read()
        print cookie
        self.view_main_cookie(opener)


    def view_main_cookie(self, opener):
        """
        cookie方式访问个人主页
        :return:
        """
        headers = self.__prepare_headers()
        headers['Referer'] = 'http://my.csdn.net'
        opener.addheaders = list(headers.items())
        print opener.open(self.main_page_url).read()


    def login_session(self):
        """
        session方式登录csdn
        :return:
        """
        session = requests.session()
        # 获取登录界面
        html = session.get(self.login_url).text
        data = self.__parse_login_html_bs4(html)

        # 登录csdn
        response = session.post(self.login_url, data)
        print response.text
        self.view_main_session(session)

    def view_main_session(self, session):
        """
        session方式访问个人主页
        :return:
        """
        headers = self.__prepare_headers()
        headers['Referer'] = 'http://my.csdn.net'
        print session.get(self.main_page_url, headers=headers).text

    def __parse_login_html(self, html):
        """
        解析login界面中隐藏form参数
        :param html: login界面的html
        :return: 返回登录form参数
        """
        lt = re.search(r'name=\"lt\" value=\"(.*?)\"', html).group(1)
        execution = re.search(r'name=\"execution\" value=\"(.*?)\"', html).group(1)
        _eventId = re.search(r'name=\"_eventId\" value=\"(.*?)\"', html).group(1)
        return {
            'username': self.username,
            'password': self.password,
            'lt': lt,
            'execution': execution,
            '_eventId': _eventId
        }

    def __parse_login_html2(self, html):
        """
        自动解析hidden元素
        :param html:
        :return:
        """
        pattern = r'input type="hidden" name="(.*?)" value="(.*?)"'
        values_re = re.compile(pattern, re.M | re.I)
        values = re.findall(values_re, html)
        values = dict(values)
        values.update({
            'username': self.username,
            'password': self.password
        })
        return values

    def __parse_login_html_bs4(self, html):
        """
        用bs4解析hidden元素
        :param html:
        :return:
        """
        values = {}
        soup = BeautifulSoup(html, "html.parser")
        inputs = soup.find_all('input', type='hidden')
        for input in inputs:
            values[input.get('name')] = input.get('value')

        values.update({
            'username': self.username,
            'password': self.password
        })
        return values

    def __prepare_headers(self):
        """
        构建csdn网站请求头
        :return:
        """
        header = {
            'User-Agent': self.user_agent,
            'Connection': 'keep-alive',
        }
        return header


csdnobj = CSDN('username', 'password')
csdnobj.login_session()