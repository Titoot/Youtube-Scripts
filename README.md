## Table of Contents
- [Youtube](#youtube)
  * [Direct link](#direct-link)
  * [Get Full History](#get-full-history)
- [Youtube Music](#youtube-music)
  * [youtubemusic-dl](#youtubemusic-dl)


# youtube
## direct-link
### Usage
```bash
git clone https://github.com/Titoot/Youtube-Scripts.git
cd Youtube-Scripts/Youtube
python -m pip install -r requirements.txt
python youtube.py
```
### help menu
```
python youtube.py -h
```
```
usage: youtube.py [-h] [-u URL] [-i INPUT] [-o OUTPUT]

get a direct link from a youtube video

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     one url
  -i INPUT, --input INPUT input file with urls
  -o OUTPUT, --output OUTPUT output file, default "./output.txt"
```

### Example:
```
python youtube.py -u https://youtu.be/XXXXXXXXXXX
https://rr4---XXXXXX.googlevideo.com/videoplayback?XXXXXXX
```
### note
This code is set default for 720p, you can choose 360p by changing the index from 1 to 0 here:
https://github.com/Titoot/Youtube-Scripts/blob/8ad8bb478c1c817e286f0520b71337b28e806e0f/youtube.py#L26

## get-full-history
### Usage
```bash
git clone https://github.com/Titoot/Youtube-Scripts.git
cd Youtube-Scripts/Youtube/History
python -m pip install -r requirements.txt
python GetFullHistory.py
```
make sure to add the cookies file and get the auth from youtube [history page](https://youtube.com/feed/history), the cookies can be extracted by using [get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid?hl=en)
### help menu
```bash
python GetFullHistory.py -h
```
```
usage: GetFullHistory.py [-h] [-a AUTH] [-o OUTPUT] [-v]

scrap full youtube history

optional arguments:
  -h, --help            show this help message and exit
  -a AUTH, --auth AUTH  auth token, you can get it from here https://i.imgur.com/xf8gqgl.png in
                        https://www.youtube.com/feed/history, if you can't find it scroll to the end of the page and
                        try again
  -o OUTPUT, --output OUTPUT
                        output file, default "./output.txt"
  -v, --debug           debugging
```
### Example:
```bash
python GetFullHistory.py -a $auth -l 5
```
```json
...
{
"1": [
            "Sep 8, 2022": [
                {
                    "ID": "PpxGfaG8WRQ",
                    "Title": "How to Spd Firmware Unpack & Repack",
                    "Channel": "FIRMWARE 94"
                }
            ],
            "Sep 7, 2022": [
                {
                    "ID": "7J4iL1HDshQ",
                    "Title": "Next.js Tutorial - Part 1 | Router for Beginners",
                    "Channel": "Bruno Antunes"
                },
                {
                    "ID": "FMnlyi60avU",
                    "Title": "Prisma - The Easiest Way to Work with a Database in Next.js (UPDATED)",
                    "Channel": "Prisma"
                },
                {
                    "ID": "lF8DV_ICIpY",
                    "Title": "Prisma - The Easiest Way to Work with a Database in Next.js",
                    "Channel": "Prisma"
                }
            ],
            "Sep 6, 2022": [
                {
                    "ID": "FMnlyi60avU",
                    "Title": "Prisma - The Easiest Way to Work with a Database in Next.js (UPDATED)",
                    "Channel": "Prisma"
                },
                {
                    "ID": "wqHGLjuXuHo",
                    "Title": "Next.js Tutorial - 43 - API POST Request",
                    "Channel": "Codevolution"
                },
                {
                    "ID": "Fq6-_mF2jMw",
                    "Title": "How to Install PostGreSQL and pgAdmin in Windows 10 8 7",
                    "Channel": "StudyGyaan"
                }
                ...
```

# youtube-music
## youtubemusic-dl
### why?
first it was fun, and i didn't like the way [yt-dlp](https://github.com/yt-dlp/yt-dlp) worked and it has issues with thumbnails and metadata so i fixed it in this script.
### Usage
```bash
git clone https://github.com/Titoot/Youtube-Scripts.git
cd Youtube-Scripts/YoutubeMusic
python -m pip install -r requirements.txt
python YoutubeMusic-dl.py
```
### help menu
```bash
python YoutubeMusic-dl.py -h
```
```
usage: YoutubeMusic-dl.py [-h] [-u URL] [-p PLAYLIST] [-d] [-o OUTPUT]

download music from youtube music

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     one url
  -p PLAYLIST, --playlist PLAYLIST get playlist
  -d, --download        download it
```
### Example:
```
python .\YoutubeMusic-dl.py -u https://music.youtube.com/watch?v=H4buRu9-Wb4 -d
Title: Another Love
Author: Tom Odell
Link: https://rr2---sn-bpb5oxu-3c26.googlevideo.com/videoplayback?expire=1673893474&ei=AkLFY4zjEYuu1wK2wZfwBw&ip=2a09%3Abac1%3A2200%3A10%3A%3A40%3A32&id=o-AKnN7VCqexlXb5PYMu3-bUTZouXTmi-4R6-j1C88YC0r&itag=140&source=youtube&requiressl=yes&mh=x-&mm=31%2C29&mn=sn-bpb5oxu-3c26%2Csn-hgn7yn7z&ms=au%2Crdu&mv=m&mvi=2&pl=64&gcr=eg&initcwndbps=951250&vprv=1&mime=audio%2Fmp4&gir=yes&clen=3957464&dur=244.359&lmt=1620810742211906&mt=1673871450&fvip=5&keepalive=yes&fexp=24007246&c=ANDROID&txp=5531432&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cgcr%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRgIhALK_f8GgFQW6glOQ3VpCFPM0K9JM-9A2iKhsO8HjTgoeAiEA3IOH-D313SZ_it7xtaoZYpbPFSsUOS4s7Y-IEKDLlm8%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhAOUdGlsQDmJyMvR7XmAY3N3uJ5nEapDwNYN2A9tdv2HpAiAnhcI0YBPzb-wOKb_o9VaeHyvrrRA65ERVVpIOiSZASQ%3D%3D
Thumbnail: https://lh3.googleusercontent.com/7a0LqOeMSeQjIfUPSfvWkk1Ew1CKrjYzpWte6FcQwx-uOUERJSmhnjsUlyerYX1BN2PJlX_0OP3kSHMz=w544-h544-l90-rj

Downloading "Another Love" now
Done Downloading
```
