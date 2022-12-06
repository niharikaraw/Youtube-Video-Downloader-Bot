from bot import views
from django.urls import path
from bot.views import download, introduction


urlpatterns = [
    path('5558568629:AAGHAg7y7Ilr778_WFtBx-Lik3R7p8sVsh8', introduction),
    path('set_webhook/', views.set_webhook),
    path('download/<str:video_id>', download)

]