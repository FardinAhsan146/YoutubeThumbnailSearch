import sqlite3
from sqlite3 import Connection
from typing import Optional

from .video_content import VideoContent

def thumbnail_url(video_id: str) -> str:
    return f"https://i1.ytimg.com/vi/{video_id}/maxresdefault.jpg"

def create_connection(db_name: str = 'talk_to_youtuber_db.sqlite') -> Optional[Connection]:
    """Create a database connection to the SQLite database specified by db_name."""
    conn: Optional[Connection] = None
    try:
        conn = sqlite3.connect(db_name)
        print(f"Connected to database '{db_name}'")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn: Connection) -> None:
    """Create a table named video_contents with four string fields."""
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS video_contents (
        channel_name TEXT NOT NULL,
        video_id TEXT NOT NULL,
        video_title TEXT,
        thumbnail_url TEXT 
    );
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        print("Table 'video_contents' created.")
    except sqlite3.Error as e:
        print(e)

def delete_table(conn: Connection) -> None:
    """Delete the video_contents table if it exists."""
    delete_table_sql = 'DROP TABLE IF EXISTS video_contents;'
    try:
        cursor = conn.cursor()
        cursor.execute(delete_table_sql)
        conn.commit()
        print("Table 'video_contents' deleted.")
    except sqlite3.Error as e:
        print(e)

def insert_initial_row(conn: Connection, channel_name: str, video_id: str, video_title: str) -> None:
    """Insert a new row into the video_contents table with channel_name, video_id, video_title, and thumbnail_url only if the video_id doesn't already exist."""
    check_sql = '''
    SELECT 1 FROM video_contents WHERE video_id = ? LIMIT 1;
    '''
    insert_sql = '''
    INSERT INTO video_contents (channel_name, video_id, video_title, thumbnail_url)
    VALUES (?, ?, ?, ?);
    '''
    try:
        cursor = conn.cursor()
        
        # Check if the video_id already exists
        cursor.execute(check_sql, (video_id,))
        exists = cursor.fetchone()
        
        if exists:
            pass
        else:
            # Generate the thumbnail URL
            thumb_url = thumbnail_url(video_id)
            
            # Proceed with insertion
            cursor.execute(insert_sql, (channel_name, video_id, video_title, thumb_url))
            conn.commit()
    except sqlite3.Error as e:
        print(e)

def get_videos_by_channel(conn: Connection, channel_name: str) -> Optional[list[VideoContent]]:
    """Get all video content for a given channel name."""
    select_sql = '''
    SELECT * FROM video_contents WHERE channel_name = ?;
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(select_sql, (channel_name,))
        rows = cursor.fetchall()
        rows = [VideoContent(*row) for row in rows]

        if rows:
            return rows
        else:
            print(f"No videos found for channel '{channel_name}'.")
            return None
    except sqlite3.Error as e:
        print(e)
        return None
    
def video_exists(conn: Connection, video_id: str) -> bool:
    """Check if a video with the given video_id exists in the video_contents table."""
    check_sql = '''
    SELECT 1 FROM video_contents WHERE video_id = ? LIMIT 1;
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(check_sql, (video_id,))
        result = cursor.fetchone()
        return result is not None
    except sqlite3.Error as e:
        print(f"Error checking video existence: {e}")
        return False

if __name__ == '__main__':
    # db_name: str = 'talk_to_youtuber_db.sqlite'

    # # Create a database connection
    # conn: Optional[Connection] = create_connection(db_name = db_name )

    # if conn:
    #     #Create the video_contents table
    #     create_table(conn)

    #     # Insert a test row
    #     insert_initial_row(conn, 'MyChannel', '12345', 'This is a test title.')

    #     # Update video transcript
    #     update_video_transcript(conn, '12345', 'This is a test transcript.')

    #     # Delete the video_contents table
    #     delete_table(conn)

    #     # Close the database connection
    #     conn.close()
    pass 

