from LoginApp.services import getUserById
from ProjectApp.models import KvantProject
from ProjectApp.services.services import getClassedProject, getProjectById

from .forms import ChatMessageSaveForm

# В начале в инициализаторе класса объявляется атрибуты self.user_id и self.project_id, 
# которые принимают идентификатор пользователя и идентификатор проекта соответственно. 
# Затем метод проверки доступа вызывается, принимая идентификатор пользователя, для получения экземпляра пользователя.  

class ChatProjectAccessMixin:
    def __init__(self, user_id, project_id):
        self.user_id = user_id
        self.project_id = project_id
    
    # После этого вызывается метод _authenticateTest(), который проверяет, авторизован ли пользователь
    # Затем Объект ExiststTest вызывается, чтобы проверить, существует ли проект в БД
    
    def checkAccess(self):
        user = getUserById(self.user_id)
        if self._authenticateTest(user) and self._objectExiststTest(self.project_id):
            project = getProjectById(self.project_id)
            return self._chatAccessTest(project, user) and self._isActiveProject(project)
        return False
    
    def _authenticateTest(self, user):
        """ Тест на авторизованность """
        return user.is_authenticated
    
    def _objectExiststTest(self, object_id):
        return KvantProject.objects.filter(id=object_id).exists()
    
    # Метод _isActiveProject() используется для проверки того, является ли проект активным.
    
    def _isActiveProject(self, project):
        return hasattr(project, 'activekvantproject')
    
    # _chatAccessTest() используется для проверки того, разрешено ли пользователю использовать чат проекта. 
    
    def _chatAccessTest(self, project, user):
        return (project.tutor == user) or (project.teamleader == user) or (user in project.team.all())

# Функция сначала принимает сообщение и идентификатор пользователя и идентификатор проекта.
# Затем создается экземпляр формы ChatMessageSaveForm, который содержит информацию о пользователе и сообщении. 
# Затем форма проверяется на соответствие правилам и если валидна, сохраняется (form.save())

def addProjectChatMessage(message, user_id, project_id):
    form = ChatMessageSaveForm({
        'sender': getUserById(user_id), 'message': message})
    if form.is_valid():
        chat_instance = form.save()
        project = getProjectById(project_id)
        getClassedProject(project).chat.add(chat_instance)

# Затем сообщение добавляется к экземпляру проекта (getClassedProject(project).chat.add(chat_instance)).
# Если форма не валидна, возвращаются ошибки.


        return chat_instance
    return form.errors
