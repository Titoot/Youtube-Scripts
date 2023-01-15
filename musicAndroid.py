import eyed3
from eyed3.id3.frames import ImageFrame
from urllib.parse import unquote,quote
from urllib import request
from termcolor import colored
from pydub import AudioSegment
import decoder
import requests
import argparse
import json
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
	
	API_KEY = getAPIKey()

	data = {"context":{"client":{"clientName":"ANDROID","clientVersion":"16.05"}},"videoId":f"{id}"}

	music = requests.post(f'https://music.youtube.com/youtubei/v1/player?key={API_KEY}', headers=headers, json=data)

	musicData = json.loads(music.text)
	return musicData

def getDataMeta(id):
	
	API_KEY = getAPIKey()

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

def tomp3(name):
	# open the m4a file
	m4a_audio = AudioSegment.from_file(f"{name}.m4a", format="m4a")

	# save the mp3 file
	m4a_audio.export(f"{name}.mp3", format="mp3")
	os.remove(f"{name}.m4a")

def download(url,title,author,thumbnail):
	headers = {"range":"bytes=0-"}
	name = f"Downloads\\{title} - {author}"
	audio = requests.get(url, headers=headers,stream=True)
	with open(f"{name}.m4a", "wb") as f:
		f.write(audio.content)

	tomp3(name)

	cover = request.urlretrieve(thumbnail, 'cover.jpg')
	addthumbnail(name,'cover.jpg')

def colorful(title,author,data,thumbnail):
	return f"{colored('Title:', 'yellow')} {title}\n{colored('Author:', 'yellow')} {author}\n{colored('Link:', 'blue')} {data}\n{colored('Thumbnail:', 'red')} {thumbnail}\n"

def main():
	parser = argparse.ArgumentParser(description='get a direct link from a youtube video')
	parser.add_argument('-u','--url', help='one url')
	parser.add_argument('-p','--playlist', help='get playlist')
	parser.add_argument('-d','--download', help='download it', action='store_true')
	parser.add_argument('-i','--input', help='input file with urls')
	parser.add_argument('-o','--output', help='output file, default "./output.txt"')
	args = parser.parse_args()

	if args.url:
		videoId = getID(args.url)
		musicData = getData(videoId)
		MetaData = metadata(musicData)

		print(colorful(MetaData.title(),MetaData.author(),musicData,MetaData.thumbnail()))

	elif args.playlist:
		playlist = getPlaylistIds(args.playlist)
		for i in playlist:
			musicData = getData(i)
			MetaData = metadata(getDataMeta(i))
			#print(getUrl(musicData))
			url = getUrl(musicData)
			print(colorful(MetaData.title(),MetaData.author(),url,MetaData.thumbnail()))

			if args.download:
				download(url,MetaData.title(),MetaData.author(),MetaData.thumbnail())

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