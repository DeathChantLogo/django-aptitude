from django.contrib import admin
from models import *

class QuestionDataAdmin(admin.ModelAdmin):
    list_display = ('text', 'display_type', 'difficulty')
    list_filter = ('type',)
    
    def display_type(self, obj):
        return obj.get_type_display()
    display_type.short_description = 'Question Type'
    display_type.admin_order_field = 'type'

class RenderedQuestionAdmin(admin.ModelAdmin):
    pass

class AptSessionAdmin(admin.ModelAdmin):
    list_display = ('display_username', 'time_started', 
                    'display_score', 'display_length')
    
    def display_score(self, obj):
        if obj.time_ended:
            return obj.get_final_grade()
        else:
            return "N/A"
    
    def display_length(self, obj):
        if obj.time_ended:
            return obj.time_ended - obj.time_started
        else:
            return "N/A"
    display_length.short_description = 'Length'
    
    def display_username(self, obj):
        return obj.user.username
    display_username.short_description = 'User'
    
admin.site.register(QuestionData, QuestionDataAdmin)
admin.site.register(RenderedQuestion, RenderedQuestionAdmin)
admin.site.register(AptSession, AptSessionAdmin)
