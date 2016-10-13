# Invalidate Sphere on Posts
# Cache based on Sphere on Gets
# Forma para declarar un action y una forma de dado un action, una forma de sacar el sphereId
from popserver.lib.cache import *
from popserver.lib.cache.pylons import *
from popserver.lib.cache.persistence import *
from pylons import request

from popserver.controllers.widget.widget import WidgetController
from popserver.controllers.website.widgets import WidgetsController
from popserver.controllers.website.settings import SettingsController
from popserver.controllers.website.service import ServiceController
from popserver.controllers.website.interests import InterestsController

# CodePoint conditions

def hasParamName(param):
    return lambda call: param in request.params()

def hasNoRequestParams(call):
    return len(request.params) == 0


cacheConfig = CacheConfig()

# User Resource Type
userResourceType = cacheConfig.defineResourceType('User')
## Caching
userResourceType.cacheOn(CodePoint(WidgetController.show, hasNoRequestParams), idOnParameter(1)) 
userResourceType.cacheOn(CodePoint(WidgetController.content, hasNoRequestParams), idOnParameter(1)) 
# Por ahora solo cacheamos el widget
#userResourceType.cacheOn(CodePoint(WidgetController.home), idOnParameter(1)) # username es el 1er parametro posicional para WidgetController.home
#userResourceType.cacheOn(CodePoint(WidgetController.media), idOnParameter(1)) 

## Invalidation
userResourceType.invalidateOn(CodePoint(SettingsController.personal_settings), idOnEnviron('REMOTE_USER'))
userResourceType.invalidateOn(CodePoint(SettingsController.upload), idOnParameter(1)) 
userResourceType.invalidateOn(CodePoint(WidgetsController.theme, hasParamName('id')), idOnParameter(1)) 
userResourceType.invalidateOn(CodePoint(ServiceController.new), idOnParameter(1)) 
userResourceType.invalidateOn(CodePoint(ServiceController.cancel), idOnParameter(1)) 
userResourceType.invalidateOn(CodePoint(InterestsController.setTagInterest), idOnEnviron('REMOTE_USER'))


def enable_cache():
    cm = CacheManager(PopegoDBCachePersistence(), PylonsTagManager(), PylonsHitResponseGenerator())
    cm.activate(cacheConfig)



