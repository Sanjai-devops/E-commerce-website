from django.contrib import admin
from .models import *

# the below tribble quotted codes are used to display the image and discription on the db admin page
"""class categoryAdmin(admin.ModelAdmin):
      list_display=("name","image","description") 
    admin.site.register(catagory,catagoryAdmin)   
"""
admin.site.register(catagory)
admin.site.register(Product)