from io import BytesIO
from os.path import splitext
from sys import getsizeof

import fitz
from src.CoreApp.services.access import KvantObjectExistsMixin
from src.CoreApp.services.image import ImageThumbnailBaseMixin
from src.CoreApp.services.utils import ObjectManipulationManager
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse_lazy as rl
from src.LoginApp.models import KvantUser
from src.LoginApp.services import getUserById
from PIL import Image

from .models import KvantAward
from django.contrib.auth import login


def getUserAwardsQuery(user):
    # Возвращает все грамоты user
    return KvantAward.objects.filter(user=user)


class UserManipulationManager(ObjectManipulationManager):
    # JsonResponse - подкласс, HttpResponse, отвечает за отправку клиенту данных в формате JSON

    # Генерирует JsonResponse на ajax запрос
    def updateUserObj(self, request, user):
        obj_or_errors = self._getUpdatedObject(request)
        return self.getResponse(obj_or_errors, user=user)
    
    def _constructRedirectUrl(self, **kwargs):
        return rl('info_page', kwargs={'user_identifier': kwargs.get('user').id})

    # Генерирует JsonResponse на ajax запрос изменения пароля
class UserChangePasswordManager(ObjectManipulationManager):
    def updateObject(self, request):
        user_or_errors = self._getUpdatedObject(request)

        if isinstance(user_or_errors, KvantUser):
            if request.user == user_or_errors:
                login(request, user_or_errors)
        return self.getResponse(user_or_errors)
    
    def _constructRedirectUrl(self, **kwargs):
        return rl('info_page', kwargs={'user_identifier': kwargs.get('obj').id})

    # Генерирует JsonResponse на ajax запрос действия с портфоли
class PortfolioManipulationManager(ObjectManipulationManager):
    def createPortfolioInstance(self, request):
        user_id = request.POST.get('user')
        return self.getResponse(self._getCreatedObject(request), user_id=user_id)
    
    def _constructRedirectUrl(self, **kwargs):
        return rl('portfolio_page', kwargs={'user_identifier': kwargs.get('user_id')})


# Ковертирование PFD в JPG
# Используется в forms.py для конвертирование подгружаемых дипломов
class PDFToImageManager(ImageThumbnailBaseMixin):
    def __init__(self, coef):
        super().__init__(coef)
    
    def makeImageThumbnail(self, image_file):
        if image_file.content_type == 'application/pdf':
            return super().makeImageThumbnail(self._convertPdfToImage(image_file))
        return super().makeImageThumbnail(image_file)
    
    def _convertPdfToImage(self, pdf_file):
        image = BytesIO()
        document = fitz.open('pdf', pdf_file.read())
        file_name = f'{splitext(pdf_file.name)[0]}.jpeg'

        zoom_matrix = fitz.Matrix(2, 2) # 2 - zoom коэффициент
        byte_pdf = BytesIO(document[0].getPixmap(matrix=zoom_matrix).tobytes())
        
        Image.open(byte_pdf).save(image, format='JPEG', quality=90)
        
        return InMemoryUploadedFile(
            image, 'FileField', file_name, 
            'image/jpeg', getsizeof(image), None
        ) 
    

class UserExistsMixin(KvantObjectExistsMixin):
    request_object_arg = 'user_identifier'

    def _objectExiststTest(self, object_id):
        return KvantUser.objects.filter(id=object_id).exists()


class UserManipulationMixin(UserExistsMixin):
    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            requested_user = getUserById(kwargs.get(self.request_object_arg))
            return self._profileAccessTest(kwargs.get('user'), requested_user)
        return False
    
    def _profileAccessTest(self, user, requested_user):
        return user == requested_user or user.permission != 'Ученик'
