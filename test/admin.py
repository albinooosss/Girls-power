from django.contrib import admin
from .models import *

admin.site.register(Test)
admin.site.register(User)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Answer)

