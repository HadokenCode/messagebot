# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone

class Message(models.Model):
    SOURCE_DEFAULT = 0
    SOURCE_VK = 1
    SOURCE_TELEGRAM = 2
    SOURCE_CHOICES = ( 
        (SOURCE_DEFAULT, 'Пусто'),
        (SOURCE_VK, 'ВКонтакте'),
        (SOURCE_TELEGRAM, 'Телеграм'),
    )

    source = models.IntegerField(default=SOURCE_DEFAULT, choices=SOURCE_CHOICES)
    body = models.TextField()
    user_id = models.CharField(max_length=50)
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return '#{id} [{source} - {user_id}] {body}'.format(
            id=self.id,
            body=self.body[:50],
            source = self.get_source_display(),
            user_id=self.user_id
        )
