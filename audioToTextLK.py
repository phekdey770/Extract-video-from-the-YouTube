from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from tabulate import tabulate
import re

def get_video_id(url):
    # Extract video ID from the YouTube URL
    video_id_match = re.search(r'[?&]v=([a-zA-Z0-9_-]+)', url)
    if video_id_match:
        return video_id_match.group(1)
    return None

def fetch_transcript(video_url):
    video_id = get_video_id(video_url)
    if not video_id:
        print("Invalid YouTube URL")
        return
    
    try:
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Prepare data for tabulation
        table_data = [(entry['start'], entry['start'] + entry['duration'], entry['text']) for entry in transcript]
        
        # Print the transcript in a tabular format
        headers = ["Start Time (s)", "End Time (s)", "Text"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Optionally, format the transcript to JSON
        formatter = JSONFormatter()
        formatted_transcript = formatter.format_transcript(transcript)
        
        # Save the transcript to a file (optional)
        with open(f'{video_id}_transcript.json', 'w') as file:
            file.write(formatted_transcript)
        
        print("Transcript saved as 'transcript.json'")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace with your YouTube video URL
video_url = 'https://www.youtube.com/watch?v=C8nbgwvZB0Y'
fetch_transcript(video_url)
