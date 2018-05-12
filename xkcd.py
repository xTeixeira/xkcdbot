import urllib
import json
import random
import requests
import time

class APIException(Exception):
	def __init__(self, message):
		self.message = message

def getComic(number, retries=5):
	for nretries in range(retries):
		resp = requests.get('http://xkcd.com/'+str(number)+'/info.0.json', timeout=1)
		if resp.status_code == 200:
			return resp.json()
		time.sleep(1)
	
	raise APIException("Invalid answer from API.")

def getLatestComic(retries=5):
	for nretries in range(retries):
		resp = requests.get('http://xkcd.com/info.0.json', timeout=1)
		if resp.status_code == 200:
			return resp.json()
		time.sleep(1)
	
	raise APIException("Invalid answer from API.")

def getRandomComic(maxNumber, retries=5):
	for nretries in range(retries):
		resp = requests.get('http://xkcd.com/'+str(random.randint(1, maxNumber))+'/info.0.json', timeout=1)
		if resp.status_code == 200:
			return resp.json()
		time.sleep(1)
	
	raise APIException("Invalid answer from API.")
