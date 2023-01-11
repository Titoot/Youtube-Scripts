from urllib.parse import unquote,quote
from termcolor import colored
import decoder
import requests
import argparse
import json
import re

def getID(url):
	patterns = [r'.*\?v=(.{11})', r'\.be\/(.{11})']
	for i in patterns:
		id = re.search(i, url)
		if id:
			return id[1]
def getData(id):
	sw = requests.get('https://music.youtube.com/sw.js')

	script = re.findall(r'ytcfg\.set\(({.+?}},)',sw.text)[0].replace(r'}},',r'}}}')
	jsParse = json.loads(script)

	API_KEY = jsParse["INNERTUBE_API_KEY"]

	headers = {"origin":"https://music.youtube.com"}

	data = {"context":{"client":{"clientName":"WEB_REMIX","clientVersion":"1.20230104.01.00"}},"videoId":f"{id}"}

	music = requests.post(f'https://music.youtube.com/youtubei/v1/player?key={API_KEY}', headers=headers, json=data)

	global musicData
	musicData = json.loads(music.text)

def getUrl(data):

	mainData = data["streamingData"]["adaptiveFormats"]

	for i in range(len(mainData)):

		try:
			mainData[i]["audioQuality"]
		except KeyError:
			continue	

		if mainData[i]["audioQuality"] == "AUDIO_QUALITY_MEDIUM":
            
			StrSplit = mainData[i]["signatureCipher"].split('&')
			sig = StrSplit[0].split('=')[1]
			url = StrSplit[2].split('=')[1]
			
			decodedSig = quote(decoder.cta(unquote(sig)))

			url = unquote(url)
			decodedUrl = f"{url}&sig={decodedSig}"
			return decodedUrl

class metadata:
	def __init__(self, Data):  
		self.data = Data

	def thumbnail(self):
		return self.data["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]

	def title(self):
		return self.data["videoDetails"]["title"]
	def author(self):
		return self.data["videoDetails"]["author"]	

def main():
	parser = argparse.ArgumentParser(description='get a direct link from a youtube video')
	parser.add_argument('-u','--url', help='one url')
	parser.add_argument('-i','--input', help='input file with urls')
	parser.add_argument('-o','--output', help='output file, default "./output.txt"')
	args = parser.parse_args()

	if args.url:
		videoId = getID(args.url)
		getData(videoId)
		MetaData = metadata(musicData)

		print(f"{colored('Title:', 'yellow')} {MetaData.title()}\n\
{colored('Author:', 'yellow')} {MetaData.author()}\n\
{colored('Link:', 'blue')}{getUrl(musicData)}\n\
{colored('Thumbnail:', 'red')} {MetaData.thumbnail()}")

	elif args.input:
		if not args.output:
			print('output set to default: ./output.txt')
			f = open('output.txt', 'w')

		else:
			print('output set to : '+ args.output)
			f = open(args.output, 'w')		

		with open(args.input, 'r') as f1:
			for i in f1.readlines():

				videoId = getID(i[:-1])

				f.write(getUrl(videoId) + '\n')
	else:
		videoId = getID(input('Url:'))
		print(getUrl(videoId))


if __name__ == '__main__':
	main()	
