import os
import uuid

from django.utils import timezone
from django.utils.deconstruct import deconstructible


import os
import uuid

from django.utils import timezone


class UploadToPath:
    """
    Callable used as `upload_to=` for FileField / ImageField.

    Stores files under:
        media/<dirname>/<year>/<month>/<uuid>.<ext>

    Usage:
        file = models.FileField(upload_to=UploadToPath('nafath/files'))
        file = models.FileField(upload_to=UploadToPath('educational_contents'))

    Implements `deconstruct()` manually so Django migrations can serialize it
    reliably as:
        contract.helper.UploadToPath('nafath/files')
    """

    def __init__(self, dirname):
        # dirname: str  OR  callable(instance) -> str
        self.dirname = dirname

    def __call__(self, instance, filename):
        ext = os.path.splitext(filename)[1].lower()
        new_name = f"{uuid.uuid4().hex}{ext}"
        now = timezone.now()
        base = self.dirname(instance) if callable(self.dirname) else self.dirname
        return f"{base}/{now.year}/{now.month:02d}/{new_name}"

    # ---- required for migrations ----
    def deconstruct(self):
        return (
            "contract.helper.UploadToPath",   # import path
            [self.dirname],                    # args
            {},                                # kwargs
        )

    # ---- required so Django can compare old vs new ----
    def __eq__(self, other):
        return isinstance(other, UploadToPath) and self.dirname == other.dirname

    def __hash__(self):
        return hash(self.dirname if isinstance(self.dirname, str) else repr(self.dirname))

    def __repr__(self):
        return f"UploadToPath({self.dirname!r})"