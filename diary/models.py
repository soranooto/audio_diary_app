from django.db import models
from django.contrib.auth.models import User

class AudioDiary(models.Model):
    MOOD_CHOICES = [
        ("😁元気", "😁 元気"),
        ("😢悲しい", "😢 悲しい"),
        ("😐普通", "😐 普通"),
        ("😍嬉しい", "😍 嬉しい"),
        ("😎かっこいい", "😎 かっこいい"),
        ("😴眠い", "😴 眠い"),
        ("🤔考え中", "🤔 考え中"),
        ("😇幸せ", "😇 幸せ"),
        ("😡怒り", "😡 怒り"),
        ("🥳お祝い", "🥳 お祝い"),
        ("😱びっくり", "😱 びっくり"),
        ("🤯やばい", "🤯 やばい"),
        ("🤗感謝", "🤗 感謝"),
        ("😤やる気", "😤 やる気"),
        ("その他", "その他"),
    ]

    title = models.CharField(max_length=100)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    emoji = models.CharField(max_length=5)
    color = models.CharField(max_length=7)
    audio_file = models.FileField(upload_to='audio/')
    text_entry = models.TextField(max_length=140)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


# 🎵 統合後の Profile モデル
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='profile_icons/', blank=True, null=True)
    status_message = models.CharField(max_length=200, blank=True)
    sns_link = models.URLField(blank=True)
    current_music = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username or self.user.username

    @property
    def icon_url(self):
        """アイコンが設定されていない場合はデフォルト画像を返す"""
        if self.icon:
            return self.icon.url
        return '/static/images/default_icon.png'
