from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from djangoblog.utils import get_current_site


# Create your models here.

class BlogUser(AbstractUser):
    nickname = models.CharField(_('nick name'), max_length=100, blank=True)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)
    source = models.CharField(_('create source'), max_length=100, blank=True)

    def get_absolute_url(self):
        return reverse(
            'blog:author_detail', kwargs={
                'author_name': self.username})

    def __str__(self):
        return self.email

    def get_full_url(self):
        site = get_current_site().domain
        url = "https://{site}{path}".format(site=site,
                                            path=self.get_absolute_url())
        return url

    def get_unread_notifications_count(self):
        return Notification.objects.filter(recipient=self, is_read=False).count()

    class Meta:
        ordering = ['-id']
        verbose_name = _('user')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'


class Notification(models.Model):
    """站内消息通知"""
    class NotificationType(models.TextChoices):
        COMMENT_REPLY = ('comment_reply', _('Comment Reply'))
        SYSTEM_NOTICE = ('system_notice', _('System Notice'))
        ARTICLE_APPROVAL = ('article_approval', _('Article Approval'))

    recipient = models.ForeignKey(
        BlogUser,
        verbose_name=_('Recipient'),
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    sender = models.ForeignKey(
        BlogUser,
        verbose_name=_('Sender'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sent_notifications'
    )
    title = models.CharField(_('Title'), max_length=200)
    content = models.TextField(_('Content'))
    notification_type = models.CharField(
        _('Notification Type'),
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.COMMENT_REPLY
    )
    target_url = models.URLField(_('Target URL'), max_length=500, blank=True, null=True)
    is_read = models.BooleanField(_('Is Read'), default=False)
    create_time = models.DateTimeField(_('Create Time'), default=now)

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.title}"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])

    class Meta:
        ordering = ['-create_time']
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
