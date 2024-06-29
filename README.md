# YoutubeThumbnailSearch

YoutubeThumbnailSearch is a handy tool designed to help you search through YouTube channel thumbnails using text queries. Powered by the [OpenAI CLIP](https://openai.com/index/clip/) model, it makes searching thumbnails easy and effective, especially for journalists or researchers workign with large amounts of media content.

The gif below shows how I searched a Serbian news channel 'belamiportalofficial' with over 30,000 videos for those related to horses, just by their thumbnails.

![gif](https://github.com/FardinAhsan146/YoutubeThumbnailSearch/blob/master/docs/show.gif)

In the example above, I used the command `python main.py -youtuber belamiportalofficial -search_query horse -n_results 5` to find videos from 'belamiportalofficial' that have horses in the thumbnails.

**Note:** The first-time search might take longer since the tool needs to download video titles and embed thumbnails. On average, it processes around 1,000 videos per minute due to YouTube's rate limits on requests.

## What This Tool Solves

1. **Search Specific Channels:** Easily search for videos from a specific YouTube channel.
2. **Overcome Language/Title Issues:** Perfect when you can't remember the video title or it’s in a non-English language.
3. **When Transcripts Are Unavailable:** Useful even if the video transcript isn’t available or remembered.
4. **Rely on Visual Memory:** Great for situations where you only remember what the video's thumbnail looks like.
5. **Handle Large Volumes:** Much better than manually scrolling through channels with hundreds or thousands of videos.
6. **Boost Efficiency:** Lets you search through video thumbnails using text queries, saving time and effort.

## Features

1. **Download Video IDs:** Fetches all video IDs for a channel and constructs video and thumbnail URLs.
2. **Embed Thumbnails:** Uses the OpenAI CLIP model to embed thumbnails and stores the results in a vector database.
3. **Search Thumbnails with Text:** Allows you to search video thumbnails using text queries.
4. **Persistent Database:** Stores results and embeddings in a vector database for faster future searches.

## Technical Notes

- The code is optimized for personal use, so it may need refactoring for broader applications.
- Utilizes the `ViT-B/32` version of CLIP, which works great and is manageable in size (300MB) for operations on an RTX 3080 GPU.
- The initial image URL fetching might be slow (~1 minute per 1,000 videos) due to YouTube's rate limits but still saves time compared to manual scrolling.
- Subsequent searches are faster because the tool stores embeddings in a persistent vector database.

## Installation

To use YoutubeThumbnailSearch, ensure you have a CUDA-enabled GPU and PyTorch installed. Then, install the required dependencies using:

```bash
pip install -r requirements.txt
```

## How to Run

To search for videos from a specific YouTube channel based on thumbnail content, run:

```bash
python main.py -youtuber <Name of Youtuber> -search_query <Search Query> -n_results <Number of Results to Fetch>
```

*Feel free to fetch large volumes of results; ChromaDB can handle it. The result limit is primarily for user convenience.*

---

Use this project to quickly search through large video collections, leveraging image-text embeddings to make your research work quick and effective.
