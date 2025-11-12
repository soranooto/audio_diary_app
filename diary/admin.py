from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import AudioDiary

# AudioDiaryモデルを管理画面に表示
@admin.register(AudioDiary)
class AudioDiaryAdmin(admin.ModelAdmin):
    list_display = ('title', 'mood', 'created_at')  # 一覧表示する項目
    search_fields = ('title', 'mood')  # 検索できる項目
    list_filter = ('mood',)  # フィルターを表示する項目


