from django.contrib import admin

# Register your models here.
from browser.models import *

admin.site.register(UserAgent)
admin.site.register(ScreenResolution)
admin.site.register(Languages)
admin.site.register(Platform)
admin.site.register(FontPrint)
admin.site.register(ColorDepth)
admin.site.register(Configurations)
admin.site.register(BrowserEngine)
admin.site.register(BrowserType)
admin.site.register(Folder)
admin.site.register(InstanceBrowser)
admin.site.register(UserProfileInstanceBrowserRelation)
