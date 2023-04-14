from CoreApp.services.m2m import FileM2MBaseMixin, ManyToManyObjectCreateMixin
from CoreApp.services.utils import buildDate
from django import forms
from django.core.exceptions import ValidationError
from LoginApp.services import getUserById, isUserExists

from .models import KvantMessage, MailReceiver


# Обработка возможных исключений, проверка правильности заполнения полей письма

class MailReceiverSaveForm(forms.ModelForm):

    # Обращение к модели MailRecevier и к ее полям (создание миграции этой таблицы - 0001_inital.py)
    class Meta:
        model = MailReceiver
        fields = ('receiver', 'is_read')


# Проверка и отлов исключений и ошибка при заполнении заголовка письма
class KvantMailSaveForm(forms.ModelForm):

    # Обращение к модели KvantMessage и к ее полям (создание миграции этой таблицы - 0001_inital.py)
    class Meta:
        model = KvantMessage
        fields = ('sender', 'text', 'title')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Словарь с переопределенными ошибками. Переопределены сообщения, которые будут выдаваться полем
        self.fields['title'].error_messages.update({
            'invalid': u'Заголовок невалиден.',
            'required': u'Заголовок не может быть пустым.',
            'max_length': u'Заголовок не может превышать %(limit_value)d (сейчас %(show_value)d).',
        })


    def clean_title(self):
        # Проверка и приведение данных к общему формату.
        # При невозможности валидации - выдает ошибку
        if not self.cleaned_data.get('title').isprintable():
            raise forms.ValidationError('Заголовок содержит невалидые символы')
        if '/' in self.cleaned_data.get('title'):
            raise forms.ValidationError('Заголовок не может содержать символ "/".')
        return self.cleaned_data.get('title')


# Проверка и отлов исключений и ошибка при подгрузке файла
class KvantMailFileSaveForm(FileM2MBaseMixin):
    # Обращение к модели KvantMessage и к ее полю (создание миграции этой таблицы - 0001_inital.py)
    class Meta:
        model = KvantMessage
        fields = ('files',)

    def __init__(self, *args, **kwargs):
        super().__init__('files', *args, **kwargs)

        # Словарь с переопределенными ошибками. Переопределены сообщения, которые будут выдаваться полем
        self.fields['files'].error_messages.update({
            'max_upload_count': u'Объект не может содеражть более 16 файлов',
            'max_upload_weight': u'Суммарный объем файлов не может превышать 32mB.',
        })
    
    def getFileUploadPath(self):
        return f'mail/{buildDate(self.instance.date)}/{self.instance.title}'


# Проверка и отлов исключений и ошибка при указании получаетелей
class KvantMailReceiversForm(ManyToManyObjectCreateMixin):
    class Meta:
        model = KvantMessage
        fields = ('receivers',)

    def __init__(self, *args, **kwargs):
        super().__init__('receivers', *args, **kwargs)

        # Словарь с переопределенными ошибками. Переопределены сообщения, которые будут выдаваться полем
        self.fields['receivers'].error_messages.update({
            'invalid_choice': u'Выбранный пользователь не существует.',
            'required': u'Письмо должно содержать хотя бы одного получателя.',
        })

    # Получение списка всех возможных получателей
    def getData(self):
        return self.data.getlist('receivers')

    def validateValue(self, values):
        if not values:
            raise ValidationError(self.fields['receivers'].error_messages['required'])
        if not self._validateUsers(values):
            raise ValidationError(self.fields['receivers'].error_messages['invalid_choice'])

    # При существовании пользователя и отсуствия ошибок, подгрузка получателя в письмо
    def createObjects(self, values):
        receivers_user = []
        for user in values:
            form = MailReceiverSaveForm({'receiver': getUserById(user)})
            if form.is_valid(): receivers_user.append(str(form.save().id)) 
        return receivers_user

    def _validateUsers(self, users):
        """ Валидация пользователей на существование """
        for user in users:
            if not isUserExists(user): return False
        return True
