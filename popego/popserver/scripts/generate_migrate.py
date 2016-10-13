from popserver.lib import model_setup
from popserver import model

def parseCodePath(path):
    if ':' in path:
        modulePath,attrs = path.split(':',1)
        
        needsCall = False
        if attrs.endswith('()'):
            attrs = attrs[:-2]
            needsCall = True
        attrs = attrs.split(".")
        obj = __import__(modulePath, fromlist=['__name__'])
            
        for attr in attrs:
            obj = getattr(obj, attr)
        if needsCall: 
            obj = obj()
    else:
        obj = __import__(path, fromlist=['__name__'])
        
    return obj


# Levanto parametros
import sys
classes = sys.argv[1:]

# Cambio el SchemaGenerator a Usar

engineDialect = model.metadata.bind.dialect

class MySchemaGenerator(engineDialect.schemagenerator):
    def execute(self):
        print self.buffer.getvalue()

engineDialect.schemagenerator = MySchemaGenerator

# Ejecuto el create de cada Modelo
for cl in classes:
    if '.' in cl:
        aModelClass = parseCodePath(cl)
    else:
        aModelClass = getattr(model,cl)
    aModelClass.table.create()


