import subprocess
from urllib.parse import parse_qs, urlparse
from bot.cred import URL
from bot.models import UserHistory

def yt_downloader(url):
    print(url)
    already_downloaded = False
    result = subprocess.Popen(['yt-dlp', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   universal_newlines=True)   #yt-dlp is an open source command line tool
    output, errors = result.communicate()
    print("*******",output)
    print(errors)
    output_list = output.split("\n")
    print(output_list)
    song_name = output_list[3]
    if 'has already been downloaded' in song_name:
        already_downloaded = True
        file_name = song_name.replace('has already been downloaded','').replace('[download]','')
    else:
        file_name = song_name.replace('[download] Destination: ','')
    return (file_name.strip(), already_downloaded)

#sample https://www.youtube.com/watch?v=M9TzInCWVj0
# https://youtu.be/83uZTH5OHGM
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

def get_history(chat_id):
    video_history = UserHistory.objects.filter(user_id=chat_id).select_related('video')
    print(video_history)
    reply_text = "You have downloaded the following videos:\n"
    count = 1
    for i in video_history:
        download_link = '{}download/{}'.format(URL,i.video_id)
        reply_text += str(count)+ '. '+ "<a href='{}'>{}</a>\n".format(download_link,i.video.video_name)
        count += 1
    return reply_text


