import uuid

from django.db import models
from user.models import UserProfile


# Configs list
class UserAgent(models.Model):
    value = models.CharField(verbose_name='User-Agent', blank=False, max_length=3000,  unique=True)
    def __unicode__(self):
        return self.value

class ScreenResolution(models.Model):
    weight = models.PositiveIntegerField(verbose_name='Weight', blank=False, default=0)
    height = models.PositiveIntegerField(verbose_name='Height', blank=False, default=0)
    def __unicode__(self):
        return self.value

class Languages(models.Model):
    value = models.CharField(verbose_name='Language Code', blank=False, max_length=1000,  unique=True)
    def __unicode__(self):
        return self.value

class Platform(models.Model):
    value = models.CharField(verbose_name='Platform', blank=False, max_length=200,  unique=True)
    def __unicode__(self):
        return self.value

class HardwareConcurrency(models.Model):
    value = models.PositiveIntegerField(verbose_name='hardwareConcurrency', blank=False, default=0,  unique=True)
    def __unicode__(self):
        return self.value

class Memory(models.Model):
    value = models.DecimalField(verbose_name='Memory', max_digits=5, decimal_places=2, blank=False,  unique=True)
    def __unicode__(self):
        return self.value

class DoNotTrack(models.Model):
    value = models.NullBooleanField(verbose_name='DoNotTrack', blank=False,  unique=True)
    def __unicode__(self):
        return self.value

class FontPrint(models.Model):
    value = models.CharField(verbose_name='FontPrint name', blank=False, max_length=1000, unique=True)
    def __unicode__(self):
        return self.value

class ColorDepth(models.Model):
    value = models.PositiveIntegerField(verbose_name='ColorDepth', blank=False, default=0, unique=True)
    def __unicode__(self):
        return self.value
        
# Random Choice Configurations
class Configurations(models.Model):
    useragent           = models.ManyToManyField('browser.UserAgent', blank=False, verbose_name='User-Agent')
    screenresolution    = models.ManyToManyField('browser.ScreenResolution', blank=False, verbose_name='Screen-Resoloution')
    languages           = models.ManyToManyField('browser.Languages', blank=False, verbose_name='Languages')
    platform            = models.ManyToManyField('browser.Platform', blank=False, verbose_name='Platform')
    hardwareconcurrency = models.ManyToManyField('browser.HardwareConcurrency', blank=False, verbose_name='HardwareConcurrency')
    memory              = models.ManyToManyField('browser.Memory', blank=False, verbose_name='Platform')
    donottrack          = models.ManyToManyField('browser.DoNotTrack', blank=False, verbose_name='Do Not Track')
    fontprint           = models.ManyToManyField('browser.FontPrint', blank=False, verbose_name='Font Prints')
    colordeepth         = models.ManyToManyField('browser.ColorDepth', blank=False, verbose_name='Color Deepths')
    def __unicode__(self):
        return self.value


class BrowserEngine(models.Model):
    class BrowserEngineChoices(models.TextChoices):
        CHROMIUM = "CHROMIUM"
        FIREFOX = "FIREFOX"

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(
        max_length=10,
        choices=BrowserEngineChoices.choices,
        default=BrowserEngineChoices.CHROMIUM,
    )


class BrowserType(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(
        max_length=300, default="Chrome", verbose_name="Заголовок", blank=False
    )

    def __unicode__(self):
        return self.name


class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=True, verbose_name="Имя")
    description = models.TextField(max_length=500, blank=True, verbose_name="Описание")

    def __unicode__(self):
        return f"{self.name=}"

    @property
    def folder_uuid(self):
        return self.id


class InstanceBrowser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(
        max_length=200, blank=True, default="Browser name", verbose_name="Имя"
    )
    description = models.TextField(max_length=500, blank=True, verbose_name="Описание")
    browser_type = models.ForeignKey(
        BrowserType, on_delete=models.CASCADE, related_name="browser_type"
    )
    browser_engine = models.ForeignKey(
        BrowserEngine, on_delete=models.CASCADE, related_name="browser_engine"
    )

    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Название папки",
    )

    def __unicode__(self):
        return self.name

    @property
    def type(self):
        return self.browser_type.name

    @property
    def engine(self):
        return self.browser_engine.name

    @property
    def folder_uuid(self):
        return self.folder.id

    @property
    def folder_name(self):
        return self.folder.name

    @property
    def folder_description(self):
        return self.folder.description


class UserProfileInstanceBrowserRelation(models.Model):
    ACCESS_TO_READ = {"VIEW", "ADMIN", "EDIT"}
    ACCESS_TO_EDIT = {"ADMIN", "EDIT"}
    ACCESS_TO_SHARE = {"ADMIN"}
    ACCESS_TO_DELETE = {"ADMIN"}

    class RulesChoices(models.TextChoices):
        VIEW = "VIEW"
        EDIT = "EDIT"
        ADMIN = "ADMIN"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="user")
    browser = models.ForeignKey(
        InstanceBrowser, on_delete=models.CASCADE, related_name="browser"
    )
    is_creator = models.BooleanField(
        max_length=20, blank=True, verbose_name="Является создателем"
    )
    rule_type = models.CharField(
        max_length=10,
        choices=RulesChoices.choices,
        default=RulesChoices.VIEW,
    )

    def __unicode__(self):
        return f"Relation with browser for user={self.user.login}"
