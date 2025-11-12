from django import forms
from .models import AudioDiary, Profile


# 🎵 音声日記フォーム
class AudioDiaryForm(forms.ModelForm):
    class Meta:
        model = AudioDiary
        fields = ['title', 'mood', 'emoji', 'color', 'audio_file', 'text_entry', 'image']


# 👤 プロフィール編集フォーム（旧 UserProfileForm）
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['icon', 'username', 'status_message']

