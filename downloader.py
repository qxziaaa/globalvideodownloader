import yt_dlp
import time
import sys
import threading
import json

print(r"""
  ____ _       _           _  __     ___     _            
 / ___| | ___ | |__   __ _| | \ \   / (_) __| | ___  ___  
| |  _| |/ _ \| '_ \ / _` | |  \ \ / /| |/ _` |/ _ \/ _ \ 
| |_| | | (_) | |_) | (_| | |   \ V / | | (_| |  __/ (_) |
 \____|_|\___/|_.__/ \__,_|_|    \_/  |_|\__,_|\___|\___/ 
|  _ \  _____      ___ __ | | ___   __ _  __| | ___ _ __  
| | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__| 
| |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |    
|____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|      
""")

# Load folder path from config
with open('config.json') as f:
    config = json.load(f)
folder_path = config['folder_path']

# yt-dlp options
ydl_opts = {
    'outtmpl': f'{folder_path}/%(title)s.%(ext)s',
    'format': 'bestvideo+bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'merge_output_format': 'mp4'
}

# Dot animation setup
dots = [" ", ". ", ".. ", "..."]
dot_index = 0
stop_animation = False

def loading_animation():
    global dot_index
    while not stop_animation:
        sys.stdout.write("\r" + "Downloading" + dots[dot_index])
        sys.stdout.flush()
        dot_index = (dot_index + 1) % len(dots)
        time.sleep(0.5)

def download_video(link):
    global stop_animation
    stop_animation = False
    website_name = link.split("/")[2]
    print(f'Found video on {website_name}')
    thread = threading.Thread(target=loading_animation)
    thread.start()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    stop_animation = True
    thread.join()
    print("\nDownload completed\n")

# ---------- Main loop ----------
while True:
    link = input("Enter any video link: ")
    download_video(link)
    again = input("Do you want to download another video? (y/n): ").lower()
    if again != 'y':
        print("Exiting downloader.")
        break
