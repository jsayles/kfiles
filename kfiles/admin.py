from django.contrib import admin

from models import *

# Register the objects with the admin interface
admin.site.register(Project)
admin.site.register(Project_User)
admin.site.register(File_Upload)
admin.site.register(Page_Text)
