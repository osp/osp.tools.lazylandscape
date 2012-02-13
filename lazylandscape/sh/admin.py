from sh.models import *
from django.contrib import admin


class MethodInline(admin.StackedInline):
    model = ShMethods
    extra = 0
    fieldsets = ( 
                    (None, { 'fields': (('name','args'),'comment') } ),
                    (None, { 'fields': ['body'] } )
                )
    
class AttrInline(admin.StackedInline):
    model = ShAttributes
    extra = 0
    fieldsets = [[None, { 'fields': (('name', 'value'), 'comment') }]]
 

class ClassAdmin(admin.ModelAdmin):
    fieldsets = ( 
                    (None, { 'fields': (('field', 'name'),('lang','public'), 'comment') }),
                    ('Relations', { 'fields': ('deps','parents')}),
                )
    list_display = ('name', 'field', 'lang')
    list_filter = ['field','lang']
    inlines = [ AttrInline, MethodInline ]
    
    form = RelationForm
    

admin.site.register(ShClasses, ClassAdmin)