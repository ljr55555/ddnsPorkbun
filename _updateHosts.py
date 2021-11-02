#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import required modules
import requests
import json
from urllib.parse import urljoin
from config import PORKBUN_API_ENDPOINT, PORKBUN_API_KEY, PORKBUN_API_SECRET, DOMAINS

# Get public IP address
url = urljoin(PORKBUN_API_ENDPOINT, "ping")
req_json = {"apikey": PORKBUN_API_KEY, "secretapikey": PORKBUN_API_SECRET}
r = requests.post(url=url, json=req_json)

if r.status_code == 200:
	strPublicIP = json.loads(r.text).get("yourIp", None)
	# For each domain, get records
	for strDomain in DOMAINS:
		url = urljoin(PORKBUN_API_ENDPOINT, "dns/retrieve/{}".format(strDomain))
		req_json = {"apikey": PORKBUN_API_KEY,"secretapikey": PORKBUN_API_SECRET}
		r = requests.post(url=url, json=req_json)
		
		if r.status_code == 200:
			objRecords = json.loads(r.text).get("records", None)
			for objHostname in objRecords:
				# Only update A records
				if objHostname.get('type') == 'A':
					# If the assignment is not an internal address and the assignment differs from the current public IP address
					if objHostname.get('content')[0:4] != '10.5' and objHostname.get('content') != strPublicIP:	# Only update records where public IP differs
						url = urljoin(PORKBUN_API_ENDPOINT, f"dns/edit/{strDomain}/{objHostname.get('id')}")
						# Domain component needs to be removed from hostname to avoid changing records to host.example.com.example.com
						# May also be able to post-pend dot to indicate fully qualified name
						strHostName = objHostname.get('name')
						strHostName = strHostName.replace(f".{strDomain}","")
						# Hostname matching domain name needs to be handed differently as null name fields are not allowed
						if strHostName == strDomain:
							req_json = {"apikey": PORKBUN_API_KEY, "secretapikey": PORKBUN_API_SECRET, "type": objHostname.get('type'), "content": strPublicIP, "ttl": '300'}
						else:
							req_json = {"apikey": PORKBUN_API_KEY, "secretapikey": PORKBUN_API_SECRET, "name": strHostName, "type": objHostname.get('type'), "content": strPublicIP, "ttl": '300'}
						r = requests.post(url=url, json=req_json)
						#print(f"Sent {req_json} to {url}")
						print(f"Updating {objHostname.get('name')} to {strPublicIP}:\n{r.status_code} -- {r.text}")
					#else:
					#	print(f"Host {objHostname.get('name')} does not need to be updated -- assignment is already {objHostname.get('content')}")

		else:
			print("Unable to get hosts in zone {strDomain}:\n")
			print(f"Request response text: {r.status_code} -- {r.text}")

else:
	print("Unable to get public IP:\n")
	print(f"Request response text: {r.status_code} -- {r.text}")

