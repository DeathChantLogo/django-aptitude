from django.contrib import admin
from models import *

class QuestionDataAdmin(admin.ModelAdmin):
    pass

class RenderedQuestionAdmin(admin.ModelAdmin):
    pass

class SessionAdmin(admin.ModelAdmin):
    pass

admin.site.register(QuestionData, QuestionDataAdmin)
admin.site.register(RenderedQuestion, RenderedQuestionAdmin)
admin.site.register(Session, SessionAdmin)
