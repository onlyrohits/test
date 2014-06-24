import urllib2
import threading
import time
import sys
import ast

class Proxy:
	def __init__(self, timeout = 10, includeNewProxies = False, oldProxyFilePath = '', newProxyFilePath = '', proxyVerifyUrls = []):
		self.list = []
		self.count = 0
		self.timeout = timeout
		self.includeNewProxies = includeNewProxies
		self.oldProxyFilePath = oldProxyFilePath
		self.newProxyFilePath = newProxyFilePath
		self.proxyVerifyUrls = proxyVerifyUrls


	def isEmpty(self):
		return self.list == []


	def getProxies(self):
		proxies = self.getUsedProxyListFromFile()
		
		if not proxies or self.includeNewProxies == True :
			proxies += self.getNewProxyListFromFile()
		
		if proxies:
			self.list = self.verifyProxyList(proxies)
		
		self.writeToFile(self.oldProxyFilePath, 'w+', self.list)

		return True

	def getUsedProxyListFromFile(self):
		oldProxies = []

		f = open(self.oldProxyFilePath)

		for line in f.readlines():
			if line:
				oldProxy = ast.literal_eval(line.strip())
				oldProxy.update({'averageresponsetime' : 10.0})
				oldProxy.update({'slowresponsecount' : 0})
				oldProxy.update({'successcount' : 0})
				oldProxy.update({'errorcount' : 0})
				oldProxy.update({'lastresponsetime' : 0})
				oldProxy.update({'usedcount' : 0})
				oldProxy.update({'blacklist' : 0})

				oldProxies.append(oldProxy)
		
		return oldProxies


	def getNewProxyListFromFile(self):
		newProxies = []

		f = open(self.newProxyFilePath)

		for line in f.readlines():
			if line:
				line = line.strip().split(':')
				
				proxy = {}
				proxy.update({'ipaddress' : line[0]})
				proxy.update({'port' : line[1]})
				proxy.update({'type' : 'http'})
				proxy.update({'averageresponsetime' : 10.0})
				proxy.update({'slowresponsecount' : 0})
				proxy.update({'successcount' : 0})
				proxy.update({'errorcount' : 0})
				proxy.update({'lastresponsetime' : 0})
				proxy.update({'usedcount' : 0})
				proxy.update({'blacklist' : 0})
				
				newProxies.append(proxy)

		return newProxies


	def verifyProxyList(self, proxies):
		verifiedProxies = []
		count = 1

		for proxy in proxies:
			IP = proxy.get('ipaddress')
			PORT = proxy.get('port')
			TYPE = proxy.get('type')

			print "Trying %s ..." % IP

			IPADDR = TYPE + '://' + IP + ':' + PORT

			try:
				proxy_handler = urllib2.ProxyHandler({TYPE: IPADDR})
				opener = urllib2.build_opener(proxy_handler)
				opener.addheaders = [('User-agent', 'Mozilla/5.0')]
				urllib2.install_opener(opener)

				totalRequestTime = 0
				for url in self.proxyVerifyUrls:
					start = time.time()
					urllib2.urlopen(url, timeout = self.timeout)
					stop = time.time()

					totalRequestTime += round(stop - start, 1)

				totalRequestTime = round(totalRequestTime / len(self.proxyVerifyUrls), 1)

				if totalRequestTime <= self.timeout:
					proxy['averageresponsetime'] = totalRequestTime
				
				verifiedProxies.append(proxy)

				print '%s is OK' % IP + '. Average Request Time Taken: ' + str(totalRequestTime) + '\n'
			except urllib2.HTTPError:
				print '%s is not OK' % IP + '\n'
			except Exception:
				print '%s is not OK' % IP + '\n'

		return sorted(verifiedProxies, key=lambda k: k['averageresponsetime'])


	def writeToFile(self, filename, mode, items):
		f = open(filename, mode)

		for item in items:
			f.write(str(item) + '\n')

		f.close()

		return True

	
	def getMeData(self, url):
		proxy = (item for item in self.list if item["blacklist"] == 0).next()

		IP = proxy.get('ipaddress')
		PORT = proxy.get('port')
		TYPE = proxy.get('type')

		IPADDR = TYPE + '://' + IP + ':' + PORT
		responseTime = 0.0
		try:
			proxy_handler = urllib2.ProxyHandler({TYPE: IPADDR})
			opener = urllib2.build_opener(proxy_handler)
			opener.addheaders = [('User-agent', 'Mozilla/5.0'),('Accept-encoding', 'gzip')]
			urllib2.install_opener(opener)

			start = time.time()
			request = urllib2.urlopen(url, timeout = self.timeout)
			response = request.read()
			stop = time.time()

			responseTime = round(stop - start, 1)
			(item for item in self.list if item["ipaddress"] == IP).next().update({'successcount' : proxy.get('successcount') + 1, 'lastresponsetime': responseTime, 'usedcount': proxy.get('usedcount') + 1})
			
			print self.list
			return response

		except urllib2.HTTPError:
			print '%s is not OK' % IP + '\n'
		except urllib2.URLError, e:
			print e.args
		except Exception:
			print '%s is not OK' % IP + '\n'

		(item for item in self.list if item["ipaddress"] == IP).next().update({'errorcount' : proxy.get('errorcount') + 1, 'lastresponsetime': 0.0, 'usedcount': proxy.get('usedcount') + 1})

		
		if responseTime > (proxy.get('averageresponsetime') + round(proxy.get('averageresponsetime') / 3, 1)):
			(item for item in self.list if item["ipaddress"] == IP).next().update({'slowresponsecount': proxy.get('slowresponsecount') + 1})

		(item for item in self.list if item["ipaddress"] == IP and (item['errorcount'] == 5 or item['slowresponsecount'] == 5)).next().update({'blacklist': 1})			

		print self.list
		return {}