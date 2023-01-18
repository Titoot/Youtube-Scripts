import eyed3
import logging
from eyed3.id3.frames import ImageFrame
from urllib import request
from termcolor import colored
from pydub import AudioSegment
import requests
import argparse
import json
import sys
import re
import os
headers = {"origin":"https://music.youtube.com", "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
class metadata:
	def __init__(self, Data):  
		self.data = Data

	def thumbnail(self):
		return self.data["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]

	def title(self):
		return self.data["videoDetails"]["title"]
	def author(self):
		return self.data["videoDetails"]["author"]

def getID(url):
	patterns = [r'.*\?v=(.{11})', r'\.be\/(.{11})']
	for i in patterns:
		id = re.search(i, url)
		if id:
			return id[1]

def getPlaylistIds(url):
	req = requests.get(url, headers=headers)
	data = re.findall(r'videoId\\x22:\\x22(.{11})\\x22\\x7d,\\x22multi', req.text)
	return data

def getAPIKey():
	sw = requests.get('https://music.youtube.com/sw.js')

	script = re.findall(r'ytcfg\.set\(({.+?}},)',sw.text)[0].replace(r'}},',r'}}}')
	jsParse = json.loads(script)

	API_KEY = jsParse["INNERTUBE_API_KEY"]
	return API_KEY

def getData(id):

	data = {"context":{"client":{"clientName":"ANDROID","clientVersion":"16.05"}},"videoId":f"{id}"}

	music = requests.post(f'https://music.youtube.com/youtubei/v1/player?key={API_KEY}', headers=headers, json=data)

	musicData = json.loads(music.text)
	return musicData

def getDataMeta(id):
	
	data = {"context":{"client":{"clientName":"WEB_REMIX","clientVersion":"1.20230104.01.00"}},"videoId":f"{id}"}

	music = requests.post(f'https://music.youtube.com/youtubei/v1/player?key={API_KEY}', headers=headers, json=data)

	musicData = json.loads(music.text)
	return musicData	
	

def getUrl(data):

	mainData = data["streamingData"]["adaptiveFormats"]

	for i in range(len(mainData)):

		try:
			mainData[i]["audioQuality"]
		except KeyError:
			continue

		if mainData[i]["audioQuality"] == "AUDIO_QUALITY_MEDIUM":

			return mainData[i]["url"]

def addthumbnail(name,imagefile):
	audiofile = eyed3.load(f"{name}.mp3")
	if (audiofile.tag == None):
		audiofile.initTag()

	audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(imagefile,'rb').read(), 'image/jpeg')

	audiofile.tag.save()
	os.remove('cover.jpg')
	
def legalize(string):
	return re.sub(r'[/*?:"<>|]',"",string)

def tomp3(name):
	# open the m4a file
	m4a_audio = AudioSegment.from_file(f"{name}.m4a", format="m4a")

	# save the mp3 file
	m4a_audio.export(f"{name}.mp3", format="mp3")
	os.remove(f"{name}.m4a")

def download(url,title,author,thumbnail, path="Downloads"):
	headers = {"range":"bytes=0-"}
	name = os.path.join("Downloads",legalize(f"{title} - {author}"))
	if os.path.exists(f'{name}.mp3'):
		print('file already exists')
		return
	print(f'Downloading "{title}" now')
	audio = requests.get(url, headers=headers,stream=True)
	with open(f"{name}.m4a", "wb") as f:
		f.write(audio.content)

	tomp3(name)

	cover = request.urlretrieve(thumbnail, 'cover.jpg')
	addthumbnail(name,'cover.jpg')

def colorful(title,author,data,thumbnail,args):
	string = f"{colored('Title:', 'yellow')} {title}\n{colored('Author:', 'yellow')} {author}\n"
	if args.debug:
		string += f"{colored('Link:', 'blue')} {data}\n{colored('Thumbnail:', 'red')} {thumbnail}\n"
	return string

def main():
	parser = argparse.ArgumentParser(description='download music from youtube music')
	parser.add_argument('-u','--url', help='one url')
	parser.add_argument('-p','--playlist', help='get playlist')
	parser.add_argument('-d','--download', help='download it', action='store_true')
	parser.add_argument('-D','--outputFolder', help='specify output folder')
	parser.add_argument('-v','--debug', help='debugging', action='store_true')

	args = parser.parse_args()
	if not (args.url or args.playlist):
		parser.error('No action requested, add --url or --playlist')
	if args.debug:
		logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

	global API_KEY
	API_KEY = getAPIKey()

	if args.url:
		videoId = getID(args.url)
		musicData = getData(videoId)
		url = getUrl(musicData)
		MetaData = metadata(getDataMeta(videoId))

		print(colorful(MetaData.title(),MetaData.author(),url,MetaData.thumbnail(),args))

		if args.download:
				download(url,MetaData.title(),MetaData.author(),MetaData.thumbnail(),args.outputFolder)

	elif args.playlist:
		playlist = getPlaylistIds(args.playlist)
		for i in playlist:
			musicData = getData(i)
			MetaData = metadata(getDataMeta(i))
			url = getUrl(musicData)

			print(colorful(MetaData.title(),MetaData.author(),url,MetaData.thumbnail(),args))

			if args.download:
				download(url,MetaData.title(),MetaData.author(),MetaData.thumbnail(),args.outputFolder)

	if not args.outputFolder:
		print('Done Downloading at ./Downloads')
	else:
		print(f'Done Downloading at ./{args.outputFolder}')

if __name__ == '__main__':
	main()