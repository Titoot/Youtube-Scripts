import requests
import argparse
import json
import re

def getID(url):
	patterns = [r'.*\?v=(.{11})', r'\.be\/(.{11})', r'embed\/(.{11})']
	for i in patterns:
		id = re.search(i, url)
		if id:
			return id[1]

def getUrl(id):
	sw = requests.get('https://www.youtube.com/sw.js')

	script = re.findall(r'ytcfg\.set\(({.+?}},)',sw.text)[0].replace(r'}},',r'}}}')
	jsParse = json.loads(script)

	API_KEY = jsParse["INNERTUBE_API_KEY"]

	data = {"context":{"client":{"hl":"en","gl":"EG","clientName":"WEB","clientVersion":"2.20221021.00.00"}},"videoId":f"{id}"}

	video = requests.post('https://www.youtube.com/youtubei/v1/player?key='+API_KEY, json=data)
	videoData = json.loads(video.text)
	#720p quality id:22
	Q720p = videoData["streamingData"]["formats"][1]["url"]

	return Q720p


def main():
	parser = argparse.ArgumentParser(description='get a direct link from a youtube video')
	parser.add_argument('-u','--url', help='one url')
	parser.add_argument('-i','--input', help='input file with urls')
	parser.add_argument('-o','--output', help='output file, default "./output.txt"')
	args = parser.parse_args()

	if args.url:
		videoId = getID(args.url)
		print(getUrl(videoId))
		
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
