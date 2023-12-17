import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField()
    creator = models.ForeignKey("auth.User",blank=True,related_name="creator_%(class)s_objects",on_delete=models.CASCADE)
    updater = models.ForeignKey("auth.User",blank=True,related_name="updater_%(class)s_objects",on_delete=models.CASCADE)
    date_added = models.DateTimeField(db_index=True,auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
