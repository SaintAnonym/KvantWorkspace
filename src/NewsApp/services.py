from CoreApp.services.access import KvantObjectExistsMixin
from CoreApp.services.utils import ObjectManipulationManager
from django.urls import reverse_lazy as rl

from .models import KvantNews

# Сначала подключается модуль access, который содержит класс KvantObjectExistsMixin, 
# импортируется модуль utils с классом ObjectManipulationManager и два модуля для работы с моделью KvantNews.  


# Далее определяются три функции, которые используются для получения и изменения новостей:  

# 1) getNewsCount() возвращает количество новостей для ajax-пагинации; 
# 2) getNewsById(id) возвращает новость по ее id; 
# 3) createNewEvent(manager, request) создает новое событие, при этом удаляются все старые данные, на которые больше нет необходимости. 

def getNewsCount():
    """ Возвращает кол-во новостей для ajax пагинации """
    return len(KvantNews.objects.all())


def getNewsById(id):
    """ Вовзращает новость по ее id. """
    return KvantNews.objects.get(id=id)


def createNewEvent(manager, request):
    events = list(getNewsByType(news_type=True))
    while len(events) >= 5:
        last_event = events[0]
        events.remove(last_event); last_event.delete()
    return manager.createObject(request)

# Затем объявляется класс NewsObjectManipulationManager. 
# Он наследуется от класса ObjectManipulationManager, и используется для создания новых новостей. 

class NewsObjectManipulationManager(ObjectManipulationManager):
    def _constructRedirectUrl(self, **kwargs):
        return rl('detail_news', kwargs={'news_identifier': kwargs.get('obj').id})

# Далее объявляется класс-миксин NewsExistsMixin, наследующий класс KvantObjectExistsMixin. 
# Этот класс используется для проверки существования новостей. 


class NewsExistsMixin(KvantObjectExistsMixin):
    request_object_arg = 'news_identifier'

    def _objectExiststTest(self, object_id):
        return KvantNews.objects.filter(id=object_id).exists()

# Также определяется класс-миксин NewsAccessMixin, который наследует класс NewsExistsMixin. 
# Этот класс используется для проверки авторства новостей и доступа к ним.  


class NewsAccessMixin(NewsExistsMixin):
    request_object_arg = 'news_identifier'
    
    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            news = getNewsById(kwargs.get(self.request_object_arg))
            return self._newsAccessTest(news, kwargs.get('user')) 
        return False
    
    def _newsAccessTest(self, news, user):
        """ Тест на авторство """
        return news.author == user or user.permission == 'Администратор'

# Наконец, определяется функция getNewsByType(news_type). 
# Эта функция используется для получения новостей по указанному типу.

getNewsByType = lambda news_type: KvantNews.objects.filter(is_event=news_type)