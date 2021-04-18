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
				print(objHostname)
				# If record is an A record
				if objHostname.get('type') == 'A':
					# If the assignment is not an internal address and the assignment differs from the current public IP address
					if objHostname.get('content')[0:4] != '10.5' and objHostname.get('content') != strPublicIP:
						url = urljoin(PORKBUN_API_ENDPOINT, f"dns/edit/{strDomain}/{objHostname.get('id')}")
						strHostName = objHostname.get('name')
						req_json = {"apikey": PORKBUN_API_KEY, "secretapikey": PORKBUN_API_SECRET, "name": strHostName.replace(f'.{strDomain}',''), "type": objHostname.get('type'), "content": strPublicIP, "ttl": '300'}
						r = requests.post(url=url, json=req_json)
						print(f"Updating {objHostname.get('name')} to {strPublicIP}:\n{r.status_code} -- {r.text}")
					else:
						print(f"Host {objHostname.get('name')} does not need to be updated -- assignment is already {objHostname.get('content')}")

		else:
			print("Unable to get hosts in zone {strDomain}:\n")
			print(f"Request response text: {r.status_code} -- {r.text}")

else:
	print("Unable to get public IP:\n")
	print(f"Request response text: {r.status_code} -- {r.text}")

