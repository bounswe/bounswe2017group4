from django.contrib import admin
from .models import User, UserComment, UserInterest, UserRating, Response, Edge, History

admin.site.register(User)
admin.site.register(UserComment)
admin.site.register(UserInterest)
admin.site.register(UserRating)
admin.site.register(Response)
admin.site.register(Edge)
admin.site.register(History)
# Register your models here.
