import requests
import time
import sys 
import os.path
from colorama import Fore 
"""
http://icanhazip.com/
http://checkip.dyndns.org/
https://freegeoip.net/json/
http://www.telize.com/ip
http://ip-api.com/json
http://curlmyip.com/
http://ipinfo.io/ip
"""
print(Fore.BLACK+f"""\033[1m

    -________________-_______________-
    -                                -
    -       Created by Error         -
    -________________-_______________-

\033[0m""")
ipFile="/tmp/ip.log"
timeout = 10

class Service:
  url=""
  def request(self): return requests.get(self.url, timeout = timeout)

class Icanhazip(Service):
  name="icanhazip"
  url="http://icanhazip.com/"
  def ip(self): return self.request().text.strip()

class Freegeoip(Service):
  name="freegeoip"
  url="https://freegeoip.net/json/"
  def ip(self): return self.request().json()["ip"]

class Telize(Service):
  name="telize"
  url="http://www.telize.com/ip"
  def ip(self): return self.request().text.strip()

class IpApi(Service):
  name="ip-api"
  url="http://ip-api.com/json"
  def ip(self): return self.request().json()["query"]

class Ifconfig(Service):
  name="ifconfig.me"
  url="http://ifconfig.me/all.json"
  def ip(self): return self.request().json()["ip_addr"]

def request_ip():
  services = [Icanhazip(), Freegeoip(), Telize(), IpApi(), Ifconfig() ]
  for i in range(len(services)):
    
    service = services[i]
    try:
      start = time.time()
      print (Fore.BLACK+"[+] Requesting current ip with '{}'".format(service.name))
      ip = service.ip()
      print(Fore.BLACK+"[+] Request took {} seconds ".format(int(time.time() - start)))
      return ip
    except Exception as error:
      print (Fore.BLUE+"[+] Exception when requesting ip using '{}': {} ".format(service.name, error ))
      
  error = "Non available services, add more services or increase the timeout (services = {}, timeout = {}) ".format(len(services), timeout)
  raise RuntimeError(error)

def current_ip():
  return open(ipFile,"r").readlines()[0]

def save_ip(ip):
  f = open(ipFile,'w')
  f.write(str(ip)) 

if os.path.isfile(ipFile) : 
  request_ip = request_ip()  
  current_ip = current_ip()

  if request_ip != current_ip:
    save_ip(request_ip)
    print(Fore.BLUE+"[+] IP has changed from {} to {}".format(current_ip, request_ip))
    sys.exit(1)

  else :
    print(Fore.BLUE+"[+] IP is still the same : {}".format(current_ip))

else: 
  request_ip = request_ip()
  save_ip(request_ip)
  print(Fore.BLACK+"[+] This is the first time to run the ip_change script, I will create a file in {} to store your current address: {} ".format(ipFile, request_ip))
