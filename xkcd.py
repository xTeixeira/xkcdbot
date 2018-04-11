import urllib
import json
import random
import requests

def getComic(number):
	resp = requests.get('http://xkcd.com/'+str(number)+'/info.0.json', timeout=1)
	if resp.status_code != 200:
		return;
	
	return resp.json()

def getLatestComic():
	resp = requests.get('http://xkcd.com/info.0.json', timeout=1)
	if resp.status_code != 200:
		return;
	
	return resp.json()

def getRandomComic(maxNumber):
	resp = requests.get('http://xkcd.com/'+str(random.randint(1, maxNumber))+'/info.0.json', timeout=1)
	if resp.status_code != 200:
		return;
	
	return resp.json()