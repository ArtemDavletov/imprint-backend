import uuid

from django.db import models

from user.models import UserProfile


class BrowserEngine(models.Model):
    class BrowserEngineChoices(models.TextChoices):
        CHROMIUM = 'CHROMIUM'
        FIREFOX = 'FIREFOX'

    id = models.AutoField(primary_key=True, editable=False)
    engine_type = models.CharField(
        max_length=10,
        choices=BrowserEngineChoices.choices,
        default=BrowserEngineChoices.CHROMIUM,
    )


class BrowserType(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=300, default='Chrome', verbose_name='Заголовок', blank=False)

    def __unicode__(self):
        return self.name


# class RulesType(models.Model):
#     class RulesChoices(models.TextChoices):
#         VIEW = 'VIEW'
#         EDIT = 'EDIT'
#         ADMIN = 'ADMIN'
#
#     id = models.AutoField(primary_key=True, editable=False)
#     rule_type = models.CharField(
#         max_length=10,
#         choices=RulesChoices.choices,
#         default=RulesChoices.VIEW,
#     )
#
#     def __unicode__(self):
#         return self.rule_type


class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=True, verbose_name='Имя')
    description = models.TextField(max_length=500, blank=True, verbose_name='Описание')

    def __unicode__(self):
        return f'{self.name=}'


class InstanceBrowser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=200, blank=True, default='Browser name', verbose_name='Имя')
    description = models.TextField(max_length=500, blank=True, verbose_name='Описание')
    browser_type = models.ForeignKey(BrowserType, on_delete=models.CASCADE, related_name='browser_type')
    browser_engine = models.ForeignKey(BrowserEngine, on_delete=models.CASCADE, related_name='browser_engine')

    folder_name = models.ForeignKey(Folder, on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='Название папки')

    def __unicode__(self):
        return self.name

    @property
    def type(self):
        return self.browser_type.name

    @property
    def engine(self):
        return self.browser_engine.name

    @property
    def foldername(self):
        return self.folder_name.name


class UserProfileInstanceBrowserRelation(models.Model):
    ACCESS_TO_EDIT = ("ADMIN", "EDIT")

    class RulesChoices(models.TextChoices):
        VIEW = 'VIEW'
        EDIT = 'EDIT'
        ADMIN = 'ADMIN'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user')
    browser = models.ForeignKey(InstanceBrowser, on_delete=models.CASCADE, related_name='browser')
    is_creator = models.BooleanField(max_length=20, blank=True, verbose_name='Является создателем')
    rule_type = models.CharField(
        max_length=10,
        choices=RulesChoices.choices,
        default=RulesChoices.VIEW,
    )

    def __unicode__(self):
        return f"Relation with browser for user={self.user.login}"
