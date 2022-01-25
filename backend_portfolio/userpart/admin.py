from django.contrib import admin
from .models import *


# Apercu des champs de l'annonce sur la partie administrateur
class AdminAnnonce(admin.ModelAdmin):
    list_display = ('username', 'email', 'message', 'type_feedback')


admin.site.register(TypeFeedBack)
admin.site.register(Feedback, AdminAnnonce)
admin.site.register(User)
admin.site.register(SubTaskProject)
admin.site.register(TitleProject)
admin.site.register(TaskProject)
admin.site.register(Assignement)
admin.site.register(AssignementProject)
