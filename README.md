# YoutubeThumbnailSearch

This is basically a glorified image search engine. 

![gif](https://github.com/FardinAhsan146/YoutubeThumbnailSearch/blob/master/docs/show.gif)

In the gif above I ran ` python main.py -youtuber belamiportalofficial -search_query horse -n_results 5` 

Basically searched  Serbian news channel 'belamiportalofficial' (>30k videos), for videos with horses in their thumbnails. This can be a useful tool for journalists to search through massive amounts of foreign media. 

## This is the problem this tool solves for me 
1. I want to search for a youtube video from a specific channel. 
2. I forgot the title or anything even resembling it, or the title isn't in English and I have not a chance of ever finding it.
3. I don't remmember the transcripts either. So my glorfied [youtube transcript search engine](https://github.com/FardinAhsan146/TalkToYoutuber) won't work either.
4. But I do remmember what the videos thumbnail looks like..
5. The channel has 100s if not 1000s of videos, so manually scrolling through is tedious. 
6. Why not just search the text-image embedding pairs of all the videos thumbnails? BOOM.
7. It doesn't even matter if the search or loadup is slow. It is still going to be miles faster than literally going through the youtube channel manually, which seems to be the only other alternative as opposed to cooking up some unholy yandex search query. 

## How it works. 
1. Download all the videos ids for a channel. You can construct the video url and thumbnail url from this. 
2. Embded all the thumbnails using OpenAI's CLIP, and store the result in a vector db. 
3. Done. You can now search through the video thumbnails using text search queries. 

## Comments 
* Code quality is goofy because its a tool I made mostly for personal use. Will refactor and improve if required.
* I'm using the `ViT-B/32` version CLIP, and albeit being one of the smaller models, it works excellently. It's a 300MB model so I can load it entirely into my RTX 3080 and do a gazillion operations on it. 
* The initial image url fetch is slow. Around 1 minute per 1000 videos. But youtubes rate limits are not that generous, and this is still a massively time saving tool as opposed to doing this task manually. 
* It won't be slow the second time around because I store the results and embeddings in a vector database. 

## Installation
* You will need pytorch and a Cuda GPU. Otherwise this project won't be feasible to run. 
* `pip install -r requirements.txt`

## How to run
* `python main.py --youtuber <Name of youtuber> --search_query <What you want the thumbnails to contain>`
