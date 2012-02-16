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
from django.core.signals import *

import reversion

newline = "\n"
tab = "    "
tab2 = 2 * tab
tab3 = 3 * tab




jsClassImpl = """
var LazyLandscapeField = LazyLandscapeField || Object.create({},  {
        _class:{value: new Array(), writable: true, configurable: true},
        New:{value: function(o)
            {
                    for(var i = 0; i < this._class.length; i++)
                    {
                            var c = this._class[i];
                            if(c._T == o)
                            {
                                    var ret = Object.create(c);
                                    Object.defineProperty(ret, "_cparent", {value : ret.__proto__, writable : false, enumerable : false, configurable : false});
                                    // ok, we need a bit of a trick as neither c nor ret got the hasOwnProperty method
                                    ret.hasOwnProperty = Object.prototype.hasOwnProperty;
                                    var args = Array.prototype.slice.call(arguments);
                                    args.shift();
                                    if(ret.__proto__.hasOwnProperty('init') && ((typeof ret.init) == 'function'))
                                    {
                                            var init = ret.init;
                                            if(args.length >= init.length)
                                                    init.apply(ret, args);
                                            else
                                                    throw new Error(ret.Type() +".init() takes "+init.length+" argument(s), "+args.length+" provided");
                                    }
                                    return ret;
                            }
                    }
                    return null;
            }},
        CreateClass:{value: function(proto)
            {
                    Object.defineProperty(proto, "Type", {value : function(){return this._T}, writable : false, enumerable : false, configurable : false});
                    Object.defineProperty(proto, "_cparent", {value : proto.__proto__, writable : false, enumerable : false, configurable : false});
                    Object.defineProperty(proto, "Parent", {value : function()
                                                                    {
                                                                            if(this.hasOwnProperty('_cparent'))
                                                                            {
                                                                                    if(this._cparent.hasOwnProperty('_T'))
                                                                                    {
                                                                                            if(this._cparent._T != this._T)
                                                                                                    return this._cparent;
                                                                                            else
                                                                                                    return this._cparent.Parent();
                                                                                    }
                                                                            }
                                                                            return null;
                                                                    }, writable : false, enumerable : false, configurable : false});
                    proto.hasOwnProperty = Object.prototype.hasOwnProperty;
                    this._class.push(proto);
            }},
        GetClass:{value: function(o)
            {
                    for(var i = 0; i < this._class.length; i++)
                    {
                            var c = this._class[i];
                            if(c._T == o)
                            {
                                    return c;
                            }
                    }
                    return null;
            }}
});
"""

class ShClasses(models.Model):
    #id = models.IntegerField(null=False, primary_key=True, blank=False)
    name = models.CharField(max_length=256, blank=False)
    comment = models.TextField(blank=True)
    field = models.CharField(max_length=256, blank=False)
    lang = models.CharField(max_length=32, blank=False, choices=[['python','Python'],['js','Javascript']])
    public = models.BooleanField(default=False)
    
    parents = models.ManyToManyField('self',db_table="ll_parents",related_name='children',  symmetrical=False ,blank=True)
    deps = models.ManyToManyField('self',db_table="ll_deps",related_name='nodes', symmetrical=False ,blank=True)
    
    class Meta:
        db_table = u'll_classes'
        
    def __init__(self, *args, **kwargs):
        super(ShClasses, self).__init__(*args, **kwargs)
        self.attachRevision()
        
    def __unicode__(self):
        return self.name
        
    def str(self):
        return self.__unicode__()
        
    def write_class_python(self, ccontrol, clist, order):
        if self.id in ccontrol:
            return 
        #print( ((1024 - order[0]) * tab) + '>' +self.name) 
                
        ret = []
        ccontrol.append(self.id)
        #if hasattr(self, 'rel_target'):
        deps = self.deps.all()
        #for i in dir(deps):
                #print '%s => %s' % (i, getattr(deps,i))
        for r in deps:
            if r is not None:
                print 'DEP of %s => %s' % (self.name, r.name)
                r.write_class_python(ccontrol, clist, order)
            
        extend = []
        parents = self.parents.all()
        for r in parents:
            if r is not None:
                print 'PARENT of %s => %s' % (self.name, r.name)
                r.write_class_python(ccontrol, clist, order)
                extend.append(p.field + '.' + p.name)
            
        #ret.append(newline+'class ' + self.field+ ':')
        if len(extend) > 0:
            ret.append(newline+tab+'class ' + self.name + '('+ ','.join(extend) +'):'+ newline)
        else:
            ret.append(newline+tab+'class ' + self.name + '(object):' + newline)
                
        for a in self.attrs.all():
            ret.append(tab2 + a.name + ' =  ' + a.value + newline)
        
        for m in self.methods.all():
            args = ['self']
            for a in m.args.split(','):
                if len(a.strip()) > 0:
                    args.append(a)
            hasBody = len(m.body.strip()) > 0
            if hasBody:
                tabBody = []
                for l in m.body.splitlines():
                    tabBody.append(''.join([tab3,l,newline]))
                ret.append( newline.join([ tab2 + 'def ' + m.name +'(' + ','.join(args) + '):', ''.join(tabBody) ,newline]) )
            else:
                print 'WARNING : %s.%s.%s has no body : len(m.body) = %d' % (self.field, self.name, m.name, len(m.body))
                fname = tab2 + 'def ' + m.name +'(' + ','.join(args) + '):'
                ret.append( newline.join([ fname, tab3 + 'pass' , newline ] ) )
            
        ret.append(newline)
        clist.append({
            'field' : self.field,
            'name' : self.name,
            'source' : ''.join(ret),
            'order' : order[0]
            })
            
        order[0] -= 1
        print 'ORDER (%s) %d'%(self.name, order[0])
      
    def sortSource(self, a , b):
        sa = a['order']
        sb = b['order']
        if sa > sb:
            return -1
        if sa < sb:
            return 1
        return 0
        
    def hashSource(self, clist):
        clist.sort(self.sortSource)
        ret = []
        cur = []
        f = ''
        for i in clist:
            if f != i['field']:
                if cur:
                    ret.append((f, cur))
                    cur = []
                f = i['field']
                
            cur.append(i)
        if cur:
            ret.append((f, cur))
        return ret
        
    def get_python_source(self):
        ccontrol = []
        clist = []
        self.write_class_python(ccontrol, clist, [1024])
        return self.hashSource(clist)
        
    def write_class_js(self, wp):
        if self.id in wp:
            return ''
            
        wp.append(self.id)
        ret = []
        deps = self.deps.all()
        for r in deps:
            if r is not None:
                ret.append(r.write_class_js( wp))
                
        parents = self.parents.all()
        for r in parents:
            if r is not None:
                ret.append(r.write_class_js( wp))

        ret.append('var '+self.field+' = '+self.field+' || Object.create(LazyLandscapeField, {field : {value : "'+self.field+'"}});')

        ret.append("(function(field){")
        ret.append(tab + "var parent = {};")
        for p in parents:
            ret.append(tab + 'parent = '+p.field+'+GetClass("'+p.name+'"); ')


        ret.append(tab + 'var props = { _T : {value: "'+self.name+'"},')

        for attr in self.attrs.all():
            ret.append(tab + attr.name +': {value : '+ attr.value +', writable: true, enumerable: true, configurable: true},')

        for m in self.methods.all():
            ret.append(tab +  m.name + ': {value : function('+ m.args +'){')
            tabBody = []
            for l in m.body.splitlines():
                tabBody.append(''.join([tab2,l,newline]))
            ret.append(''.join(tabBody))
            ret.append(tab +'}, writable: true, enumerable: true, configurable: true}, ')

        ret.append(tab +'};')
        ret.append(tab +'field.CreateClass(Object.create(parent, props)); ');
        ret.append('})('+ self.field +');')

        return newline.join(ret)        
        
    def get_js_source(self):
        ccontrol = []
        ret = [jsClassImpl]
        ret.append( self.write_class_js(ccontrol) )
        return newline.join(ret)
        
        
    def source(self):
        if self.lang == 'python':
            return self.get_python_source()
        elif self.lang == 'js':
            return self.get_js_source()
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
