import requests
import argparse
import logging
import json
import sys
import re

class history:
	def __init__(self, Data):
		self.data = Data
	def getMainPageCont(self):
		try:
			cont = self.data["continuationContents"]["sectionListContinuation"]["continuations"][1]["reloadContinuationData"]["continuation"]
			return cont
		except KeyError:
			logError('make sure that Auth token is set correctly')
			
	def getMainList(self):
		return self.data["continuationContents"]["sectionListContinuation"]["contents"]

	def getListVideos(self):
		Videos = {}
		HistoryList = self.getMainList()
		for i in HistoryList:
			mainlist = i["itemSectionRenderer"]["contents"]
			date = i["itemSectionRenderer"]["header"]["itemSectionHeaderRenderer"]["title"]["runs"][0]["text"]
			Videos[date] = []
			for j in mainlist:

				Id = j["compactVideoRenderer"]["videoId"]

				try:	
					Title = j["compactVideoRenderer"]["title"]["runs"][0]["text"]
				except:
					# for Empty Title Names
					Title = ""
				try:		
					Channel = j["compactVideoRenderer"]["longBylineText"]["runs"][0]["text"]
				except:
					# for Empty Channel Names
					Channel = ""	

				Videos[date].append({"ID":Id,"Title": Title,"Channel":Channel})

		return Videos
	
	def getNextCont(self):
		try:
			return self.data["continuationContents"]["sectionListContinuation"]["continuations"][0]["nextContinuationData"]["continuation"]
		except:
			#when it reaches the end
			return None

def getAPIKey():
	sw = requests.get('https://youtube.com/sw.js')

	script = re.findall(r'ytcfg\.set\(({.+?}},)',sw.text)[0].replace(r'}},',r'}}}')
	jsParse = json.loads(script)

	API_KEY = jsParse["INNERTUBE_API_KEY"]

	return API_KEY
def logError(message):
	logging.error(message)
	sys.exit(1)
def parseCookieFile(cookiefile):
	"""Parse a cookies.txt file and return a dictionary of key value pairs
	compatible with requests."""

	cookies = {}
	try:
	    with open (cookiefile, 'r') as fp:
	        for line in fp:
	            if not re.match(r'^\#', line):
	                lineFields = line.strip().split('\t')
	                try:
	                	cookies[lineFields[5]] = lineFields[6]
	                except:
	               		continue
	except FileNotFoundError:
		logError('cookie file is not found, make sure that it\'s extracting using "get cookies.txt" and it\'s named "youtube.com_cookies.txt"')
	except Exception as e:
		logError(e)	

	return cookies
def getCookies():
	cookies = parseCookieFile("youtube.com_cookies.txt")
	return cookies

def getCont():
	req = requests.get('https://www.youtube.com/feed/history',cookies=cookies)
	cont = re.findall(r'continuationCommand":{"token":"(.+?)"',req.text)[0]

	if not cont:
		logError('make sure to export the cookies using get cookies.txt (a chrome extension)')

	return cont

def getData(auth, cont):

	headers = {"origin":"https://www.youtube.com","authorization":f"{auth}"}

	data = {"context":{"client":{"clientName":"ANDROID","clientVersion":"16.05"}},"continuation":cont if cont else getCont()}

	req = requests.post('https://www.youtube.com/youtubei/v1/browse?key='+API_KEY, headers=headers ,json=data, cookies=cookies)
	data = json.loads(req.text)

	return data

def main():
	parser = argparse.ArgumentParser(description='scrap full youtube history')
	parser.add_argument('-a','--auth', help='auth token, you can get it from here https://i.imgur.com/xf8gqgl.png in https://www.youtube.com/feed/history, if you can\'t find it scroll to the end of the page and try again')
	parser.add_argument('-o','--output', help='output file, default "./output.txt"')
	parser.add_argument('-v','--debug', help='debugging', action='store_true')
	args = parser.parse_args()

	if args.debug:
		logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

	global API_KEY,cookies
	API_KEY = getAPIKey()
	cookies = getCookies()

	#print(getCont())
	
	auth = args.auth

	History = history(getData(auth, None))
	logging.debug(History.getMainPageCont())

	History = history(getData(auth, History.getMainPageCont()))
	page = 1
	data = {}

	while History.getNextCont():
		print(f'Page Number: {page}', end='\r')
		logging.debug(f'ContinuationID: {History.getNextCont()}')
		data[page] = []
		HistoryVideos = History.getListVideos()
		logging.debug(HistoryVideos)
		data[page].append(HistoryVideos)

		History = history(getData(auth, History.getNextCont()))
		page += 1
			

	if args.output:
		print(f'output set to: ./{args.output}')
		with open(args.output, 'w', encoding='utf-8') as f:
			f.write(json.dumps(data, indent=4))
	else:
		print(f'output set to: ./output.txt')
		with open('output.txt', 'w', encoding='utf-8') as f:
			f.write(json.dumps(data, indent=4))

if __name__ == '__main__':
	main()	
