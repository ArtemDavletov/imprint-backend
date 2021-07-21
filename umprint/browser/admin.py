from django.contrib import admin
from browser.models import*

admin.site.register(UserAgent)
admin.site.register(ScreenResolution)
admin.site.register(Languages)
admin.site.register(Platform)
admin.site.register(HardwareConcurrency)
admin.site.register(Memory)
admin.site.register(DoNotTrack)
admin.site.register(FontPrint)
admin.site.register(ColorDepth)
admin.site.register(Configurations)

