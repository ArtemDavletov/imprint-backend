from django.db import models


class Geolocation(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    latitude = models.IntegerField(verbose_name="Latitude")
    longitude = models.IntegerField(verbose_name="Longitude")
    accuracy = models.IntegerField(verbose_name="Точность")


class Proxy(models.Model):
    class RroxyChoices(models.TextChoices):
        WITHOUT = "WITHOUT"
        FREE = "FREE"
        TOR = "TOR"
        HTTP = "HTTP"
        SOCKS4 = "SOCKS4"
        SOCKS5 = "SOCKS5"

    id = models.AutoField(primary_key=True, editable=False)
    port = models.CharField(blank=True, max_length=15)
    host = models.PositiveIntegerField(blank=True)
    type = models.CharField(
        max_length=10,
        choices=RroxyChoices.choices,
        default=RroxyChoices.WITHOUT,
    )


class DeviceType(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(verbose_name="Device type", max_length=100)


class OSType(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(verbose_name="Разновидность операционной системы", max_length=100)


class MaskMediaDevices(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    video_inputs = models.PositiveIntegerField(default=0, verbose_name="Количество video inputs")
    audio_inputs = models.PositiveIntegerField(default=0, verbose_name="Количество audio inputs")
    audio_outputs = models.PositiveIntegerField(default=0, verbose_name="Количество audio outputs")


class UserAgent(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=1000)

    device_type = models.ForeignKey(
        DeviceType, on_delete=models.CASCADE, related_name="device_type"
    )

    os_type = models.ForeignKey(
        OSType, on_delete=models.CASCADE, related_name="os_type"
    )


class ScreenResolution(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    is_mobile = models.BooleanField(default=False)
    is_lanscape = models.BooleanField(default=False)


class UserAgentScreenResolutionRelation(models.Model):
    id = models.AutoField(primary_key=True, editable=False)

    user_agent = models.ForeignKey(
        UserAgent, on_delete=models.CASCADE, related_name="user_agent"
    )

    screen_resolution = models.ForeignKey(
        ScreenResolution, on_delete=models.CASCADE, related_name="screen_resolution"
    )


class ConfigModel(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    proxy = models.ForeignKey(
        Proxy, on_delete=models.CASCADE, related_name="proxy"
    )

    geolocation = models.ForeignKey(
        Geolocation, on_delete=models.CASCADE, related_name="geolocation"
    )

    ua_sr_relation = models.ForeignKey(
        UserAgentScreenResolutionRelation, on_delete=models.CASCADE, related_name="geolocation"
    )

    timezone = models.CharField(max_length=100)
