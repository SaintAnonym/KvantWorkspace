from django.http import JsonResponse
from src.AdminApp.services import getCourseQuery
from src.CoreApp.services.access import (KvantTeacherAndAdminAccessMixin,
                                     KvantWorkspaceAccessMixin)
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import generic
from src.LoginApp.forms import ImageChangeForm, PasswordChangeForm
from src.LoginApp.models import KvantUser
from src.LoginApp.services import getUserById
from src.ProjectApp.services.services import KvantProjectQuerySelector
from src.RegisterApp.forms import *

from . import services
from .forms import (KvantAwardSaveForm, SocialInfoBannerSaveForm,
                    SocialInfoSaveForm)
from src.RegisterApp.services import getUserPersonalInfo


class SettingsPageTemplateView(services.UserExistsMixin, generic.DetailView):
    # Подключение к модели KvantUser, содержащей в себе инф-ю о пользователе
    model = KvantUser

    # Здесь задаются права пользователя?...
    pk_url_kwarg        = 'user_identifier'
    context_object_name = 'requested_user'

    # Адрес шаблона
    template_name       = 'ProfileApp/ProfileInfo/index.html'


class PortfolioPageListView(services.UserExistsMixin, generic.DetailView):
    # Подключение к модели KvantUser, содержащей в себе инф-ю о пользователе
    model               = KvantUser

    # Здесь задаются права пользователя?...
    pk_url_kwarg        = 'user_identifier'
    context_object_name = 'requested_user'

    # Адрес шаблона
    template_name       = 'ProfileApp/ProfilePortfolio/index.html'

    def get_context_data(self, **kwargs):
        # словарь, представляющий собой контекст шаблона
        context = super().get_context_data(**kwargs)

        # обноваление контекста на основе данных о грамотах пользователя
        context.update(awards=services.getUserAwardsQuery(kwargs.get('object')))

        return context


class StaticsPageTemplateView(services.UserExistsMixin, generic.DetailView):
    # Подключение к модели KvantUser, содержащей в себе инф-ю о пользователе
    model               = KvantUser

    # Здесь задаются права пользователя?...
    pk_url_kwarg        = 'user_identifier'
    context_object_name = 'requested_user'

    # Адрес шаблона
    template_name       = 'ProfileApp/ProfileStatistics/index.html'

    def get_context_data(self, **kwargs):
        # словарь, представляющий собой контекст шаблона
        context = super().get_context_data(**kwargs)

        #обноваление контекста на основе данных о курсах пользователя
        context.update(courses=getCourseQuery(kwargs.get('object')))
        
        return context


class ProjectsPageTemplateView(services.UserExistsMixin, generic.DetailView):
    # Подключение к модели KvantUser, содержащей в себе инф-ю о пользователе
    model               = KvantUser

    # Здесь задаются права пользователя?...
    pk_url_kwarg        = 'user_identifier'
    context_object_name = 'requested_user'

    # Адрес шаблона
    template_name       = 'ProfileApp/ProfileProjects/index.html'

    def get_context_data(self, **kwargs):
        # словарь, представляющий собой контекст шаблона
        context = super().get_context_data(**kwargs)

        context.update({
            'projects': KvantProjectQuerySelector(
                kwargs.get('object'), {'subject': 'mine'}).getCatalogQuery()
        })
        return context


class LogoutKvantUserView(KvantWorkspaceAccessMixin, generic.View):
    def get(self, request, *args, **kwargs):
        logout(request); return redirect('login_page')


class KvantUserChangeView(services.UserManipulationMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        # Шаблон профиля
        self.forms, self.u_func = {
            # аватарка профиля
            'image': ([ImageChangeForm], lambda u: u),

            # Инф-я о соц.сетях привязанных к аккаунту
            'social': ([SocialInfoSaveForm], lambda u: u.socialinfo),

            # Инф-я о баннере вверху страницы профиля
            'banner': ([SocialInfoBannerSaveForm], lambda u: u.socialinfo),

            # Раздел личные данные, ученик
            'student': ([StudentPersonalInfoSaveForm], lambda u: u.studentpersonalinfo),

            # инф-я о родителях
            'father': ([StudentParentSaveForm], lambda u: u.studentpersonalinfo.father),
            'mother': ([StudentParentSaveForm], lambda u: u.studentpersonalinfo.mother),

            # документы
            'staff': ([StaffPersonalInfoSaveForm], lambda u: u.staffpersonalinfo),
            'staff_scans': ([StaffScanSaveForm], lambda u: u.staffpersonalinfo.scans),
            'student_scans': ([StudentScanSaveForm], lambda u: u.studentpersonalinfo.scans),
        }.get(request.POST.get('type'), (None, None))
        kwargs.update(user_func=self.u_func)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Получает пользователя по данному id Если пользователь не существует, возвращает None
        user = getUserById(self.kwargs.get('user_identifier'))
        object_manager = services.UserManipulationManager(self.forms, object=self.u_func(user))
        return object_manager.updateUserObj(request, user)
    
    def _profileAccessTest(self, user, requested_user):
        # отлов возможной ошибки при получении данных о пользователе
        try:
            self.u_func(requested_user)
        except Exception as e:
            return False
        return super()._profileAccessTest(user, requested_user)


class PortfolioAddForm(services.UserExistsMixin, KvantTeacherAndAdminAccessMixin, generic.View):
    # Контроллер добавления портфолио
    def dispatch(self, request, *args, **kwargs):
        kwargs.update(user_identifier=request.POST.get('user'))
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        object_manager = services.PortfolioManipulationManager([KvantAwardSaveForm])
        return object_manager.createPortfolioInstance(request)


class PasswordChangeView(services.UserManipulationMixin, generic.View):
    # Контроллер изменения пароля портфолио
    def post(self, request, *args, **kwargs):
        # Получение инф-и о пользователе на основе его id
        user = getUserById(kwargs.get('user_identifier'))
        manager = services.UserChangePasswordManager([PasswordChangeForm], object=user)
        return manager.updateObject(request)


class UserScanDeleteView(services.UserManipulationMixin, generic.View):
    def post(self, request, *args, **kwargs):
        # Получение инф-и о пользователе на основе его id
        user_info = getUserPersonalInfo(getUserById(kwargs.get('user_identifier')))
        if hasattr(user_info.scans, request.POST.get('scan')):
            getattr(user_info.scans, request.POST.get('scan')).delete()
        return JsonResponse({'status': 200})
    
    def _profileAccessTest(self, user, requested_user):
        # Обработка исключения
        if self.request.POST.get('scan') is None:
            return False
        return super()._profileAccessTest(user, requested_user)
        
