#coding:utf-8
import requests
from PIL import Image
from bs4 import BeautifulSoup
import re
import os
import linecache
#请求登录界面的viewstate
sessions = requests.session()
r = sessions.get("http://202.115.80.153/default5.aspx")
c = r.content
mysoup = BeautifulSoup(c, 'html.parser')
inputstring = mysoup.find_all('input', attrs={"name":"__VIEWSTATE"})
inputstring = inputstring[0]
viewstate = inputstring['value']


#login 登录信息
if not os.path.exists('E:\\yonghu'):
	os.makedirs('E:\\yonghu')
	f = open('E:\\yonghu\\shuju.txt','w')
	username = input("请输入用户名:")
	password = input("请输入密码：")
	f.write(username+"\n"+password+"\n")
	f.close()	
name = input("名字:")	
usernames = linecache.getline('E:\\yonghu\\shuju.txt', 1)
passwords = linecache.getline('E:\\yonghu\\shuju.txt', 2)
username = str(usernames).replace('\n','')
password = str(passwords).replace('\n','')
linecache.clearcache()
学年 = input("学年(格式xxx-xxx)：")
学期 = input("学期(1或者2):")
url = "http://202.115.80.153/default5.aspx"

#获取验证码
captcha_url = "http://202.115.80.153/CheckCode.aspx"
capr  = sessions.get(captcha_url)
with open('captcha.jpg', 'wb') as f:
	f.write(capr.content)
	f.close()
	im = Image.open('captcha.jpg')
	im.show()
code = input('验证码:')
refer = "http://202.115.80.153/xs_main.aspx?xh="+username

#构造post数据
datas = {'__VIEWSTATE':viewstate,
'TextBox1':username,
'TextBox2':password,
'TextBox3':code,
'RadioButtonList1':'学生',
'Button1':'登录',
'lbLanguage': '',
'hidPdrs': '',
'hidsc': ''
}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
response = sessions.post(url,headers=headers, data=datas)


#构造跳转页面的数据，因为无法直达，所以必须跳转一次
headerss = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Host':'202.115.80.153',
'Referer':refer,
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
Url = 'http://202.115.80.153/xscj_gc.aspx?xh='+username+'&xm='+name+'&gnmkdm=N121605'
responses = sessions.post(Url,headers=headerss)

#获取跳转页面的viewstate
mysoups = BeautifulSoup(responses.content, 'html.parser')
inputstrings = mysoups.find_all('input', attrs={"name":"__VIEWSTATE"})
inputstrings = inputstrings[0]
viewstates = inputstrings['value']

#构造请求成绩页面的数据
score_headers = {'Referer':refer,
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}
score_data = {'__VIEWSTATE':viewstates,
'ddlXN':'',
'ddlXQ':'',
'Button1':'按学期查询'
}
#回应的网页
score_response = sessions.post(Url,data=score_data,headers=score_headers)

#得到请求的网页内容
content = score_response.content

#利用beautifulsoup解析
soup = BeautifulSoup(content, 'html.parser')

#正则
title = r'<td>'+学年+'</td><td>'+学期+'</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>'
title_source = re.compile(title)
titles = re.findall(title_source,str(soup))
for line in titles:
	body = str(line)
	content = body.replace('\'','')
	contents = content.strip('(,)')
	contentss = contents.replace(', \\xa0','')
	print(contentss+"\n")
	
	
a = input('回车退出：')

	


		
	





