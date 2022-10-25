### Usage
```bash
git clone https://github.com/Titoot/Youtube-DirectLink-Extractor.git
cd Youtube-DirectLink-Extractor
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
#### note
This code is set default for 720p, you can choose 360p by changing the index from 1 to 0 here:
https://github.com/Titoot/Youtube-DirectLink-Extractor/blob/8ad8bb478c1c817e286f0520b71337b28e806e0f/youtube.py#L26
