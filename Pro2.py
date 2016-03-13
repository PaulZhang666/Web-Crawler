import urllib, urllib2, cookielib, re
from collections import deque

firstgeturl = 'http://cs5700sp16.ccs.neu.edu/accounts/login/?next=/fakebook/'
posturl = 'http://cs5700sp16.ccs.neu.edu/accounts/login/'
finalgeturl = 'http://cs5700sp16.ccs.neu.edu/fakebook/'

cj = cookielib.CookieJar()
cookie_hanler = urllib2.HTTPCookieProcessor(cj)

req = urllib2.Request(firstgeturl)
opener = urllib2.build_opener(cookie_hanler)
urllib2.install_opener(opener)
contents = opener.open(req)
contents = contents.read()
# print contents

cookies = ''
for index, cookie in enumerate(cj):
	cookies = cookies + cookie.name + "=" + cookie.value + ";"
cookie = cookies[:-1]
#print cookies

token = re.compile('csrfmiddlewaretoken\'.*?value=\'(.*?)\'')
qqq = re.findall(token, contents)
csrf = qqq[0]
#print csrf

postdata = urllib.urlencode({
	'username': '001618402',
	'password': 'FDLTX2RV',
	'csrfmiddlewaretoken': csrf,
	'next': '/fakebook/'
})

''' Totally no use...
header = {
	'Host': 'cs5700sp16.ccs.neu.edu',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding': 'gzip,deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'Content-Length': '109',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Cookie': '__utma=206999436.1724549389.1447087345.1447362068.1447637628.4; __utmz=206999436.1447637628.4.4.utmcsr=northeastern.edu|utmccn=(referral)|utmcmd=referral|utmcct=/graduate/programs/electrical-and-computer-engineering/; _ga=GA1.2.1864593473.1447291178;' + cookie,
	'Origin': 'http://cs5700sp16.ccs.neu.edu',
	'Referer': 'http://cs5700sp16.ccs.neu.edu/accounts/login/?next=/fakebook/',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
}
'''

class RedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_302(self,req,fp,code,msg,headers):
		pass

opener = urllib2.build_opener(RedirectHandler,cookie_hanler)
request = urllib2.Request(posturl, postdata)

try:
	response = opener.open(request)
except:
	result = opener.open(finalgeturl)
result = result.read()
#print result

queue = deque()
visited = set()
queue.append(finalgeturl)
count = 0

originurl = 'http://cs5700sp16.ccs.neu.edu/fakebook/'
flag = 0
flagset = set()

while queue and flag < 5:
	url = queue.popleft()

	#visited.add(str(url))
	#print visited
	#print len(visited)
	#print count
	count += 1

	try:
		if url not in visited:
			urlop = urllib2.urlopen(url)
			visited.add(str(url))
			#print url
	except:
		continue
	try:
		data = urlop.read().decode('utf-8')
	except:
		continue

	name = re.compile('a href=\"/fakebook/(\d+)/\">')
	page = re.compile('<p>Page \d of (\d)')
	friend = re.compile('a href=\"/fakebook/(\d+/friends/\d+/)')
	secret_flag = re.compile('([0-9a-zA-Z]{64})')
	'''
	for p in page.findall(data):
		if p != -1:
			i = 2
			while i <= p:
				sss = str(url)
				queue.append(sss[:-2]+str(i))
				i += 1
    '''

	for x in name.findall(data):
		if originurl+x not in visited:
			url = originurl+x
			queue.append(url)

	for y in friend.findall(data):
		if originurl+y not in visited:
			url = originurl+y
			queue.append(url)

	for f in secret_flag.findall(data):
		if f not in flagset:
			print f
			flagset.add(f)
			flag += 1




























