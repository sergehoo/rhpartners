from pathlib import Path
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class PrivateCVStorage(FileSystemStorage):
    def __init__(self):
        super().__init__(location=Path(settings.BASE_DIR) / 'private_uploads')

    def url(self, name):
        raise ValueError('Les CV sont accessibles uniquement via une vue autorisée.')
