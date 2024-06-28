from dataclasses import dataclass

@dataclass
class VideoContent:
    channel_name: str
    video_id: str
    video_title: str
    thumbnail_url: str