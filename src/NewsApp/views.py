from django.http import JsonResponse
from CoreApp.services.access import (KvantTeacherAndAdminAccessMixin,
                                     KvantWorkspaceAccessMixin)
from django.views import generic

from . import services
from .forms import KvantNewsFilesSaveForm, KvantNewsSaveForm
from .models import KvantNews
from AdminApp.services import getCourseQuery

# Класс для главной страницы новостей. Он наследует класс KvantWorkspaceAccessMixin и 
# предоставляет метод get_context_data для получения контекстных данных, 
# таких как максимальное количество новостей, список курсов и событий. 

class MainPageTemplateView(KvantWorkspaceAccessMixin, generic.TemplateView):
    """ Контроллер главной новостной страницы """
    template_name = 'NewsApp/MainPage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'max_news': services.getNewsCount(),
            'courses': getCourseQuery(self.request.user),
            'events': services.getNewsByType(news_type=True),})
        return context

# Класс для просмотра новостей. Получает информацию о новостях

class NewsDetailView(services.NewsExistsMixin, generic.DetailView):
    """ Контроллер детального просмотра новостей """
    model               = KvantNews
    pk_url_kwarg        = 'news_identifier'
    context_object_name = 'news'
    template_name       = 'NewsApp/NewsDetailView/index.html'

# Полученик списка всех новостей, которые относятся к типу новостей. 

class NewsListView(KvantWorkspaceAccessMixin, generic.ListView):
    """ Контроллер для организации пагинации по новостям """
    model               = KvantNews
    ordering            = ['-date', '-id']
    paginate_by         = 8
    template_name       = 'NewsApp/NewsPreview/index.html'
    context_object_name = 'all_news'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(all_news=services.getNewsByType(news_type=False),)
        return ctx

# Создание новостей
# Он наследуется от класса KvantTeacherAndAdminAccessMixin и предоставляет метод post 
# для создания новостей с помощью управляющего объекта NewsObjectManipulationManager. 

class NewsCreateView(KvantTeacherAndAdminAccessMixin, generic.View):
    """ Контроллер создания новости """
    def post(self, request, *args, **kwargs):
        object_manager = services.NewsObjectManipulationManager(
            [KvantNewsSaveForm, KvantNewsFilesSaveForm])
        return object_manager.createObject(request)

# Класс для редактирования новости
# Педоставляет метод post для обновления новости с помощью управляющего объекта NewsObjectManipulationManager. 

class NewsUpdateView(services.NewsAccessMixin, generic.View):
    """ Контроллер редактирования новости """
    def post(self, request, *args, **kwargs):
        news = services.getNewsById(kwargs.get('news_identifier'))
        object_manager = services.NewsObjectManipulationManager(
            [KvantNewsSaveForm, KvantNewsFilesSaveForm], object=news)
        return object_manager.updateObject(request)

# Для удаления новости. Наследует от класса services.NewsAccessMixin и предоставляет метод post для удаления новости. 

class NewsDeleteView(services.NewsAccessMixin, generic.View):
    """ Контроллер удаления новости """
    def post(self, request, *args, **kwargs):
        services.getNewsById(kwargs.get('news_identifier')).delete()
        return JsonResponse({'status': 200})

# Класс для создания события, наследуется от класса KvantTeacherAndAdminAccessMixin и предоставляет метод post 
# для создания событий с помощью управляющего объекта NewsObjectManipulationManager и метода createNewEvent.

class EventCreateView(KvantTeacherAndAdminAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        object_manager = services.NewsObjectManipulationManager(
            [KvantNewsSaveForm, KvantNewsFilesSaveForm])
        return services.createNewEvent(object_manager, request)
        