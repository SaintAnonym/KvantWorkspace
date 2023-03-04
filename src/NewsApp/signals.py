from .models import KvantNews
from django.dispatch import receiver
from django.db.models.signals import pre_delete

# реализует приемник сигнала pre_delete для модели KvantNews. 
# Когда инстанс данной модели будет удаляться, приёмник автоматически вызовет функцию cleanNewsFiles(), 
# которая удалит все файлы, привязанные к данному инстансу.

@receiver(pre_delete, sender=KvantNews)
def cleanNewsFiles(sender, instance, **kwargs):
    for file in instance.files.all(): file.delete()