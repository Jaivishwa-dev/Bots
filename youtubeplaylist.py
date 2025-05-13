


# for download playlist videos
import os
from yt_dlp import YoutubeDL

def download_playlist(playlist_url, save_path=".", video_quality="1080p", file_format="mp4"):
    """
    Advanced YouTube Playlist Downloader.

    :param playlist_url: URL of the YouTube playlist to download.
    :param save_path: Directory to save the downloaded videos. Default is current directory.
    :param video_quality: Quality of the videos (e.g., '1080p', '720p', 'best', etc.).
    :param file_format: File format for the output (e.g., 'mp4', 'mkv').
    """
    try:
        # Configure options
        ydl_opts = {
            'format': f'bestvideo[height<={video_quality}][ext=mp4]+bestaudio/best',  # 1080p video + best audio
            'outtmpl': os.path.join(save_path, '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s'),  # Save file with playlist title and index
            'merge_output_format': file_format,  # Merge into desired file format
            'quiet': False,  # Show download progress
            'progress_hooks': [progress_hook],  # Attach progress hook
            'noplaylist': False,  # Allow playlist downloads
        }

        # Download playlist
        with YoutubeDL(ydl_opts) as ydl:
            print(f"Starting download for playlist: {playlist_url}")
            ydl.download([playlist_url])

    except Exception as e:
        print(f"Error: {e}")

def progress_hook(d):
    """
    Hook to display progress during download.

    :param d: Dictionary with progress data.
    """
    if d['status'] == 'downloading':
        print(f"Downloading: {d['_percent_str']} - {d['_eta_str']} remaining.")
    elif d['status'] == 'finished':
        print(f"Download complete! File saved to {d['filename']}")

if __name__ == "__main__":
    # Input from user
    playlist_url = input("Enter YouTube playlist URL: ").strip()
    save_path = input("Enter save directory (leave blank for current directory): ").strip() or "."
    video_quality = input("Enter video quality (default '1080p'): ").strip() or "1080p"
    file_format = input("Enter file format (default 'mp4'): ").strip() or "mp4"

    # Validate save directory
    if not os.path.exists(save_path):
        print(f"Creating directory: {save_path}")
        os.makedirs(save_path)

    # Download playlist
    download_playlist(playlist_url, save_path, video_quality, file_format)
