# YoutubeThumbnailSearch

YoutubeThumbnailSearch is an advanced image search tool designed to help you search through YouTube channel thumbnails based on text queries. This tool uses the powerful OpenAI CLIP model to embed and search thumbnails, making it remarkably useful for journalists or researchers dealing with large volumes of media content.

The gif below demonstrates the process of searching a Serbian news channel 'belamiportalofficial' with over 30,000 videos for those related to horses based on their thumbnails.

![gif](https://github.com/FardinAhsan146/YoutubeThumbnailSearch/blob/master/docs/show.gif)

In the example above, I used the command `python main.py -youtuber belamiportalofficial -search_query horse -n_results 5` to search the channel 'belamiportalofficial' for videos with horses in the thumbnails.

**Note:** The first-time search may take longer because the tool needs to download video titles and embed thumbnails. On average, the tool processes around 1,000 videos per minute due to rate limits on requests sent to YouTube.

## Problem Solved by the Tool

1. **Search Specific Channels:** It helps you search for videos from a specific YouTube channel.
2. **Overcome Language/Title Issues:** It's ideal if you can't recall the video title or if it's in a non-English language.
3. **When Transcripts Are Unavailable:** It’s useful when the video transcript is unavailable or unremembered.
4. **Rely on Visual Memory:** Perfect for situations where you remember what the video's thumbnail looks like.
5. **Handle Large Volumes:** It’s extremely helpful for bypassing manual scrolling through channels with hundreds or thousands of videos.
6. **Boost Efficiency:** It allows searching through image embedding pairs of video thumbnails efficiently, significantly faster than manual searching.

## Features

1. **Download Video IDs:** The tool fetches all video IDs for a channel and constructs video and thumbnail URLs.
2. **Embed Thumbnails:** It uses the OpenAI CLIP model to embed thumbnails and stores the results in a vector database.
3. **Search Thumbnails with Text:** You can search video thumbnails using text queries.
4. **Persistent Database:** It stores results and embeddings in a vector database for faster subsequent searches.

## Technical Comments

- The code is optimized for personal use, so it may require refactoring for broader applications.
- It utilizes the smaller yet effective `ViT-B/32` version of CLIP, which works excellently with a manageable model size (300MB) for operations on an RTX 3080 GPU.
- The initial image URL fetching may be slow (~1 minute per 1,000 videos) due to YouTube rate limits but significantly saves time compared to manual scrolling.
- Subsequent searches are faster because the tool stores embeddings in a persistent vector database.

## Installation

To use YoutubeThumbnailSearch, ensure you have a CUDA-enabled GPU and PyTorch installed. Install the required dependencies using:

```bash
pip install -r requirements.txt
```

## How to Run

To search for videos from a specific YouTube channel based on thumbnail content, run:

```bash
python main.py -youtuber <Name of Youtuber> -search_query <Search Query> -n_results <Number of Results to Fetch>
```

*Fetch large volumes of results if needed; ChromaDB can handle it. The result limit is primarily for user convenience.*

---

Use this project to efficiently search through extensive video collections, leveraging state-of-the-art image-text embedding technology to meet your unique search requirements.