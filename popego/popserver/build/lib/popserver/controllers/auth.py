import logging

from popserver.lib.base import *
from authkit.authorize.pylons_adaptors import authorize 
from authkit.permissions import RemoteUser, ValidAuthKitUser, UserIn
from authkit.authorize import middleware
from routes import url_for

log = logging.getLogger(__name__)

class AuthController(BaseController):

    def signout(self):
        from_where = str(request.params.get('from'))
        if from_where != 'widget':
            redirect_to(controller='website/home')
        else:
            #self._logout()
            widget_owner = str(request.params.get('owner'))
            parent_url = str(request.params.get('parentUrl'))
            widgetTheme = str(request.params.get('theme'))
            instanceId = str(request.params.get('instanceId'))
            redirect_to(controller='widget/widget', action='content', 
                        username=widget_owner, parentUrl=parent_url, 
                        theme=widgetTheme, instanceId=instanceId)

    #@validate(schema=forms.UserLogin())
    def signin(self):
       """
       Verify username and password
       """
       # Both fields filled?
#       form_username = self.form_result['username']
#       form_password = self.form_result['password']
       form_username = str(request.params.get('username'))
       form_password = str(request.params.get('password'))
       form_widgetOwner = str(request.params.get('widgetOwner'))
       from_where = str(request.params.get('from'))
       parent_url = str(request.params.get('parentUrl'))
       widgetTheme = str(request.params.get('theme'))
       instanceId = str(request.params.get('instanceId'))
       
       # Get user data from database
       users = request.environ['authkit.users']

       if '@' in form_username: # user may enter email instead of username
           form_email = form_username.strip()
	   try:
	       u = users.model.User.query.filter_by(email=form_email).first()
	       form_username = u.username
	   except:
               c.error = True

       if not users.user_exists(form_username):
           c.error = True
           if from_where != 'widget':  
               return render('/website/home/index.mako')
               
       # Wrong password? 
       if not users.user_has_password(form_username, form_password):
           c.error = True
           if from_where != 'widget':
               return render('/website/home/index.mako')
             
       # Mark user as logged in
       self._login(form_username)
       
       if from_where == 'widget':
           redirect_to(controller='widget/widget', action='content', 
                       username=form_widgetOwner, parentUrl=parent_url, 
                       theme=widgetTheme, viewerLoginError=c.error,
                       instanceId=instanceId)
       else: 
           redirect_to(action='index', controller='website/service', 
                       username=form_username)

# AuthController = middleware(AuthController(), ValidAuthKitUser())
