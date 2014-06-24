from Proxy import *
import socket
#socket.setdefaulttimeout(60)

p = Proxy(60, False, 'workingproxy.txt', 'proxies.txt', ['https://www.qaparichay.in'])

p.getProxies()
import time
start_time = time.time()
ghtml = p.getMeData('http://www.spokeo.com/email-search/search?e=rohit.kkumar@gmail.com')
import gzip
print ghtml
import StringIO
compressedstream = StringIO.StringIO(ghtml)
f = gzip.GzipFile(fileobj=compressedstream)
html = f.read()
print html
print("--- %s seconds ---" % (time.time() - start_time))

# p.getMeData('https://www.qaparichay.in')
# p.getMeData('https://www.qaparichay.in')
# p.getMeData('https://www.qaparichay.in')
# p.getMeData('https://www.qaparichay.in')
# p.getMeData('https://www.qaparichay.in')
# p.getMeData('http://api.meetup.com/2/member/2?key=59194e36d4381f353e1151602c29f')
# p.getMeData('http://api.meetup.com/2/member/3?key=59194e36d4381f353e1151602c29f')
# p.getMeData('http://api.meetup.com/2/member/4?key=59194e36d4381f353e1151602c29f')
# p.getMeData('http://api.meetup.com/2/member/5?key=59194e36d4381f353e1151602c29f')
# p.getMeData('http://api.meetup.com/2/member/6?key=59194e36d4381f353e1151602c29f')
# p.getMeData('http://api.meetup.com/2/member/7?key=59194e36d4381f353e1151602c29f')
# p.getMeData('http://api.meetup.com/2/member/8?key=59194e36d4381f353e1151602c29f')
# p.getMeData('http://api.meetup.com/2/member/9?key=59194e36d4381f353e1151602c29f')
# p.getMeData('http://api.meetup.com/2/member/10?key=59194e36d4381f353e1151602c29f')