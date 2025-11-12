from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'diary'

urlpatterns = [
    path('', views.diary_list, name='diary_list'),  # 音声日記一覧ページ
    path('create/', views.diary_create, name='diary_create'),  # 音声日記作成ページ
    path('<int:pk>/', views.diary_detail, name='diary_detail'),  # 音声日記詳細ページ
    path('mypage/', views.mypage, name='mypage'),  # マイページ
    path('edit_profile/', views.edit_profile, name='edit_profile'),  # プロフィール編集
    path('stickers/', views.sticker_page, name='sticker_page'),  # ステッカー一覧
    path('settings/', views.settings_page, name='settings'),  # 設定ページ
    path('chatbot/', views.chatbot_page, name='chatbot'),# chatbot
]

# 開発サーバーでメディアファイルを提供するための設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


