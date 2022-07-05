from distutils.log import error
import subprocess
from urllib.parse import parse_qs, urlparse


def yt_downloader(url):
    print(url)
    result = subprocess.Popen(['yt-dlp', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   universal_newlines=True)
    output, errors = result.communicate()
    print("*******",output)
    print(errors)
    output_list = output.split("\n")
    print(output_list)
    song_name = output_list[3]
    if 'has already been downloaded' in song_name:
        file_name = song_name.replace('has already been downloaded','').replace('[download]','')
    else:
        file_name = song_name.replace('[download] Destination: ','')
    return file_name.strip()


def get_video_id(url):
    if url.startswith(('youtu', 'www')):
        url = 'http://' + url
        
    query = urlparse(url)
    
    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    else:
        raise ValueError