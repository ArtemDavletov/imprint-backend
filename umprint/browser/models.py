import uuid

from django.db import models
from user.models import UserProfile

# Configs list
class UserAgent(models.Model):
    value = models.CharField(
        verbose_name="User-Agent", blank=False, max_length=3000, unique=True
    )

    def __unicode__(self):
        return self.value


class ScreenResolution(models.Model):
    width = models.PositiveIntegerField(verbose_name="width", blank=False, default=0)
    height = models.PositiveIntegerField(verbose_name="Height", blank=False, default=0)
    landscape = models.NullBooleanField(verbose_name="Land Scape", default=None)

    def __unicode__(self):
        return self.value


class Languages(models.Model):
    value = models.CharField(
        verbose_name="Language Code", blank=False, max_length=1000, unique=True
    )

    def __unicode__(self):
        return self.value


class Platform(models.Model):
    value = models.CharField(
        verbose_name="Platform", blank=False, max_length=200, unique=True
    )

    def __unicode__(self):
        return self.value


class FontPrint(models.Model):
    value = models.CharField(
        verbose_name="FontPrint name", blank=False, max_length=1000, unique=True
    )

    def __unicode__(self):
        return self.value


class ColorDepth(models.Model):
    value = models.PositiveIntegerField(
        verbose_name="ColorDepth", blank=False, default=0, unique=True
    )

    def __unicode__(self):
        return self.value


# Random Choice Configurations
class Configurations(models.Model):
    browser_type = models.ManyToManyField(
        "browser.BrowserType", related_name="browser_type"
    )
    browser_engine = models.ManyToManyField(
        "browser.BrowserEngine", related_name="browser_engine"
    )
    useragent = models.ManyToManyField(
        "browser.UserAgent", blank=False, verbose_name="User-Agent"
    )
    screenresolution = models.ManyToManyField(
        "browser.ScreenResolution", blank=False, verbose_name="Screen-Resoloution"
    )
    languages = models.ManyToManyField(
        "browser.Languages", blank=False, verbose_name="Languages"
    )
    platform = models.ManyToManyField(
        "browser.Platform", blank=False, verbose_name="Platform"
    )
    hardwareconcurrency = models.CharField(
        blank=False, verbose_name="HardwareConcurrency", max_length=200
    )
    memory = models.CharField(blank=False, verbose_name="memory", max_length=20)
    donottrack = models.NullBooleanField(
        default=None, blank=False, verbose_name="Do Not Track"
    )
    fontprint = models.ManyToManyField(
        "browser.FontPrint", blank=False, verbose_name="Font Prints"
    )
    colordeepth = models.ManyToManyField(
        "browser.ColorDepth", blank=False, verbose_name="Color Deepths"
    )

    def __unicode__(self):
        return self.value


class BrowserEngine(models.Model):
    class Meta:
        verbose_name = "Движки браузера (BrowserEngine)"
        verbose_name_plural = "Движки браузера (BrowserEngine)"

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


#
class InstanceBrowser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=200, blank=True, default="Browser name", verbose_name="Имя"
    )
    description = models.TextField(max_length=500, blank=True, verbose_name="Описание")
    # Configs
    browser_type = models.ForeignKey(
        "browser.BrowserType",
        on_delete=models.CASCADE,
        verbose_name="Тип браузера",
        related_name="browser_instance_browser_type",
    )
    browser_engine = models.ForeignKey(
        "browser.BrowserEngine",
        on_delete=models.CASCADE,
        verbose_name="Тип движка браузера",
        related_name="browser_instance_browser_engine",
    )
    useragent = models.CharField(blank=True, verbose_name="User-Agent", max_length=3000)
    screenresolution = models.CharField(
        blank=True, verbose_name="Screen-Resoloution", max_length=200
    )
    languages = models.CharField(blank=True, verbose_name="Languages", max_length=1000)
    platform = models.CharField(blank=True, verbose_name="Platform", max_length=300)
    hardwareconcurrency = models.CharField(
        blank=True, verbose_name="HardwareConcurrency", max_length=200
    )
    memory = models.CharField(blank=True, verbose_name="Memory", max_length=20)
    donottrack = models.NullBooleanField(
        blank=True, default=None, verbose_name="Do Not Track", max_length=20
    )
    fontprint = models.CharField(
        blank=True, verbose_name="Font Prints", max_length=5000
    )
    colordeepth = models.CharField(
        blank=True, verbose_name="Color Deepths", max_length=20
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
