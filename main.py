import os
import sys
import time 
import torch
import clip
import chromadb
from tqdm import tqdm
import random 
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional

from image_utils.image_from_url import get_image_from_url
from youtube_utils import get_video_ids
from database import database_utils

# Ensure CUDA is available, otherwise use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

# Load CLIP model
model, preprocess = clip.load("ViT-B/32", device=device)

# Initialize Chroma client
client = chromadb.PersistentClient(path="chroma_clip_embeddings/")
collection = client.get_or_create_collection(name="youtube_thumbnail_embeddings",  metadata={"hnsw:space": "cosine"})


def print_video_info(video_data: Dict[str, Any]) -> None:
    """
    Print out video title and URL to CLI with PowerShell-compatible hyperlinks.

    Args:
        video_data (Dict[str, Any]): Dictionary containing video data.
    """
    base_url = "https://www.youtube.com/watch?v="
    
    for i, data in enumerate(zip(video_data['ids'][0], video_data['metadatas'][0])):
        id, metadata = data 
        url = f"{base_url}{id}"
        print(f"-------- Video {i}")
        print(f"Video Title: {metadata['video_title']}")
        print(f"Video Url: {url}")
        # PowerShell-compatible hyperlink
        print("-------- \n")

def process_video(video: Any) -> Optional[Dict[str, Any]]:
    """
    Retrieve thumbnail from url and embded it. 

    Args:
        video (Any): Video object containing video information.

    Returns:
        Optional[Dict[str, Any]]: Dictionary containing processed video data, or None if processing fails.
    """
    url = f"https://img.youtube.com/vi/{video.video_id}/hqdefault.jpg"
    
    try:
        thumbnail = get_image_from_url(url)
        
        # Embed the thumbnail
        image = preprocess(thumbnail).unsqueeze(0).to(device)
        with torch.no_grad():
            image_features = model.encode_image(image)
        
        # Convert the embedding to a Python list
        embedding_list = image_features.cpu().tolist()[0]
        
        return {
            "id": video.video_id,
            "embedding": embedding_list,
            "metadata": {
                "channel_name": video.channel_name,
                "video_title": video.video_title
            }
        }
    except Exception as e:
        print(f"Error processing video {video.video_id}: {str(e)}")
        return None

def add_to_collection(result: Optional[Dict[str, Any]]) -> None:
    """
    Add the thumbnail embedding to the vector db 

    Args:
        result (Optional[Dict[str, Any]]): Processed video data to add to the collection.
    """
    if result:
        collection.add(
            ids=[result["id"]],
            embeddings=[result["embedding"]],
            metadatas=[result["metadata"]]
        )

def process_and_add(video: Any) -> None:
    """
    Wrapper for the process_video and add_to_collection functions for multi threading 

    Args:
        video (Any): Video object to process and add.
    """
    result = process_video(video)
    if result:
        add_to_collection(result)
    # random jitters for rate limit 
    time.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process YouTube videos and search for similar thumbnails")
    parser.add_argument("-youtuber", type=str, help="Name of the YouTuber")
    parser.add_argument("-search_query", type=str, help="Search query for similar thumbnails")
    parser.add_argument("-n_results", type=int, help="Number of search queries to return")
    parser.add_argument("--refetch", action="store_true", help="Refetch and reprocess all data")
    args = parser.parse_args()

    youtuber = args.youtuber

    # Make the SQLITE table connection 
    conn = database_utils.create_connection(db_name = './database/youtuber_db.sqlite')

    if args.refetch:
        # create the videos table 
        database_utils.create_table(conn)

        # Start downloading the video ids
        get_video_ids.get_videos(youtuber, conn)

    # Get all the videos 
    all_videos = database_utils.get_videos_by_channel(conn, youtuber)

    # Process videos using multiple threads
    if args.refetch:
        with ThreadPoolExecutor(max_workers=40) as executor:
            list(tqdm(executor.map(process_and_add, all_videos), total=len(all_videos), desc="Processing videos"))

    # Get the search query from command line arguments
    search_query = args.search_query

    # embed the users query 
    text = clip.tokenize([search_query]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text)

    # Convert the embedding to a Python list
    text_features_list = text_features.cpu().tolist()[0]

    # query results 
    results = collection.query(
        query_embeddings=[text_features_list],
        n_results=args.n_results,
        where={"channel_name": youtuber},
        include=["metadatas"]
    )

    print_video_info(results)