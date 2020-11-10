import os.path
import requests
import threading
import json
import re
import math
import socket

# Checking HTTP or HTTPS. 
# Check HTTP by providing a HTTP link.
# Check HTTPS by providing a HTTPS link;

checkLink = 'add-url-here'
proxyValueChecker = 'add-value-of-checkLinkHere' # Value provided on the page;
threads = 300
deadCount = 0
aliveCount = 0

# Loading the proxies from the text file into an array format;

def loadProxies(filename):
	try:
		stocks = open(filename).read().splitlines()
		proxies = []
		#print(stocks)
		for line in stocks:
			proxies.append(line)
		return proxies
	except:
		print('File was not found')
		return False


# Function to test if the proxy is alive

def checkProxy(proxy):
		global deadCount, aliveCount
		proxies = {'http': 'http://' + proxy, 'https': 'http://' + proxy}
		try:
			checkStart = time.time()
			rProxy = requests.get(checkLink, proxies=proxies, timeout=1)
			if rProxy.text == proxyValueChecker:
					f = open('working_proxies.txt', 'a')
					f.write(proxy + "\n")
					f.close()
					print(proxy)
					aliveCount += 1
					return True
		except:
			deadCount += 1
			return False


def split_processing(items, num_splits=threads):
    split_size = len(items) // num_splits
    threads = []
    for i in range(num_splits):
        start = i * split_size
        end = (None if i + 1 == num_splits else (i + 1) * split_size)
        threads.append(threading.Thread(target=process, args=(items,
                       start, end)))
        threads[-1].start()
    for t in threads:
        t.join()


def process(items, start, end):
    for item in items[start:end]:
        try:
            checkProxy(item)
        except Exception as err:
            print (err)


# Start the proccess

def start():
	list = input("[LIST] Provide proxy list (proxies.txt): ")
	proxyList = loadProxies(list)
	if proxyList == False:
			print ()
	else:
			print ('[SUCCESS] Proxies successfully retrieved from source.')
			print ('[STARTING] Proxy Checker is starting up...')
			split_processing(proxyList)
			print ('Found ' + str(aliveCount) + ' alive proxies and ' + str(deadCount) +' dead proxies....')
			#time.sleep(60)
			#start()


# Captcha the users input.

print ('LiteDev Proxy Checker v0.wtf.')
start()

input("Press Enter to quit...")

