from popserver.lib.base import *
from popserver.lib.controller_utils import find_widget, build_json_response

class WidgetsController(BaseController):

    @authorize(And(UserInRoute('username'),ValidAuthKitUser()))
    def index(self):
        c.user = self.user
        c.baseUrl = self._getBaseUrl()
        widget = find_widget(c.user.username, 1)
        c.theme = widget.getTheme()
        
        return render('/website/user/widgets.mako')


    @authorize(And(UserInRoute('username'),ValidAuthKitUser()))
    @jsonify
    def theme(self, username, id):
        widget = find_widget(username, id)
        status = "ok"
        
        if 'theme' not in request.POST:
            status = "error"
            desc = "Oops, try again!"
        else:
            # TODO: verificar que el theme exista
            widget.theme = request.POST['theme']
            widget.flush()
            desc = "Done! Your widget color was updated."
        
        return build_json_response(status, desc)

