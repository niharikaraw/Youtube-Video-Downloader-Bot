import json
import re
import traceback
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
import telegram
from bot.cred import *
from django.views.decorators.csrf import csrf_exempt
from emoji import emojize
from bot.models import FileInfo

from bot.utils import get_video_id, yt_downloader

# Create your views here.

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token= TOKEN)
"{'update_id': 425632664, 'message': {'message_id': 9, 'from': {'id': 5164975159, 'is_bot': False, 'first_name': 'N', 'last_name': 'R', 'language_code': 'en'}, 'chat': {'id': 5164975159, 'first_name': 'N', 'last_name': 'R', 'type': 'private'}, 'date': 1656956377, 'text': 'Hi'}}"
@csrf_exempt
def introduction(request):
    try:
        body = json.loads(request.body)
        print(body)
        chat_id = body.get('message').get('chat').get('id')
        print(chat_id)
        message = body.get('message').get('text')
        video_filename = None
        reply_to_message_id = body.get('message').get('message_id')
        return_reply = 'Welcome to Youtube Downloader Bot {} {}{}!\n Send me a valid youtube link and I will send you the video.'.format(body.get('message').get('from').get('first_name'),body.get('message').get('from').get('last_name'),emojize(':grinning_face:'))
        regex_youtube = 'http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?'
        if re.search(regex_youtube,message):
            url = message.strip()
            video_filename = yt_downloader(url)
    except Exception as e:
        print(traceback.format_exc())
        return_reply = 'Oops! Something went wrong{} Please provide a valid youtube link'.format(emojize(':slightly_frowning_face:'))

    try:
        if video_filename:
            video_id = get_video_id(url)
            file_name_obj = FileInfo(
                video_name = video_filename,
                video_id = video_id 
            )
            file_name_obj.save()
            try:
                bot.send_video(chat_id=chat_id, video=open(video_filename, 'rb'), supports_streaming=True)
            except:
                download_link = '{}download/{}'.format(URL,video_id)
                bot.send_message(chat_id=chat_id,text='Your download link is:\n{}'.format(download_link), parse_mode=telegram.ParseMode.MARKDOWN, reply_to_message_id=reply_to_message_id)
        else:
            bot.send_message(chat_id=chat_id, text=return_reply, parse_mode=telegram.ParseMode.MARKDOWN, reply_to_message_id=reply_to_message_id)
    except Exception as e :
        print (e)
        return_reply = "Oops! Something went wrong{} Please try again".format(emojize(':slightly_frowning_face:'))

        return HttpResponse('okay')

    if (chat_id != 5164975159):
        bot.send_message(chat_id=5164975159, text=message)
    return HttpResponse("Hi")


def download(request, video_id):
    try:
        print(video_id)
        video_file_name = FileInfo.objects.filter(video_id=video_id).first()
        print(model_to_dict(video_file_name))
        if video_file_name:
            return HttpResponse(open(video_file_name.video_name, 'rb'), content_type='video/mp4')
    except:
        print(traceback.format_exc())


    return HttpResponse('Video not found.Please try again')


def set_webhook(request):
   s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
   print(s)
   if s:
       return HttpResponse("webhook setup ok")
   else:
       return HttpResponse("webhook setup failed")
