import copy

class Sequence(object):
    def __init__(self, callable_obj, start=0):
        self.callable_obj = callable_obj
        self.count = start
    
    def next(self):
        return self.callable_obj(self.next_count())
    
    def next_count(self):
        self.count += 1
        return self.count
    
class Relationship(object):
    
    def __init__(self, name_of_factory, kwargs):
        self.name = name_of_factory
        self.kwargs = kwargs
    
    def create(self, *args, **kwargs):
        return Factory.create(self.name, **self.kwargs)

class Blueprint(object):
    """
    Store the blueprint to create a object for the factory.
    """
    
    def __init__(self, name_of_factory, model, kwargs, create_function):
        self.name_of_factory = name_of_factory
        self.model = model
        self.kwargs = kwargs
        self.create_function = create_function
    
    def create(self, kwargs):
        """
        Create the object following the blueprint.
        """
        params = copy.copy(self.kwargs)
        params.update(kwargs)
        
        for key, value in params.iteritems():
            if isinstance(value, Relationship):
                params[key] = value.create()
            elif isinstance(value, Sequence): 
                params[key] = value.next()
        
        func = getattr(self.model.objects, self.create_function)
        result = func(**params)

        return result

class Factory(object):
    __factories__ = {}
    
    class NoFactoryDefined(Exception): pass
    
    @classmethod
    def define(self, name_of_factory, model, kwargs, create_function='create'):
        bp = Blueprint(name_of_factory, model, kwargs, create_function)
        self.__factories__[name_of_factory] = bp
    
    @classmethod
    def create(self, name_of_factory, **kwargs):
        bp = self.__factories__.get(name_of_factory)
        if not bp == None:
            return bp.create(kwargs)
        raise self.NoFactoryDefined("There was no factory defined for %s" % name_of_factory)
    
    @classmethod
    def relationship(self, name_of_factory, **kwargs):
        return Relationship(name_of_factory, kwargs)
    
    @classmethod
    def sequence(self, callable_obj, start=0):
        return Sequence(callable_obj, start)
    
    @classmethod
    def attributes_for(self, name_of_factory):
        bp = self.__factories__.get(name_of_factory)
        if not bp == None:
            res = {}
            for key, value in bp.kwargs.iteritems():
                if not isinstance(value, Relationship):
                    if isinstance(value, Sequence): 
                        res[key] = value.next()
                    else:
                        res[key] = value
                
            
            return res
        raise self.NoFactoryDefined("There was no factory defined for %s" % name_of_factory)

## Test Case
#from django_model_factory.models import TestModel, TestModelFriend
#from notification.models import Carrier

#Factory.define('test', TestModel, {
#    'name' : "Vitaly Babiy"
#})

#Factory.define('friend', TestModelFriend, {
#    'age' : 10,
#    'friend' : Factory.relationship('test')
#})

#Factory.define('sprint', Carrier, {
#    'name' : Factory.sequence(lambda n: "%d-sprint" % n),
#    'gateway' : 'gateway'
#})

#print "Finshed Creating Factory"
