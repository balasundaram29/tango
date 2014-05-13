#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      AnnaiAll
#
# Created:     02/04/2014
# Copyright:   (c) AnnaiAll 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from django.contrib import admin
from rango.models import Category,Page,UserProfile

class PageAdmin(admin.ModelAdmin):
    list_display=('title','category','url')

admin.site.register(Category)
admin.site.register(Page,PageAdmin)
admin.site.register(UserProfile)
