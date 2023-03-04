from django import forms
from .models import ChatMessage

# создает форму, которую вы можете использовать для сохранения сообщений чата в базе данных 

class ChatMessageSaveForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = '__all__'