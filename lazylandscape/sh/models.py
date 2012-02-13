# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.forms import ModelForm

import reversion

newline = "\n"
tab = "    "

class ShClasses(models.Model):
    #id = models.IntegerField(null=False, primary_key=True, blank=False)
    name = models.CharField(max_length=256, blank=False)
    comment = models.TextField(blank=True)
    field = models.CharField(max_length=256, blank=False)
    lang = models.CharField(max_length=32, blank=False, choices=[['python','Python'],['php','PHP'],['js','Javascript']])
    public = models.BooleanField(default=False)
    
    parents = models.ManyToManyField('self',db_table="ll_parents",blank=True)
    deps = models.ManyToManyField('self',db_table="ll_deps",blank=True)
    
    class Meta:
        db_table = u'll_classes'
        
    def __init__(self, *args, **kwargs):
        super(ShClasses, self).__init__(*args, **kwargs)
        self.attachRevision()
        
    def __unicode__(self):
        return self.name
        
    def str(self):
        return self.__unicode__()
        
    def write_class_python(self, wp):
        if self.id in wp:
            return
        
        wp.append(self.id)
        ret = [newline]
        
        if hasattr(self, 'rel_target'):
            for r in self.rel_target.all():
                ret.append(r.write_class_python(wp))
        
        #for p in self.deps.all():
            #ret.append(ShClasses.objects.get(id=p.dep).write_class_python(wp))
            
        #for p in self.parents.all():
            #ret.append(ShClasses.objects.get(id=p.dep).write_class_python(wp))
            
        extend = []
        if hasattr(self, 'rel_target'):
            for p in self.rel_target.filter(name='parent'):
                #parent = ShClasses.objects.get(id=p.parent)
                extend.append(p.field + '_' + p.name)
        
        if len(extend) > 0:
            ret.append(newline+'class ' + self.field + '_' + self.name + '('+ ','.join(extend) +'):'+ newline)
        else:
            ret.append(newline+'class ' + self.field + '_' + self.name + '(object):' + newline)
                
        for a in self.attrs.all():
            ret.append(tab + a.name + ' =  ' + a.value + newline)
        
        for m in self.methods.all():
            args = ['self']
            for a in m.args.split(','):
                if len(a.strip()) > 0:
                    args.append(a)
            hasBody = len(m.body.strip()) > 0
            tab2 = tab+tab
            if hasBody:
                tabBody = []
                for l in m.body.splitlines():
                    tabBody.append(''.join([tab2,l,newline]))
                ret.append( newline.join([ tab + 'def ' + m.name +'(' + ','.join(args) + '):', tab2, ''.join(tabBody) ,newline]) )
            else:
                fname = tab + 'def ' + m.name +'(' + ','.join(args) + '):'
                ret.append( newline.join([ fname, tab2 + 'pass' , newline ] ) )
            
        ret.append(newline)
        return ''.join(ret)  
        
    def get_python_source(self):
        wp = []
        return self.write_class_python( wp)
        
    def source(self):
        if self.lang == 'python':
            return self.get_python_source()
        return ''
        
    def attachRevision(self):
        if self.id is not None:
            self.versions = reversion.get_unique_for_object(self)
        
reversion.register(ShClasses)
class RelationForm(ModelForm):
    class Meta:
        model = ShClasses
    def __init__(self, *args, **kwargs):
        super(RelationForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            #for i in dir(self.fields['parents']):
                #print '%s => %s' % (i, getattr(self.fields['parents'],i))
            self.fields['parents'].choices = self.rel_choice(kwargs['instance'])
            self.fields['deps'].choices = self.rel_choice(kwargs['instance'])
            
    def rel_choice(self, instance):
        cx = ShClasses.objects.filter(lang = instance.lang).exclude(id = instance.id)
        ret = {}
        for c in cx:
            if c.field not in ret:
                ret[c.field] = []
            ret[c.field].append(  [str(c.id), c.name] )
        
        ret0 = []
        for i in ret:
            tmp = []
            for j in ret[i]:
                tmp.append(j)
            ret0.append([i,tmp])
        
        return ret0
                    
        
        
class ShAttributes(models.Model):
    #id = models.IntegerField(null=False, primary_key=True, blank=False)
    name = models.CharField(max_length=256, blank=False)
    comment = models.TextField(blank=True)
    value = models.CharField(max_length=256,blank=False)
    cls = models.ForeignKey(ShClasses, db_column='cid', related_name='attrs')
    class Meta:
        db_table = u'll_attributes'
        
reversion.register(ShAttributes)       
        
class ShMethods(models.Model):
    #id = models.IntegerField(null=False, primary_key=True, blank=False)
    name = models.CharField(max_length=256, blank=False)
    comment = models.TextField(blank=True)
    body = models.TextField(blank=True)
    args = models.CharField(max_length=256, blank=True)
    cls = models.ForeignKey(ShClasses, db_column='cid', related_name='methods')
    class Meta:
        db_table = u'll_methods'
        
reversion.register(ShMethods) 

        
