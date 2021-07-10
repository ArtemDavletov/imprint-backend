import uuid

from django.db import models

from user.models import UserProfile


class BrowserEngine(models.Model):
    class BrowserEngineChoices(models.TextChoices):
        CHROMIUM = 'CHROMIUM'
        FIREFOX = 'FIREFOX'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    engine_type = models.CharField(
        max_length=10,
        choices=BrowserEngineChoices.choices,
        default=BrowserEngineChoices.CHROMIUM,
    )


class BrowserType(models.Model):
    class BrowserChoices(models.TextChoices):
        CHROME = 'CHROME'
        MAZILLA = 'MAZILLA'
        SAFARI = 'SAFARI'
        OPERA = 'OPERA'
        TOR = 'TOR'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    engine_type = models.CharField(
        max_length=10,
        choices=BrowserChoices.choices,
        default=BrowserChoices.CHROME,
    )


class RulesType(models.Model):
    class RulesChoices(models.TextChoices):
        VIEW = 'VIEW'
        EDIT = 'EDIT'
        ADMIN = 'ADMIN'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    engine_type = models.CharField(
        max_length=10,
        choices=RulesChoices.choices,
        default=RulesChoices.VIEW,
    )


class InstanceBrowser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    browser_type = models.ForeignKey(BrowserType, on_delete=models.CASCADE, related_name='browser_type')
    browser_engine = models.ForeignKey(BrowserType, on_delete=models.CASCADE, related_name='browser_engine')

    folder_name = models.CharField(max_length=20, blank=True, verbose_name='Название папки')

    def __unicode__(self):
        return self.name


class UserProfileInstanceBrowserRelation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user')
    browser = models.ForeignKey(InstanceBrowser, on_delete=models.CASCADE, related_name='browser')

    rule_type = models.ForeignKey(RulesType, on_delete=models.CASCADE, related_name='rule')
    is_creator = models.BooleanField(max_length=20, blank=True, verbose_name='Является создателем')

    def __unicode__(self):
        return f"Relation with browser for user={self.user.login}"
