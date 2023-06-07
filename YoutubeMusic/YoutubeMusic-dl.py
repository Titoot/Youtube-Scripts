import eyed3
import logging
from eyed3.id3.frames import ImageFrame
from clint.textui import progress
from urllib import request
from termcolor import colored
from pydub import AudioSegment
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
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
	req = session.get(url, headers=headers)
	data = re.findall(r'videoId\\x22:\\x22(.{11})\\x22\\x7d,\\x22multi', req.text)
	return data

def getAPIKey():
	sw = session.get('https://music.youtube.com/sw.js')

	script = re.findall(r'ytcfg\.set\(({.+?}},)',sw.text)[0].replace(r'}},',r'}}}')
	jsParse = json.loads(script)

	API_KEY = jsParse["INNERTUBE_API_KEY"]
	return API_KEY

def getData(id):
	headersNew = headers
	headersNew["user-agent"] = "com.google.android.youtube/18.16.34"
	data = {"context":{"client":{"clientName":"ANDROID","clientVersion":"18.16.34", "androidSdkVersion":33}},"videoId":f"{id}"}

	music = session.post(f'https://music.youtube.com/youtubei/v1/player?key={API_KEY}', headers=headersNew, json=data)

	musicData = json.loads(music.text)
	return musicData

def getDataMeta(id):
	data = {"context":{"client":{"clientName":"WEB_REMIX","clientVersion":"1.20230104.01.00"}},"videoId":f"{id}"}

	music = session.post(f'https://music.youtube.com/youtubei/v1/player?key={API_KEY}', headers=headers, json=data)

	musicData = json.loads(music.text)
	return musicData	
	
def logError(message):
	logging.error(message)
	sys.exit(1)
def getUrl(data):
	try:
		mainData = data["streamingData"]["adaptiveFormats"]
	except KeyError:
		logError(data)

	for i in range(len(mainData)):

		try:
			mainData[i]["audioQuality"]
		except KeyError:
			continue

		if mainData[i]["audioQuality"] == "AUDIO_QUALITY_MEDIUM":

			return mainData[i]["url"]

def addmetadata(name,imagefile, author, title):
	audiofile = eyed3.load(f"{name}.mp3")
	if (audiofile.tag == None):
		audiofile.initTag()

	audiofile.tag.title = title
	audiofile.tag.artist = author
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
	name = os.path.join(path,legalize(f"{title}"))
	if os.path.exists(f'{name}.mp3'):
		print('file already exists')
		return
	print(f'Downloading "{title}" now')
	audio = session.get(url, headers=headers,stream=True)
	total_length = int(audio.headers.get('content-length'))
	with open(f"{name}.m4a", "wb") as f:

		if total_length is None:
			f.write(audio.content)
		else:
			for chunk in progress.bar(audio.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
				if chunk:
					f.write(chunk)
					f.flush()
	tomp3(name)
	cover = session.get(thumbnail)
	with open('cover.jpg', 'wb') as f:
		f.write(cover.content)

	addmetadata(name,'cover.jpg', author, title)

def colorful(title,author,data,thumbnail,args):
	string = f"{colored('Title:', 'yellow')} {title}\n{colored('Author:', 'yellow')} {author}\n"
	if args.debug:
		string += f"{colored('Link:', 'blue')} {data}\n{colored('Thumbnail:', 'red')} {thumbnail}\n"
	return string

def setupRequests():
	global session
	session = requests.Session()
	retry = Retry(connect=3, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	session.mount('http://', adapter)
	session.mount('https://', adapter)

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

	setupRequests()

	global API_KEY
	API_KEY = getAPIKey()

	if args.url:
		videoId = getID(args.url)
		musicData = getData(videoId)
		url = getUrl(musicData)
		MetaData = metadata(getDataMeta(videoId))

		print(colorful(MetaData.title(),MetaData.author(),url,MetaData.thumbnail(),args))

		if args.download and args.outputFolder is not None:
				download(url,MetaData.title(),MetaData.author(),MetaData.thumbnail(),args.outputFolder)
		elif args.download:
				download(url,MetaData.title(),MetaData.author(),MetaData.thumbnail())

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